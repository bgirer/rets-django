# coding=utf-8
import datetime as dt
import logging
import signal
import sys
import threading
import time
import traceback
from math import ceil

import pytz
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import DataError
from psycopg2 import DataError as PG_DataError
from rets.client import RetsClient
from rets.errors import *

from rets_django import models

logger = logging.getLogger(__name__)

procs = []


def get_process(processes, process_name):
    for process in processes:
        if process.name == process_name:
            return process
        else:
            return None


class ListingException(Exception):
    pass


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
        assert group is None, "group argument must be None for now"
        if kwargs is None:
            kwargs = {}
        self._target = target
        self._name = str(name)
        self._args = args
        self._kwargs = kwargs
        self.daemon = daemon

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def normalize_none(field_value):
    """
    Helper function to normalize strings that should be None
    """

    none_strings = ['n/k', 'none known', 'unknown', 'no/unknown', '0x0']
    if not field_value:
        normalized_field_value = None
    elif type(field_value) == str and field_value.lower() in none_strings:
        normalized_field_value = None
    else:
        normalized_field_value = field_value
    return normalized_field_value


def get_class_metadata_as_dict(resource_class):
    """
    Maps a RETS Resource.Class.Table.metadata instance as a dictionary (normally a tuple
    of OrderedDicts).
    """
    column_names = set()
    for column_name in resource_class.table.fields:
        column_names.add(column_name)
    class_metadata = dict()
    for column_metadatum in resource_class.table.metadata:
        class_metadata[column_metadatum['SystemName']] = column_metadatum
    return class_metadata


def make_query_string(query_dict):
    """
    Build RETS search's required query string from a dictionary of DMQL name=>value
    pairs.
    """
    query_string = str()
    counter = 0
    query_keys = list(query_dict.keys())
    for name in query_keys:
        query_string += '(%s=%s)' % (name, query_dict[name])
        counter += 1
        if counter != len(query_keys):
            query_string += ','
    return query_string


def submit_search_query(query_string, query_limit, query_offset,
                        resource_class):
    """
    Submit a search query request to the RETS API
    """
    search_result = resource_class.search(
            query='%s' % query_string, limit=query_limit, offset=query_offset)
    return search_result


def extract_listing_data(listing):
    """
    Extract the data from a rets-python Record object into a Listing object
    """

    # get the data dict from the listing
    listing_data = listing.data
    # get the SystemNames for all of this listing's data tuples
    listing_data_keys = list(listing_data.keys())
    # instantiate a Listing object with the RETS PK as the system_id value
    listing_object = models.Listing(system_id=listing.resource_key)
    # get all the fields from the Listing model
    listing_object_fields = models.Listing._meta.get_fields()
    # iterate over each Listing model field
    for field in listing_object_fields:
        # Skip relation fields
        if not field.is_relation:
            try:
                # assign the field's db_column to a variable
                field_db_column = field.db_column
            except AttributeError:
                # if no db_column, skip it
                continue
            if field_db_column in listing_data_keys:
                # if we find the db_column in the SystemNames list, update the new
                #   Listing object accordingly
                if listing_data[field_db_column]:
                    if type(listing_data[field_db_column]) in [dt.datetime,
                                                               dt.date]:
                        attr = listing_data[field_db_column].replace(
                                tzinfo=pytz.UTC)
                        setattr(listing_object, field.name,
                                normalize_none(attr))
                    else:
                        setattr(listing_object, field.name,
                                normalize_none(listing_data[field_db_column]))
    return listing_object


def update_core_listing_data(existing_listing_object, new_listing_object):
    """
    Find what fields have been changed for an updated Listing object, update the fields
    on the existing object accordingly, and return the updated object.
    """
    listing_object_fields = []
    for field in models.Listing._meta.get_fields():
        try:
            if field.db_column.startswith('L_'):
                listing_object_fields.append(field.name)
        except AttributeError:
            continue
    new_listing_data = [{d: getattr(new_listing_object, d)} for d in
                        listing_object_fields]
    updated_listing_object = existing_listing_object
    for new_attr in new_listing_data:
        new_attr_key = list(new_attr.keys())[0]
        setattr(updated_listing_object, new_attr_key,
                new_attr.get(new_attr_key))
    return updated_listing_object


class Command(BaseCommand):
    """
    Find listings whose status is not available and update their status in the database.
    """
    requires_migrations_checks = True
    queries = {
        'L_StatusCatID': '~1',
    }

    limit = 2500.0

    client = RetsClient(
            login_url=settings.RETS_LOGIN_URL,
            username=settings.RETS_USER,
            password=settings.RETS_PASSWORD,
            auth_type='basic'
    )

    def add_arguments(self, parser):
        parser.add_argument('--class', metavar="-c", action="store", type=str,
                            help='Name of property class to search. Should be one of: "RE_1", "RI_2" or "LN_3".',
                            dest='property_class_name',
                            )

    def handle(self, *args, **options):
        resource_class_name = options['property_class_name']
        resource = self.client.get_resource('Property')
        try:
            resource_class = resource.get_class(resource_class_name)
        except KeyError:
            logger.error('Invalid argument: %s' % resource_class_name)
            raise CommandError()
        query_string = make_query_string(self.queries)
        limit = self.limit
        offset = 1

        search_result_count = self.client.http.search(resource='Property',
                                                      class_=resource_class_name,
                                                      query='(L_StatusCatID=1)',
                                                      count=2).count
        block_count = ceil(search_result_count / limit)
        counter = 1
        for block in range(0, int(block_count)):
            # Start a process with handle_block() as its callback for each block of
            #   search results
            process = StoppableThread(target=self.handle_block,
                                      name='%s__scrub_block_%i' % (
                                              resource_class.name, counter),
                                      kwargs={'resource_class': resource_class,
                                              'query_string': query_string,
                                              'limit': int(limit),
                                              'offset': int(offset),
                                              'thread_name': '%s__scrub_block_%i' % (
                                                      resource_class.name, counter)
                                              }
                                      )
            process.start()
            time.sleep(30)
            logger.info('Listing scrubber process started: %s' % process.name)
            procs.append(process)
            # self.handle_block(resource_class, query_string, limit, offset)
            offset += limit
            counter += 1

    def handle_block(self, resource_class, query_string, limit, offset, thread_name):
        try:
            search_result = submit_search_query(query_string, int(limit),
                                                int(offset), resource_class)
        except (RetsApiError, AttributeError) as e:
            raise CommandError(e)
        if search_result.data:
            # Map the search results to a dict
            results_dict = dict()
            for result in search_result.data:
                results_dict[result.data['L_ListingID']] = result
            # Get all the system_ids for the active properties in the database
            all_db_active_listing_ids = [i['system_id'] for i in
                                         models.Listing.objects.filter(
                                                 status='ACTIVE').values('system_id')]
            # Check the IDs of the listings in the search results against the list of IDs of the database's active listings
            all_rets_inactive_listing_ids = [j.data['L_ListingID'] for j in
                                             search_result.data]
            ids_of_listings_to_update = list(set(all_db_active_listing_ids).intersection(
                    set(all_rets_inactive_listing_ids)))
            listings_to_update = models.Listing.objects.filter(
                    system_id__in=ids_of_listings_to_update)
            # For each listing that is active in the database but present in the non-active listings search results, update the listing.
            if not len(listings_to_update):
                logger.info(
                        '[%s] No listings for Property Class <%s> need to be scrubbed from the database.' % (
                            thread_name, resource_class.name))
                logger.info('Stopping thread: %s' % thread_name)
                process = get_process(procs, thread_name)
                if process and not process.stopped():
                    process.stop()
            else:
                logger.info('%i Listings have updated statuses. Updating now...' % len(
                        listings_to_update))
                for listing in listings_to_update:
                    results_item = results_dict.get(listing.system_id)
                    try:
                        self.handle_listing(listing, results_item)
                    except ListingException:
                        continue

    @staticmethod
    def handle_listing(listing_object, results_item):
        try:
            new_listing_object = extract_listing_data(results_item)
            updated_listing_object = update_core_listing_data(listing_object,
                                                              new_listing_object)
            updated_listing_object.save()
        except (ValueError, DataError, PG_DataError):
            logger.debug(traceback.print_exc(limit=None))
            raise ListingException()


# Handle premature exits
def signal_handler(signal, frame):
    for proc in procs:
        if not proc.stopped():
            proc.stop()
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)
