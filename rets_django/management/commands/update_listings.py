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
from django.db.utils import DataError, IntegrityError
from geopy.exc import GeocoderServiceError, GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim
from psycopg2 import DataError as PG_DataError
from requests.exceptions import ConnectionError
from requests_toolbelt.multipart.decoder import MultipartDecoder
from rets.client import RetsClient
from rets.errors import *
from rets.http.client import _build_entity_object_ids
from urllib3.exceptions import ProtocolError

from rets_django import models

logger = logging.getLogger(__name__)
new_objects_count = 0

# Exit signal handler variables
new_objects_cache = []
procs = []


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
                        class_resource):
    """
    Submit a search query request to the RETS API
    """

    search_result = class_resource.search(
            query='%s' % query_string, limit=query_limit, offset=query_offset)
    return search_result


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
                        setattr(listing_object, field.name, attr)
                    else:
                        setattr(listing_object, field.name,
                                normalize_none(listing_data[field_db_column]))
    return listing_object


def extract_agent_data(listing):
    """
    Extract the data from a rets-python Record object into an
    Agent object, using the prefix parameter to determine
    agent type.
    """

    # get the data dict from the listing
    listing_data = listing.data
    # get the SystemNames for all of this listing's data tuples
    listing_data_keys = list(listing_data.keys())
    # get all the fields from the Agent model
    agent_object_fields = models.Agent._meta.get_fields()
    # instantiate an empty Agent object
    agent_object = models.Agent()
    # iterate over each of the Agent model fields
    for field in agent_object_fields:
        try:
            if not field.is_relation and not field.primary_key:
                # if the field is not a relation or PK, get its db_column and prepend the current agent prefix
                field_db_column = field.db_column
                if field_db_column in listing_data_keys:
                    # if the rets name (prefix + db_column) is in the listing data, add it to the new Agent object
                    if listing_data[field_db_column]:
                        # if the listing data's value for this field isn't None, add it to the object
                        setattr(agent_object, field.name,
                                normalize_none(listing_data[field_db_column]))
        except AttributeError:
            # if the field doesn't have a db_column, just skip this loop iteration
            continue
    return agent_object


def extract_feature_data(listing, property_class):
    """
    Extract the data from a rets-python Record object into a Listing object
    """

    # Get the metadata for this resource class
    property_class_metadata = get_class_metadata_as_dict(property_class)
    # get the data dict from the listing
    listing_data = listing.data
    # get the SystemNames for all of this listing's data tuples
    listing_data_keys = list(listing_data.keys())
    # do a get_or_create() on each Feature datapoint
    feature_prefix = 'LFD_'
    feature_objects = set()
    for listing_data_key in listing_data_keys:
        if listing_data_key.startswith(feature_prefix):
            if listing_data[listing_data_key]:
                feature_normal_name = property_class_metadata[listing_data_key][
                    'LongName']
                for feature_value in listing_data[listing_data_key]:
                    if normalize_none(feature_value):
                        feature_object, created = models.Feature.objects.get_or_create(
                                rets_name=listing_data_key, value=feature_value,
                                name=feature_normal_name)
                        feature_objects.add(feature_object)
    return feature_objects


def extract_remark_data(listing):
    """
    Extract the data from a rets-python Record object into a Remark object.
    """

    # get the data dict from the listing
    listing_data = listing.data
    # get the SystemNames for all of this listing's data tuples
    listing_data_keys = list(listing_data.keys())
    # get all the fields from the Remark model
    remark_object_fields = models.Remark._meta.get_fields()
    # instantiate an empty Remark object
    remark_object = models.Remark()
    # iterate over each of the Remark model fields
    for field in remark_object_fields:
        try:
            if not field.is_relation and not field.primary_key:
                # if the field is not a relation or PK, get its db_column and prepend the current remark prefix
                field_db_column = field.db_column
                if field_db_column in listing_data_keys:
                    # if the rets name (prefix + db_column) is in the listing data, add it to the new Remark object
                    if listing_data[field_db_column]:
                        # if the listing data's value for this field isn't None, add it to the object
                        setattr(remark_object, field.name,
                                normalize_none(listing_data[field_db_column]))
        except AttributeError:
            # if the field doesn't have a db_column, just skip this loop iteration
            continue
    return remark_object


def extract_office_data(listing):
    """
    Extract the office data from a rets-python Record object into an
    Office object.
    """

    # get the data dict from the listing
    listing_data = listing.data
    # get the SystemNames for all of this listing's data tuples
    listing_data_keys = list(listing_data.keys())
    # get all the fields from the Office model
    office_object_fields = models.Office._meta.get_fields()
    # instantiate an empty Office object
    office_object = models.Office()
    # iterate over each of the Office model fields
    for field in office_object_fields:
        try:
            if not field.is_relation and not field.primary_key:
                # if the field is not a relation or PK, get its db_column and prepend the current office prefix
                field_db_column = field.db_column
                if field_db_column in listing_data_keys:
                    # if the rets name (prefix + db_column) is in the listing data, add it to the new Office object
                    if listing_data[field_db_column]:
                        # if the listing data's value for this field isn't None, add it to the object
                        setattr(office_object, field.name,
                                normalize_none(listing_data[field_db_column]))
        except AttributeError:
            # if the field doesn't have a db_column, just skip this loop iteration
            continue
    return office_object


def extract_tax_info_data(listing):
    """
    Extract the data from a rets-python Record object into an
    TaxInfo object.
    """
    # get the data dict from the listing
    listing_data = listing.data
    # get the SystemNames for all of this listing's data tuples
    listing_data_keys = list(listing_data.keys())
    # get all the fields from the TaxInfo model
    tax_info_object_fields = models.TaxInfo._meta.get_fields()
    # instantiate an empty TaxInfo object
    tax_info_object = models.TaxInfo()
    # iterate over each of the TaxInfo model fields
    for field in tax_info_object_fields:
        try:
            if not field.is_relation and not field.primary_key:
                # if the field is not a relation or PK, get its db_column and prepend the current tax_info prefix
                field_db_column = field.db_column
                if field_db_column in listing_data_keys:
                    # if the rets name (prefix + db_column) is in the listing data, add it to the new TaxInfo object
                    if listing_data[field_db_column]:
                        # if the listing data's value for this field isn't None, add it to the object
                        setattr(tax_info_object, field.name,
                                normalize_none(listing_data[field_db_column]))
        except AttributeError:
            # if the field doesn't have a db_column, just skip this loop iteration
            continue
    return tax_info_object


def construct_full_address(listing_object):
    return listing_object.address, listing_object.city, listing_object.state, listing_object.zip_code


def get_geocoordinates(geolocator, listing_object):
    address, city, state, zip_code = construct_full_address(listing_object)
    address_string_combinations = [
        '%s %s %s %s' % (address, city, state, zip_code),
        '%s %s %s' % (address, city, state),
        '%s %s' % (address, zip_code)
    ]
    location = None
    for address_string_combination in address_string_combinations:
        try:
            location = geolocator.geocode(address_string_combination)
        except (GeocoderTimedOut, GeocoderServiceError, GeocoderUnavailable):
            time.sleep(10)
            try:
                location = geolocator.geocode(address_string_combination)
            except (
                    GeocoderTimedOut, GeocoderServiceError,
                    GeocoderUnavailable):
                return None, None
        if location:
            return location.latitude, location.longitude
        else:
            continue
    if not location:
        return None, None


def extract_virtual_tour_data(listing):
    """
    Extract the data from a rets-python Record object into an
    VirtualTour object.
    """
    # get the data dict from the listing
    listing_data = listing.data
    # get the SystemNames for all of this listing's data tuples
    listing_data_keys = list(listing_data.keys())
    # get all the fields from the VirtualTour model
    virtual_tour_object_fields = models.VirtualTour._meta.get_fields()
    # instantiate an empty VirtualTour object
    virtual_tour_object = models.VirtualTour()
    # iterate over each of the VirtualTour model fields
    for field in virtual_tour_object_fields:
        try:
            if not field.is_relation and not field.primary_key:
                # if the field is not a relation or PK, get its db_column and prepend the current virtual_tour prefix
                field_db_column = field.db_column
                if field_db_column in listing_data_keys:
                    # if the rets name (prefix + db_column) is in the listing data, add it to the new VirtualTour object
                    if listing_data[field_db_column]:
                        # if the listing data's value for this field isn't None, add it to the object
                        setattr(virtual_tour_object, field.name,
                                normalize_none(listing_data[field_db_column]))
        except AttributeError:
            # if the field doesn't have a db_column, just skip this loop iteration
            continue
    return virtual_tour_object


def get_listing_image(part):
    """
    Returns a listing image URL from a MultipartDecoder part object
    """
    return part.headers[b'Location'].decode('utf-8')


def fetch_listing_images(client, listing):
    """
    Makes use of some built-in rets-python methods to get image URLs for a listing. Note:
    this function (and get_listing_image()) were only necessary because rets-python failed
    to return anything useful with its Record.get_object() method when the location
    parameter was set to True.
    """
    headers = {'Accept': '*/*'}
    payload = {'Resource': 'Property', 'Type': 'Photo',
               'ID': _build_entity_object_ids(
                       listing.resource_key), 'Location': 1}
    encoding = 'utf-8'
    try:
        response = client.http._http_post(client.http._url_for('GetObject'),
                                          headers=headers, payload=payload)
    except (ProtocolError, ConnectionError, ConnectionResetError):
        client.http.login()
        response = client.http._http_post(client.http._url_for('GetObject'),
                                          headers=headers, payload=payload)
    multipart = MultipartDecoder.from_response(response, encoding)
    return multipart.parts


class Command(BaseCommand):
    requires_migrations_checks = True

    # Enter DMQL queries as Python dicts here.
    queries = {
        'L_StatusCatID': 1,
    }

    limit = 2500.0

    client = RetsClient(
            login_url=settings.RETS_LOGIN_URL,
            username=settings.RETS_USER,
            password=settings.RETS_PASSWORD,
            auth_type='basic'
    )

    geolocator = Nominatim()

    def add_arguments(self, parser):
        parser.add_argument('--class',
                            metavar="-c",
                            action="store",
                            type=str,
                            help='Name of property class to search. Can be one of: "RE_1", "RI_2" or "LN_3".',
                            dest='property_class_name'
                            )

    def handle(self, *args, **options):
        resource_class_name = options['property_class_name']
        resource = self.client.get_resource('Property')
        try:
            resource_class = resource.get_class(resource_class_name)
        except KeyError:
            raise CommandError('Invalid argument: %s' % resource_class_name)
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
            proc = StoppableThread(target=self.handle_block,
                                   name='{%s__upsert_block_%i' % (
                                           resource_class.name, counter),
                                   kwargs={'resource_class': resource_class,
                                           'query_string': query_string,
                                           'limit': int(limit),
                                           'offset': int(offset),
                                           'thread_name': '{%s__scrub_block_%i' % (
                                                   resource_class.name, counter)
                                           }
                                   )
            proc.start()
            time.sleep(30)
            logger.info('Listing update process started: %s' % proc.name)
            procs.append(proc)
            # self.handle_block(resource_class, query_string, limit, offset)
            offset += limit
            counter += 1

    def handle_block(self, resource_class, query_string, limit, offset, thread_name):
        """
        Collect RETS search query data and update our models with the new data.
        """
        try:
            search_result = submit_search_query(query_string, int(limit),
                                                int(offset),
                                                resource_class)
        except (RetsApiError, AttributeError) as e:
            raise CommandError(e)
        if search_result.data:
            for listing in search_result.data:
                try:
                    self.handle_listing(listing, resource_class)
                except ListingException:
                    continue
            logger.info(
                    'Block <%s> added %i new Listing objects to the database.' % (
                        thread_name, new_objects_count))

    def handle_listing(self, listing, resource_class):
        """
        Update or insert a Listing object
        """
        # Create the listing object & global variable declaring whether or not the
        #   listing should be deleted if the script exits prematurely.
        listing_object = extract_listing_data(listing)
        # Check if this listing already exists
        listing_object_dupe_check = models.Listing.objects.filter(
                system_id=listing_object.system_id)
        # If the listing already exists in DB, check if it was updated
        if listing_object_dupe_check:
            existing_listing_object = models.Listing.objects.get(
                    system_id=listing_object.system_id)
            # Force UTC timezone awareness on existing and new listings' update_date value
            existing_listing_update_date = existing_listing_object.update_date
            new_listing_update_date = listing_object.update_date
            aware_existing_listing_update_date = existing_listing_update_date.replace(
                    tzinfo=pytz.UTC)
            aware_new_listing_update_date = new_listing_update_date.replace(
                    tzinfo=pytz.UTC)
            # Check if the new listing's update_date is later than the new one
            if aware_new_listing_update_date > aware_existing_listing_update_date:
                updated_listing_object = update_core_listing_data(
                        existing_listing_object, listing_object)
                updated_listing_object.save()
        # If the listing doesn't already exist, add it to the database!
        else:
            try:
                # try saving the listing object to the model, but
                #   continue and log the error if it fails.
                try:
                    listing_object.save()
                    new_objects_cache.append(listing_object)
                except (IntegrityError, DataError, PG_DataError):
                    logger.debug(
                            'Received error when inserting new Listing object:')
                    logger.debug(traceback.print_exc(limit=None))
                    raise ListingException()
                # Retrieve a set of Feature objects
                feature_objects = extract_feature_data(listing,
                                                       resource_class)
                for feature_object in feature_objects:
                    # Add each feature to the new Listing object
                    listing_object.features.add(feature_object)
                listing_object.save()
                # Create and attach the Remark object
                remark_object = extract_remark_data(listing)
                remark_object.save()
                listing_object.remark = remark_object
                listing_object.save()

                # Create the agent object
                agent_object = extract_agent_data(listing)
                # if the agent object has a unique identifier, get or
                #   create that Agent object and add it to listing's
                #   agent_set
                if agent_object.agent_id:
                    agent_object_final, created = models.Agent.objects.get_or_create(
                            agent_id=agent_object.agent_id)
                    listing_object.agent_set.add(agent_object_final)
                    listing_object.save()
                # Create and attach the office object
                office_object = extract_office_data(listing)
                # if the office object has a unique identifier, get or
                #   create that Office object and add it to listing's
                #   office_set
                if office_object.office_id:
                    office_object_final, created = models.Office.objects.get_or_create(
                            office_id=office_object.office_id)
                    listing_object.office_set.add(office_object_final)
                    listing_object.save()
                # Create and attach the TaxInfo object
                tax_info_object = extract_tax_info_data(listing)
                tax_info_object.listing = listing_object
                tax_info_object.save()
                # Create and attach the VirtualTour object
                virtual_tour_object = extract_virtual_tour_data(
                        listing)
                virtual_tour_object.listing = listing_object
                virtual_tour_object.save()
                # Get geocoordinates and add them to the listing
                latitude, longitude = get_geocoordinates(
                        self.geolocator, listing_object)
                listing_object.latitude = latitude
                listing_object.longitude = longitude
                # Get listing images
                listing_image_responses = fetch_listing_images(self.client, listing)
                for part in listing_image_responses:
                    image_url = get_listing_image(part)
                    if len(image_url):
                        image_object = models.Photo(listing=listing_object,
                                                    url=get_listing_image(part))
                        image_object.save()
                # Save the listing object and remove it from the new objects cache
                listing_object.save()
                new_objects_cache.remove(listing_object)
                updated_objects_count = globals().get('new_objects_count')
                globals().update({'new_objects_count': updated_objects_count + 1})
            except (ValueError, DataError, PG_DataError):
                logger.debug(traceback.print_exc(limit=None))
                try:
                    new_objects_cache.remove(listing_object)
                except ValueError:
                    pass
                raise ListingException()


# Handle premature exits
def signal_handler(signal, frame):
    if len(new_objects_cache):
        print(
                'Received an exit signal. Trying to delete %i Listing object(s): %s' % (
                    len(new_objects_cache),
                    [i.system_id for i in new_objects_cache]))
        for listing_object in new_objects_cache:
            updated_listing_object = models.Listing.objects.get(
                    system_id=listing_object.system_id)
            updated_listing_object.delete()
            print('Deleted Listing object <%s> before exiting' % listing_object.system_id)
    for proc in procs:
        if not proc.stopped():
            proc.stop()
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)
