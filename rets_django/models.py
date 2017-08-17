# coding=utf-8
from django.db import models
# from django.conf import settings
#
# import requests
# from urllib.parse import urljoin


class MoneyField(models.CharField):
    def db_type(self, connection):
        return 'money'


class Listing(models.Model):
    # Native fields
    system_id = models.IntegerField(db_column="L_ListingID",
                                    unique=True, verbose_name="SystemID")
    address = models.CharField(max_length=100, blank=True, null=True,
                               db_column="L_Address", verbose_name="Address")
    address2 = models.CharField(max_length=50, blank=True, null=True,
                                db_column="L_Address2", verbose_name="Adress 2")
    address_direction = models.CharField(max_length=2,
                                         blank=True, null=True,
                                         db_column="L_AddressDirection",
                                         verbose_name="Address Direction")
    address_number = models.CharField(max_length=15,
                                      blank=True, null=True,
                                      db_column="L_AddressNumber",
                                      verbose_name="Address Number")
    address_search_number = models.IntegerField(blank=True, null=True,
                                                db_column="L_AddressSearchNumber",
                                                verbose_name="Address Search Number")
    address_street = models.CharField(max_length=50,
                                      blank=True, null=True,
                                      db_column="L_AddressStreet",
                                      verbose_name="Address Street")
    zip_area = models.CharField(max_length=50, blank=True, null=True,
                                db_column="L_Area",
                                verbose_name="Zip/Area")
    list_price = MoneyField(max_length=15, blank=True, null=True,
                            db_column="L_AskingPrice",
                            verbose_name="List Price (H)")
    city = models.CharField(max_length=50, blank=True, null=True,
                            db_column="L_City", verbose_name="City")
    property_class = models.CharField(max_length=50, blank=True, null=True,
                                      db_column="L_Class", verbose_name="Class")
    close_of_escrow_date = models.DateField(blank=True, null=True,
                                            db_column="L_ClosingDate",
                                            verbose_name="Close of Escrow Date")
    pending_date = models.DateField(blank=True, null=True,
                                    db_column="L_ContractDate",
                                    verbose_name="Pending Date")
    dom = models.IntegerField(blank=True, null=True,
                              db_column="L_DOM", verbose_name="DOM")
    days_on_market = models.IntegerField(blank=True, null=True,
                                         db_column="L_DOMLS",
                                         verbose_name="DOMLS")
    mls_id = models.CharField(max_length=20, blank=True, null=True,
                              db_column="L_DisplayId", verbose_name="MLS #")
    first_photo_add_timestamp = models.DateTimeField(
            blank=True, null=True, db_column="L_FirstPhotoAddDt",
            verbose_name="First Photo Add Timestamp")
    how_sold = models.CharField(max_length=50, blank=True, null=True,
                                db_column="L_HowSold", verbose_name="How Sold")
    idx = models.CharField(
            max_length=100, blank=True, null=True, db_column="L_IdxInclude",
            verbose_name="IDX (Y/N)")
    list_date_received = models.DateTimeField(blank=True, null=True,
                                              db_column="L_InputDate",
                                              verbose_name="List Date Received")
    projected_cost_of_sales = MoneyField(max_length=15, blank=True, null=True,
                                         db_column="L_Keyword2",
                                         verbose_name="Proj Cost of Sales")
    projected_gross_profit = MoneyField(max_length=15, blank=True, null=True,
                                        db_column="L_Keyword3",
                                        verbose_name="Proj Gross Profit")
    projected_owner_salary = MoneyField(max_length=15, blank=True, null=True,
                                        db_column="L_Keyword4",
                                        verbose_name="Proj Owner Salary")
    projected_manager_salary = MoneyField(max_length=15, blank=True, null=True,
                                          db_column="L_Keyword5",
                                          verbose_name="Proj Manager Salary")
    projected_interest = MoneyField(max_length=15, blank=True, null=True,
                                    db_column="L_Keyword6",
                                    verbose_name="Projected Interest")
    projected_depreciation = MoneyField(max_length=15, blank=True, null=True,
                                        db_column="L_Keyword7",
                                        verbose_name="Projected Depreciation")
    projected_adjusted_net_income = MoneyField(max_length=15, blank=True,
                                               null=True,
                                               db_column="L_Keyword8",
                                               verbose_name="Proj Adjusted Net Income")
    doc_timestamp = models.DateTimeField(blank=True, null=True,
                                         db_column="L_LastDocUpdate",
                                         verbose_name="Doc Timestamp")
    photo_timestamp = models.DateTimeField(blank=True, null=True,
                                           db_column="L_Last_Photo_updt",
                                           verbose_name="PhotoTimestamp")
    listing_agent = models.ForeignKey(to='Agent', blank=True, null=True,
                                      db_column="L_ListAgent1",
                                      related_name="listing_agent",
                                      verbose_name="Listing Agent")
    colisting_agent = models.ForeignKey(to='Agent', blank=True, null=True,
                                        db_column="L_ListAgent2",
                                        related_name="colisting_agent",
                                        verbose_name="Co-Listing Agent")
    listing_office = models.ForeignKey(to='Office', blank=True, null=True,
                                       db_column="L_ListOffice1",
                                       related_name="listing_office",
                                       verbose_name="Listing Office")
    colisting_office = models.ForeignKey(to='Office', blank=True, null=True,
                                         db_column="L_ListOffice2",
                                         related_name="colisting_office",
                                         verbose_name="Co-Listing Office")
    listing_date = models.DateField(blank=True, null=True,
                                    db_column="L_ListingDate",
                                    verbose_name="Listing Date")
    listing_type = models.CharField(max_length=50, blank=True, null=True,
                                    db_column="L_Type_", verbose_name="Type")
    off_market_status_date = models.DateField(
            blank=True, null=True, db_column="L_ListingsOffMarketStatusDate",
            verbose_name="Off Market Status Date")
    lvt_date = models.DateField(blank=True, null=True, db_column="L_LvtDate",
                                verbose_name="LVT Date")
    approx_number_of_acres = models.DecimalField(
            max_digits=10, decimal_places=4, blank=True, null=True,
            db_column="L_NumAcres", verbose_name="Approx # of Acres")
    number_of_units = models.SmallIntegerField(blank=True, null=True,
                                               db_column="L_NumUnits",
                                               verbose_name="# of Units")
    original_price = MoneyField(max_length=15, blank=True, null=True,
                                db_column="L_OriginalPrice",
                                verbose_name="Original Price")
    photo_count = models.IntegerField(blank=True, null=True,
                                      db_column="L_PictureCount",
                                      verbose_name="Photo Count")
    price_per_sqft = MoneyField(max_length=15, blank=True, null=True,
                                db_column="L_PricePerSQFT",
                                verbose_name="Price Per SQFT")
    sale_or_rent = models.CharField(max_length=25, blank=True, null=True,
                                    db_column="L_SaleRent",
                                    verbose_name="Sale/Rent")
    selling_agent = models.ForeignKey(to='Agent', blank=True, null=True,
                                      db_column="L_SellingAgent1",
                                      related_name="selling_agent",
                                      verbose_name="Selling Agent")
    selling_agent_2 = models.ForeignKey(to='Agent', blank=True, null=True,
                                        db_column="L_SellingAgent2",
                                        related_name="selling_agent_2",
                                        verbose_name="Selling Agent 2")
    selling_office = models.ForeignKey(to='Office', blank=True, null=True,
                                       db_column="L_SellingOffice1",
                                       related_name="selling_office",
                                       verbose_name="Selling Office")
    selling_office_2 = models.ForeignKey(to='Office',
                                         blank=True, null=True,
                                         db_column="L_SellingOffice2",
                                         related_name="selling_office_2",
                                         verbose_name="Selling Office 2")
    sold_price = MoneyField(max_length=15, blank=True, null=True,
                            db_column="L_SoldPrice", verbose_name="Sold Price")
    state = models.CharField(max_length=2, blank=True, null=True,
                             db_column="L_State", verbose_name="State")
    status = models.CharField(max_length=15, blank=True, null=True,
                              db_column="L_Status", verbose_name="Status")
    status_category = models.CharField(max_length=50, blank=True, null=True,
                                       db_column="L_StatusCatID",
                                       verbose_name="Status Category")
    status_date = models.DateField(blank=True, null=True,
                                   db_column="L_StatusDate",
                                   verbose_name="Status Date")
    status_detail = models.IntegerField(blank=True, null=True,
                                        db_column="L_StatusID",
                                        verbose_name="Status Detail")
    search_price = MoneyField(max_length=15, blank=True, null=True,
                              db_column="L_SystemPrice",
                              verbose_name="Search Price")
    update_date = models.DateTimeField(blank=True, null=True,
                                       db_column="L_UpdateDate",
                                       verbose_name="Update Date")
    zip_code = models.CharField(max_length=20, blank=True, null=True,
                                db_column="L_Zip", verbose_name="Zip")
    asking_price_low = MoneyField(max_length=15, blank=True, null=True,
                                  db_column="L_asking_price_low",
                                  verbose_name="Price Low")
    associated_document_count = models.IntegerField(blank=True, null=True,
                                                    db_column="L_listings_associated_doc_count",
                                                    verbose_name="Associated Document Count")
    doc_manager = models.IntegerField(blank=True, null=True,
                                      db_column="L_public_documents_count",
                                      verbose_name="Doc Manager")
    walk_score = models.IntegerField(blank=True, null=True,
                                     db_column="L_walk_score",
                                     verbose_name="WalkScore")
    walk_score_link = models.URLField(blank=True, null=True,
                                      db_column="L_walk_score_source_link",
                                      verbose_name="Walk Score Link")
    # Foreign fields
    features = models.ManyToManyField(to='Feature')
    remark = models.OneToOneField(to='Remark', null=True, blank=True)
    # Non-RETS fields
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)

    @property
    def images(self):
        return Photo.objects.filter(listing=self.pk)

    def __repr__(self):
        return '<Listing: %i>' % self.system_id


class Remark(models.Model):
    county = models.CharField(max_length=100, db_column="LM_Char10_1",
                              verbose_name="County", null=True, blank=True)
    sqft_source = models.CharField(max_length=100, db_column="LM_Char10_10",
                                   verbose_name="SqFt Source", null=True,
                                   blank=True)
    stories = models.CharField(max_length=100, db_column="LM_Char10_11",
                               verbose_name="Stories", null=True, blank=True)
    interior_walls = models.CharField(max_length=100, db_column="LM_Char10_12",
                                      verbose_name="Interior Walls", null=True,
                                      blank=True)
    internet_address_field = models.CharField(max_length=100,
                                              db_column="LM_Char10_13",
                                              verbose_name="Internet Address Field",
                                              null=True, blank=True)
    boat_facilities = models.CharField(max_length=100, db_column="LM_Char10_14",
                                       verbose_name="Boat Facilities",
                                       null=True, blank=True)
    lot_size = models.CharField(max_length=100, db_column="LM_Char10_15",
                                verbose_name="Lot Size", null=True, blank=True)
    lot_size_source = models.CharField(max_length=100, db_column="LM_Char10_16",
                                       verbose_name="Lot Size Source",
                                       null=True, blank=True)
    existing_bonds = models.CharField(max_length=100, db_column="LM_Char10_18",
                                      verbose_name="Existing Bonds", null=True,
                                      blank=True)
    special_assessments = models.CharField(max_length=100,
                                           db_column="LM_Char10_19",
                                           verbose_name="Special Assessments",
                                           null=True, blank=True)
    market_area = models.CharField(max_length=100, db_column="LM_Char10_2",
                                   verbose_name="Market Area", null=True,
                                   blank=True)
    department_of_housing_3 = models.CharField(max_length=100,
                                               db_column="LM_Char10_20",
                                               verbose_name="Department of Housing 3",
                                               null=True, blank=True)
    department_of_housing_4 = models.CharField(max_length=100,
                                               db_column="LM_Char10_21",
                                               verbose_name="Department of Housing 4",
                                               null=True, blank=True)
    department_of_housing_5 = models.CharField(max_length=100,
                                               db_column="LM_Char10_22",
                                               verbose_name="Department of Housing 5",
                                               null=True, blank=True)
    fenced = models.CharField(max_length=100, db_column="LM_Char10_23",
                              verbose_name="Fenced", null=True, blank=True)
    license_2 = models.CharField(max_length=100, db_column="LM_Char10_24",
                                 verbose_name="License #2", null=True,
                                 blank=True)
    license_3 = models.CharField(max_length=100, db_column="LM_Char10_25",
                                 verbose_name="License #3", null=True,
                                 blank=True)
    license_4 = models.CharField(max_length=100, db_column="LM_Char10_26",
                                 verbose_name="License #4", null=True,
                                 blank=True)
    license_5 = models.CharField(max_length=100, db_column="LM_Char10_27",
                                 verbose_name="License #5", null=True,
                                 blank=True)
    model = models.CharField(max_length=100, db_column="LM_Char10_28",
                             verbose_name="Model", null=True, blank=True)
    make = models.CharField(max_length=100, db_column="LM_Char10_29",
                            verbose_name="Make", null=True, blank=True)
    trees_1 = models.CharField(max_length=100, db_column="LM_Char10_3",
                               verbose_name="Trees (1)", null=True, blank=True)
    serial_1 = models.CharField(max_length=100, db_column="LM_Char10_30",
                                verbose_name="Serial #1", null=True, blank=True)
    zoning = models.CharField(max_length=100, db_column="LM_Char10_4",
                              verbose_name="Zoning", null=True, blank=True)
    possible_new_zoning = models.CharField(max_length=100,
                                           db_column="LM_Char10_5",
                                           verbose_name="Possible New Zoning",
                                           null=True, blank=True)
    price_inc_lease_value = models.CharField(max_length=100,
                                             db_column="LM_Char10_6",
                                             verbose_name="Price Inc Lease Value",
                                             null=True, blank=True)
    price_include_real_estate = models.CharField(max_length=100,
                                                 db_column="LM_Char10_7",
                                                 verbose_name="Price Include Real Estate",
                                                 null=True, blank=True)
    price_includes_license = models.CharField(max_length=100,
                                              db_column="LM_Char10_9",
                                              verbose_name="Price Includes License",
                                              null=True, blank=True)
    value_range_pricing = models.CharField(max_length=100,
                                           db_column="LM_Char1_1",
                                           verbose_name="Value Range Pricing?",
                                           null=True, blank=True)
    exclusive_use_yard = models.CharField(max_length=100,
                                          db_column="LM_Char1_10",
                                          verbose_name="Exclusive Use Yard",
                                          null=True, blank=True)
    incorporated = models.CharField(max_length=100, db_column="LM_Char1_12",
                                    verbose_name="Incorporated", null=True,
                                    blank=True)
    real_estate_included = models.CharField(max_length=100,
                                            db_column="LM_Char1_13",
                                            verbose_name="Real Estate Included",
                                            null=True, blank=True)
    tax_rolls = models.CharField(max_length=100, db_column="LM_Char1_14",
                                 verbose_name="Tax Rolls", null=True,
                                 blank=True)
    variance = models.CharField(max_length=100, db_column="LM_Char1_15",
                                verbose_name="Variance", null=True, blank=True)
    paved_streets = models.CharField(max_length=100, db_column="LM_Char1_17",
                                     verbose_name="Paved Streets", null=True,
                                     blank=True)
    septic = models.CharField(max_length=100, db_column="LM_Char1_18",
                              verbose_name="Septic", null=True, blank=True)
    storm_drains = models.CharField(max_length=100, db_column="LM_Char1_19",
                                    verbose_name="Storm Drains", null=True,
                                    blank=True)
    entry_only = models.CharField(max_length=100, db_column="LM_Char1_3",
                                  verbose_name="Entry Only", null=True,
                                  blank=True)
    vacation_rental_by_owner = models.CharField(max_length=100,
                                                db_column="LM_Char1_4",
                                                verbose_name="Vacation Rental By Owner",
                                                null=True, blank=True)
    short_sale = models.CharField(max_length=100, db_column="LM_Char1_5",
                                  verbose_name="Short Sale", null=True,
                                  blank=True)
    internet_syndication_yn = models.CharField(max_length=100,
                                               db_column="LM_Char1_6",
                                               verbose_name="Internet Syndication Y/N",
                                               null=True, blank=True)
    sign_on_property = models.CharField(max_length=100, db_column="LM_Char1_7",
                                        verbose_name="Sign on Property",
                                        null=True, blank=True)
    elevator = models.CharField(max_length=100, db_column="LM_Char1_8",
                                verbose_name="Elevator", null=True, blank=True)
    entry_3_steps_to_entry = models.CharField(max_length=100,
                                              db_column="LM_Char1_9",
                                              verbose_name="Entry: 3+ Steps to Entry",
                                              null=True, blank=True)
    assessors_parcel = models.CharField(max_length=100, db_column="LM_char25_1",
                                        verbose_name="Assessors Parcel #",
                                        null=True, blank=True)
    year_2 = models.CharField(max_length=100, db_column="LM_char25_10",
                              verbose_name="Year (2)", null=True, blank=True)
    map_coordinates = models.CharField(max_length=100, db_column="LM_char25_11",
                                       verbose_name="Map Coordinates",
                                       null=True, blank=True)
    list_firm_code = models.CharField(max_length=100, db_column="LM_char25_12",
                                      verbose_name="List Firm Code", null=True,
                                      blank=True)
    actual_other_income = models.CharField(max_length=100,
                                           db_column="LM_char25_14",
                                           verbose_name="Actual Other Income",
                                           null=True, blank=True)
    act_vacancy_credit_loss = models.CharField(max_length=100,
                                               db_column="LM_char25_15",
                                               verbose_name="Act. Vacancy&Credit Loss",
                                               null=True, blank=True)
    actual_gross_oper_income = models.CharField(max_length=100,
                                                db_column="LM_char25_16",
                                                verbose_name="Actual Gross Oper Income",
                                                null=True, blank=True)
    actual_operating_expense = models.CharField(max_length=100,
                                                db_column="LM_char25_17",
                                                verbose_name="Actual Operating Expense",
                                                null=True, blank=True)
    present_loan = models.CharField(max_length=100, db_column="LM_char25_18",
                                    verbose_name="Present Loan", null=True,
                                    blank=True)
    down_payment = models.CharField(max_length=100, db_column="LM_char25_19",
                                    verbose_name="Down Payment", null=True,
                                    blank=True)
    age_4 = models.CharField(max_length=100, db_column="LM_char25_2",
                             verbose_name="Age 4", null=True, blank=True)
    have = models.CharField(max_length=100, db_column="LM_char25_20",
                            verbose_name="Have", null=True, blank=True)
    type_of_land = models.CharField(max_length=100, db_column="LM_char25_21",
                                    verbose_name="Type of Land", null=True,
                                    blank=True)
    tract_name = models.CharField(max_length=100, db_column="LM_char25_22",
                                  verbose_name="Tract Name", null=True,
                                  blank=True)
    land_use_1 = models.CharField(max_length=100, db_column="LM_char25_23",
                                  verbose_name="Land Use (1)", null=True,
                                  blank=True)
    land_use_2 = models.CharField(max_length=100, db_column="LM_char25_24",
                                  verbose_name="Land Use (2)", null=True,
                                  blank=True)
    land_use_3 = models.CharField(max_length=100, db_column="LM_char25_25",
                                  verbose_name="Land Use (3)", null=True,
                                  blank=True)
    land_use_4 = models.CharField(max_length=100, db_column="LM_char25_26",
                                  verbose_name="Land Use (4)", null=True,
                                  blank=True)
    land_use_5 = models.CharField(max_length=100, db_column="LM_char25_27",
                                  verbose_name="Land Use (5)", null=True,
                                  blank=True)
    age_1 = models.CharField(max_length=100, db_column="LM_char25_28",
                             verbose_name="Age 1", null=True, blank=True)
    age_2 = models.CharField(max_length=100, db_column="LM_char25_29",
                             verbose_name="Age 2", null=True, blank=True)
    age_5 = models.CharField(max_length=100, db_column="LM_char25_3",
                             verbose_name="Age 5", null=True, blank=True)
    age_3 = models.CharField(max_length=100, db_column="LM_char25_30",
                             verbose_name="Age 3", null=True, blank=True)
    lot_dimensions_approx = models.CharField(max_length=100,
                                             db_column="LM_char25_4",
                                             verbose_name="Lot Dimensions Approx",
                                             null=True, blank=True)
    actual_cash_on_cash = models.CharField(max_length=100,
                                           db_column="LM_char25_5",
                                           verbose_name="Actual Cash on Cash",
                                           null=True, blank=True)
    gross_multiplier = models.CharField(max_length=100, db_column="LM_char25_6",
                                        verbose_name="Gross Multiplier",
                                        null=True, blank=True)
    actual_total_pi_pay = models.CharField(max_length=100,
                                           db_column="LM_char25_7",
                                           verbose_name="Actual Total P&I Pay",
                                           null=True, blank=True)
    actual_cash_flow = models.CharField(max_length=100, db_column="LM_char25_8",
                                        verbose_name="Actual Cash Flow",
                                        null=True, blank=True)
    year_1 = models.CharField(max_length=100, db_column="LM_char25_9",
                              verbose_name="Year (1)", null=True, blank=True)
    distance_to_phone = models.CharField(max_length=100,
                                         db_column="LM_char50_1",
                                         verbose_name="Distance to Phone",
                                         null=True, blank=True)
    expense_stops = models.CharField(max_length=100, db_column="LM_char50_2",
                                     verbose_name="Expense Stops", null=True,
                                     blank=True)
    distance_to_elec = models.CharField(max_length=100, db_column="LM_char50_3",
                                        verbose_name="Distance to Elec",
                                        null=True, blank=True)
    tax_parcel = models.CharField(max_length=100, db_column="LM_char50_4",
                                  verbose_name="Tax Parcel", null=True,
                                  blank=True)
    buildings = models.CharField(max_length=100, db_column="LM_Char50_5",
                                 verbose_name="Buildings", null=True,
                                 blank=True)
    date_available = models.DateTimeField(db_column="LM_DateTime_1",
                                          verbose_name="Date Available",
                                          null=True, blank=True)
    remodel_date = models.DateTimeField(db_column="LM_DateTime_2",
                                        verbose_name="Remodel Date", null=True,
                                        blank=True)
    lease_expires = models.DateTimeField(db_column="LM_DateTime_6",
                                         verbose_name="Lease Expires",
                                         null=True, blank=True)
    lpsqft = models.DecimalField(db_column="LM_Dec_1", max_digits=15,
                                 decimal_places=2,
                                 verbose_name="Price per Square Foot",
                                 null=True, blank=True)
    cap_rate_actual = models.DecimalField(max_digits=15, decimal_places=2,
                                          db_column="LM_Dec_10",
                                          verbose_name="Cap Rate Actual",
                                          null=True, blank=True)
    splp = models.DecimalField(db_column="LM_Dec_11", max_digits=15,
                               decimal_places=2, verbose_name="SP$/LP$",
                               null=True, blank=True)
    spsqft = models.DecimalField(db_column="LM_Dec_12", max_digits=15,
                                 decimal_places=2, verbose_name="SP$/SqFt",
                                 null=True, blank=True)
    proj_other_annual_expense = models.DecimalField(db_column="LM_Dec_13",
                                                    max_digits=15,
                                                    decimal_places=0,
                                                    verbose_name="Proj Other Annual Expense",
                                                    null=True, blank=True)
    cap_rate_projected = models.DecimalField(db_column="LM_Dec_14",
                                             max_digits=15, decimal_places=2,
                                             verbose_name="Cap Rate Projected",
                                             null=True, blank=True)
    acres_1 = models.DecimalField(db_column="LM_Dec_15", max_digits=15,
                                  decimal_places=4, verbose_name="Acres 1",
                                  null=True, blank=True)
    acres_2 = models.DecimalField(db_column="LM_Dec_16", max_digits=15,
                                  decimal_places=4, verbose_name="Acres 2",
                                  null=True, blank=True)
    acres_3 = models.DecimalField(db_column="LM_Dec_17", max_digits=15,
                                  decimal_places=4, verbose_name="Acres 3",
                                  null=True, blank=True)
    acres_4 = models.DecimalField(db_column="LM_Dec_18", max_digits=15,
                                  decimal_places=4, verbose_name="Acres 4",
                                  null=True, blank=True)
    acres_5 = models.DecimalField(db_column="LM_Dec_19", max_digits=15,
                                  decimal_places=4, verbose_name="Acres 5",
                                  null=True, blank=True)
    act_equipment_rental_exp = models.DecimalField(db_column="LM_Dec_20",
                                                   max_digits=15,
                                                   decimal_places=0,
                                                   verbose_name="Act. Equipment Rental Exp",
                                                   null=True, blank=True)
    actual_repairs_expense = models.DecimalField(db_column="LM_Dec_21",
                                                 max_digits=15,
                                                 decimal_places=0,
                                                 verbose_name="Actual Repairs Expense",
                                                 null=True, blank=True)
    actual_payroll_expense = models.DecimalField(db_column="LM_Dec_22",
                                                 max_digits=15,
                                                 decimal_places=0,
                                                 verbose_name="Actual Payroll Expense",
                                                 null=True, blank=True)
    actual_payroll_tax = models.DecimalField(db_column="LM_Dec_23",
                                             max_digits=15, decimal_places=0,
                                             verbose_name="Actual Payroll Tax",
                                             null=True, blank=True)
    actual_annual_other_exp = models.DecimalField(db_column="LM_Dec_24",
                                                  max_digits=15,
                                                  decimal_places=0,
                                                  verbose_name="Actual Annual Other Exp.",
                                                  null=True, blank=True)
    projected_rent_expense = models.DecimalField(db_column="LM_Dec_25",
                                                 max_digits=15,
                                                 decimal_places=0,
                                                 verbose_name="Projected Rent Expense",
                                                 null=True, blank=True)
    proj_utilities_expense = models.DecimalField(db_column="LM_Dec_26",
                                                 max_digits=15,
                                                 decimal_places=0,
                                                 verbose_name="Proj Utilities Expense",
                                                 null=True, blank=True)
    proj_expense_insadv = models.DecimalField(db_column="LM_Dec_27",
                                              max_digits=15, decimal_places=0,
                                              verbose_name="Proj Expense Ins/Adv",
                                              null=True, blank=True)
    proj_accounting_expense = models.DecimalField(db_column="LM_Dec_28",
                                                  max_digits=15,
                                                  decimal_places=0,
                                                  verbose_name="Proj Accounting Expense",
                                                  null=True, blank=True)
    proj_phone_expense = models.DecimalField(db_column="LM_Dec_29",
                                             max_digits=15, decimal_places=0,
                                             verbose_name="Proj Phone Expense",
                                             null=True, blank=True)
    price_per_acre = models.DecimalField(db_column="LM_Dec_3", max_digits=15,
                                         decimal_places=0,
                                         verbose_name="Price Per Acre",
                                         null=True, blank=True)
    proj_equipment_expense = models.DecimalField(db_column="LM_Dec_30",
                                                 max_digits=15,
                                                 decimal_places=0,
                                                 verbose_name="Proj Equipment Expense",
                                                 null=True, blank=True)
    proj_payroll_expense = models.DecimalField(db_column="LM_Dec_4",
                                               max_digits=15, decimal_places=0,
                                               verbose_name="Proj Payroll Expense",
                                               null=True, blank=True)
    proj_payroll_tax = models.DecimalField(db_column="LM_Dec_5", max_digits=15,
                                           decimal_places=0,
                                           verbose_name="Proj Payroll Tax",
                                           null=True, blank=True)
    actual_adjusted_net_inc = models.DecimalField(db_column="LM_Dec_6",
                                                  max_digits=15,
                                                  decimal_places=0,
                                                  verbose_name="Actual Adjusted Net Inc",
                                                  null=True, blank=True)
    actual_gross_schd_income = models.DecimalField(db_column="LM_Dec_7",
                                                   max_digits=15,
                                                   decimal_places=0,
                                                   verbose_name="Actual Gross Schd Income",
                                                   null=True, blank=True)
    proj_gross_sales = models.DecimalField(db_column="LM_Dec_8", max_digits=15,
                                           decimal_places=0,
                                           verbose_name="Proj Gross Sales",
                                           null=True, blank=True)
    price_per_sqft = models.DecimalField(db_column="LM_Dec_9", max_digits=15,
                                         decimal_places=0,
                                         verbose_name="Price per SqFt",
                                         null=True, blank=True)
    num_of_buildings = models.IntegerField(db_column="LM_Int1_1",
                                           verbose_name="# of Buildings",
                                           null=True,
                                           blank=True)
    land = models.IntegerField(db_column="LM_Int1_10", verbose_name="Land %",
                               null=True, blank=True)
    improvements = models.IntegerField(db_column="LM_Int1_11",
                                       verbose_name="Improvements %", null=True,
                                       blank=True)
    personal_property = models.IntegerField(db_column="LM_Int1_12",
                                            verbose_name="Personal Property %",
                                            null=True, blank=True)
    grade = models.IntegerField(db_column="LM_Int1_13", verbose_name="% Grade",
                                null=True, blank=True)
    unit_3_total_baths = models.IntegerField(db_column="LM_Int1_14",
                                             verbose_name="Unit 3 # Total Baths",
                                             null=True, blank=True)
    total_useable = models.IntegerField(db_column="LM_Int1_15",
                                        verbose_name="Total Useable %",
                                        null=True, blank=True)
    units_wdishwashers = models.IntegerField(db_column="LM_Int1_16",
                                             verbose_name="# Units w/Dishwashers",
                                             null=True, blank=True)
    num_of_bedrooms_9 = models.IntegerField(db_column="LM_Int1_17",
                                            verbose_name="# of Bedrooms",
                                            null=True, blank=True)
    num_of_bedrooms_10 = models.IntegerField(db_column="LM_Int1_18",
                                             verbose_name="# of Bedrooms",
                                             null=True, blank=True)
    restrooms = models.IntegerField(db_column="LM_Int1_2",
                                    verbose_name="Restrooms", null=True,
                                    blank=True)
    num_of_bedrooms_5 = models.IntegerField(db_column="LM_Int1_20",
                                            verbose_name="# of Bedrooms",
                                            null=True, blank=True)
    common_restrooms = models.IntegerField(db_column="LM_Int1_3",
                                           verbose_name="Common Restrooms",
                                           null=True, blank=True)
    private_restrooms = models.IntegerField(db_column="LM_Int1_4",
                                            verbose_name="Private Restrooms",
                                            null=True, blank=True)
    occupancy = models.IntegerField(db_column="LM_Int1_5",
                                    verbose_name="Occupancy %", null=True,
                                    blank=True)
    overall_vacant = models.IntegerField(db_column="LM_Int1_6",
                                         verbose_name="Overall % Vacant",
                                         null=True, blank=True)
    num_of_stories = models.IntegerField(db_column="LM_Int1_7",
                                         verbose_name="# of Stories", null=True,
                                         blank=True)
    fireplaces = models.IntegerField(db_column="LM_Int1_8",
                                     verbose_name="Fireplaces", null=True,
                                     blank=True)
    year_built = models.IntegerField(db_column="LM_Int2_1",
                                     verbose_name="Year Built", null=True,
                                     blank=True)
    monthly_rate_1 = models.IntegerField(db_column="LM_Int2_10",
                                         verbose_name="Monthly Rate (1)",
                                         null=True, blank=True)
    monthly_rate_2 = models.IntegerField(db_column="LM_Int2_11",
                                         verbose_name="Monthly Rate (2)",
                                         null=True, blank=True)
    num_of_units_6 = models.IntegerField(db_column="LM_Int2_12",
                                         verbose_name="# of Units (6)",
                                         null=True,
                                         blank=True)
    monthly_rate_3 = models.IntegerField(db_column="LM_Int2_13",
                                         verbose_name="Monthly Rate (3)",
                                         null=True, blank=True)
    num_of_units_8 = models.IntegerField(db_column="LM_Int2_14",
                                         verbose_name="# of Units (8)",
                                         null=True,
                                         blank=True)
    num_of_units_9 = models.IntegerField(db_column="LM_Int2_15",
                                         verbose_name="# of Units (9)",
                                         null=True,
                                         blank=True)
    num_of_units_10 = models.IntegerField(db_column="LM_Int2_16",
                                          verbose_name="# of Units (10)",
                                          null=True,
                                          blank=True)
    num_of_units_1 = models.IntegerField(db_column="LM_Int2_17",
                                         verbose_name="# of Units (1)",
                                         null=True,
                                         blank=True)
    num_of_units_2 = models.IntegerField(db_column="LM_Int2_18",
                                         verbose_name="# of Units (2)",
                                         null=True,
                                         blank=True)
    num_of_units_3 = models.IntegerField(db_column="LM_Int2_19",
                                         verbose_name="# of Units (3)",
                                         null=True,
                                         blank=True)
    num_of_leased_apartments = models.IntegerField(db_column="LM_Int2_2",
                                                   verbose_name="# of Leased Apartments",
                                                   null=True, blank=True)
    num_of_units_4 = models.IntegerField(db_column="LM_Int2_20",
                                         verbose_name="# of Units (4)",
                                         null=True,
                                         blank=True)
    full_time_employees = models.IntegerField(db_column="LM_Int2_3",
                                              verbose_name="Full Time Employees",
                                              null=True, blank=True)
    average_room_days_per_yr = models.IntegerField(db_column="LM_Int2_4",
                                                   verbose_name="Average Room Days per Yr",
                                                   null=True, blank=True)
    sections = models.IntegerField(db_column="LM_Int2_5",
                                   verbose_name="# Sections", null=True,
                                   blank=True)
    bath_totals = models.IntegerField(db_column="LM_Int2_6",
                                      verbose_name="Bath Totals", null=True,
                                      blank=True)
    part_time_employees = models.IntegerField(db_column="LM_Int2_7",
                                              verbose_name="Part Time Employees",
                                              null=True, blank=True)
    num_of_spaces_2 = models.IntegerField(db_column="LM_Int2_8",
                                          verbose_name="# of Spaces (2)",
                                          null=True,
                                          blank=True)
    num_of_spaces_3 = models.IntegerField(db_column="LM_Int2_9",
                                          verbose_name="# of Spaces (3)",
                                          null=True,
                                          blank=True)
    actual_depreciation = models.IntegerField(db_column="LM_Int4_1",
                                              verbose_name="Actual Depreciation",
                                              null=True, blank=True)
    actual_gross_profit = models.IntegerField(db_column="LM_Int4_10",
                                              verbose_name="Actual Gross Profit",
                                              null=True, blank=True)
    max_search_price = models.IntegerField(db_column="LM_Int4_13",
                                           verbose_name="Max Search Price",
                                           null=True, blank=True)
    original_low_list_price = models.IntegerField(db_column="LM_Int4_14",
                                                  verbose_name="Original Low List Price",
                                                  null=True, blank=True)
    mt = models.IntegerField(db_column="LM_Int4_15", verbose_name="MT",
                             null=True, blank=True)
    tax_rate = models.IntegerField(db_column="LM_Int4_16",
                                   verbose_name="Tax Rate", null=True,
                                   blank=True)
    actual_interest = models.IntegerField(db_column="LM_Int4_17",
                                          verbose_name="Actual Interest",
                                          null=True, blank=True)
    tax_area = models.IntegerField(db_column="LM_Int4_18",
                                   verbose_name="Tax Area", null=True,
                                   blank=True)
    assumable_finance = models.IntegerField(db_column="LM_Int4_20",
                                            verbose_name="Assumable Finance",
                                            null=True, blank=True)
    actual_owner_salary = models.IntegerField(db_column="LM_Int4_3",
                                              verbose_name="Actual Owner Salary",
                                              null=True, blank=True)
    age = models.IntegerField(db_column="LM_Int4_4", verbose_name="Age",
                              null=True, blank=True)
    lease_deposit = models.IntegerField(db_column="LM_Int4_5",
                                        verbose_name="Lease Deposit", null=True,
                                        blank=True)
    lot_sqft_approx = models.IntegerField(db_column="LM_Int4_6",
                                          verbose_name="Lot SqFt Approx",
                                          null=True, blank=True)
    parking_garage_spaces = models.IntegerField(db_column="LM_Int4_7",
                                                verbose_name="Parking Garage Spaces",
                                                null=True, blank=True)
    parking_spaces_total = models.IntegerField(db_column="LM_Int4_8",
                                               verbose_name="Parking Spaces Total",
                                               null=True, blank=True)
    actual_cost_of_sales = models.IntegerField(db_column="LM_Int4_9",
                                               verbose_name="Actual Cost of Sales",
                                               null=True, blank=True)
    land_lease_purchase_yn = models.NullBooleanField(db_column="LM_bit_8",
                                                     verbose_name="Land Lease Purchase YN")
    mandatory_remarks_for_vrp = models.CharField(max_length=100,
                                                 db_column="LM_Char100_1",
                                                 verbose_name="Mandatory Remarks for VRP",
                                                 null=True, blank=True)
    unit_size_6 = models.CharField(max_length=100, db_column="LM_Char100_10",
                                   verbose_name="Unit Size (6)", null=True,
                                   blank=True)
    mandatory_rmks_1strgt_rfs = models.CharField(max_length=100,
                                                 db_column="LM_Char100_2",
                                                 verbose_name="Mandatory Rmks 1stRgt Rfs",
                                                 null=True, blank=True)
    variance_comments = models.CharField(max_length=100,
                                         db_column="LM_Char100_3",
                                         verbose_name="Variance Comments",
                                         null=True, blank=True)
    lease_expires_9 = models.CharField(max_length=100, db_column="LM_Char100_4",
                                       verbose_name="Lease Expires (9)",
                                       null=True, blank=True)
    list_agent_fax = models.CharField(max_length=100, db_column="LM_Char100_5",
                                      verbose_name="List Agent Fax", null=True,
                                      blank=True)
    internet_address = models.CharField(max_length=100,
                                        db_column="LM_Char100_7",
                                        verbose_name="Internet Address",
                                        null=True, blank=True)
    unit_size_10 = models.CharField(max_length=100, db_column="LM_Char100_8",
                                    verbose_name="Unit Size (10)", null=True,
                                    blank=True)
    lease_expires_10 = models.CharField(max_length=100,
                                        db_column="LM_Char100_9",
                                        verbose_name="Lease Expires (10)",
                                        null=True, blank=True)
    serial_2 = models.CharField(max_length=100, db_column="LM_Char10_31",
                                verbose_name="Serial #2", null=True, blank=True)
    serial_3 = models.CharField(max_length=100, db_column="LM_Char10_32",
                                verbose_name="Serial #3", null=True, blank=True)
    serial_4 = models.CharField(max_length=100, db_column="LM_Char10_33",
                                verbose_name="Serial #4", null=True, blank=True)
    serial_5 = models.CharField(max_length=100, db_column="LM_Char10_34",
                                verbose_name="Serial #5", null=True, blank=True)
    financing = models.CharField(max_length=100, db_column="LM_char10_37",
                                 verbose_name="Financing", null=True,
                                 blank=True)
    unit_number_1 = models.CharField(max_length=100, db_column="LM_Char10_38",
                                     verbose_name="Unit Number (1)", null=True,
                                     blank=True)
    unit_number_2 = models.CharField(max_length=100, db_column="LM_Char10_39",
                                     verbose_name="Unit Number (2)", null=True,
                                     blank=True)
    unit_number_3 = models.CharField(max_length=100, db_column="LM_Char10_40",
                                     verbose_name="Unit Number (3)", null=True,
                                     blank=True)
    unit_number_4 = models.CharField(max_length=100, db_column="LM_Char10_41",
                                     verbose_name="Unit Number (4)", null=True,
                                     blank=True)
    unit_number_5 = models.CharField(max_length=100, db_column="LM_Char10_42",
                                     verbose_name="Unit Number (5)", null=True,
                                     blank=True)
    other_income_source_2 = models.CharField(max_length=100,
                                             db_column="LM_Char10_43",
                                             verbose_name="Other Income Source 2",
                                             null=True, blank=True)
    other_income_amount = models.CharField(max_length=100,
                                           db_column="LM_Char10_44",
                                           verbose_name="Other Income Amount",
                                           null=True, blank=True)
    bln_year_due = models.CharField(max_length=100, db_column="LM_Char10_45",
                                    verbose_name="BLN Year Due", null=True,
                                    blank=True)
    flood_zone = models.CharField(max_length=100, db_column="LM_Char10_46",
                                  verbose_name="Flood Zone", null=True,
                                  blank=True)
    geological_hazard_zone = models.CharField(max_length=100,
                                              db_column="LM_Char10_47",
                                              verbose_name="Geological Hazard Zone",
                                              null=True, blank=True)
    list_agent_bre_license = models.CharField(max_length=100,
                                              db_column="LM_Char10_48",
                                              verbose_name="List Agent BRE License #",
                                              null=True, blank=True)
    other_income_source = models.CharField(max_length=100,
                                           db_column="LM_Char10_49",
                                           verbose_name="Other Income Source",
                                           null=True, blank=True)
    price_per_spaces = models.CharField(max_length=100,
                                        db_column="LM_char10_50",
                                        verbose_name="Price/Spaces", null=True,
                                        blank=True)
    minimum_lease_terms_1 = models.CharField(max_length=100,
                                             db_column="LM_Char10_51",
                                             verbose_name="Minimum Lease Terms (1)",
                                             null=True, blank=True)
    minimum_lease_terms_2 = models.CharField(max_length=100,
                                             db_column="LM_Char10_52",
                                             verbose_name="Minimum Lease Terms (2)",
                                             null=True, blank=True)
    minimum_lease_terms_3 = models.CharField(max_length=100,
                                             db_column="LM_Char10_53",
                                             verbose_name="Minimum Lease Terms (3)",
                                             null=True, blank=True)
    minimum_lease_terms_4 = models.CharField(max_length=100,
                                             db_column="LM_Char10_54",
                                             verbose_name="Minimum Lease Terms (4)",
                                             null=True, blank=True)
    minimum_lease_terms_5 = models.CharField(max_length=100,
                                             db_column="LM_Char10_55",
                                             verbose_name="Minimum Lease Terms (5)",
                                             null=True, blank=True)
    minimum_lease_terms_6 = models.CharField(max_length=100,
                                             db_column="LM_Char10_56",
                                             verbose_name="Minimum Lease Terms (6)",
                                             null=True, blank=True)
    minimum_lease_terms_7 = models.CharField(max_length=100,
                                             db_column="LM_Char10_57",
                                             verbose_name="Minimum Lease Terms (7)",
                                             null=True, blank=True)
    minimum_lease_terms_8 = models.CharField(max_length=100,
                                             db_column="LM_Char10_58",
                                             verbose_name="Minimum Lease Terms (8)",
                                             null=True, blank=True)
    minimum_lease_terms_9 = models.CharField(max_length=100,
                                             db_column="LM_Char10_59",
                                             verbose_name="Minimum Lease Terms (9)",
                                             null=True, blank=True)
    minimum_lease_terms_10 = models.CharField(max_length=100,
                                              db_column="LM_Char10_60",
                                              verbose_name="Minimum Lease Terms (10)",
                                              null=True, blank=True)
    common_area_maintenance = models.CharField(max_length=100,
                                               db_column="LM_Char10_61",
                                               verbose_name="Common Area Maintenance",
                                               null=True, blank=True)
    floor_load = models.CharField(max_length=100, db_column="LM_Char10_62",
                                  verbose_name="Floor Load", null=True,
                                  blank=True)
    alley_access = models.CharField(max_length=100, db_column="LM_Char10_63",
                                    verbose_name="Alley Access", null=True,
                                    blank=True)
    sign_space = models.CharField(max_length=100, db_column="LM_Char10_64",
                                  verbose_name="Sign Space", null=True,
                                  blank=True)
    country = models.CharField(max_length=100, db_column="LM_Char10_65",
                               verbose_name="Country", null=True, blank=True)
    country_2 = models.CharField(max_length=100, db_column="LM_Char10_66",
                                 verbose_name="Country 2", null=True,
                                 blank=True)
    assets_inventory = models.CharField(max_length=100,
                                        db_column="LM_Char10_67",
                                        verbose_name="Assets Inventory",
                                        null=True, blank=True)
    owner_works = models.CharField(max_length=100, db_column="LM_Char10_68",
                                   verbose_name="Owner Works", null=True,
                                   blank=True)
    owner_train_employees = models.CharField(max_length=100,
                                             db_column="LM_Char10_69",
                                             verbose_name="Owner Train Employees",
                                             null=True, blank=True)
    price_includes_goodwill = models.CharField(max_length=100,
                                               db_column="LM_Char10_70",
                                               verbose_name="Price Includes Goodwill",
                                               null=True, blank=True)
    showing_contact_type = models.CharField(max_length=100,
                                            db_column="LM_Char10_71",
                                            verbose_name="Showing Contact Type",
                                            null=True, blank=True)
    year_built_source = models.CharField(max_length=100,
                                         db_column="LM_Char10_72",
                                         verbose_name="Year Built Source",
                                         null=True, blank=True)
    originating_system_name = models.CharField(max_length=100,
                                               db_column="LM_Char10_75",
                                               verbose_name="Originating System Name",
                                               null=True, blank=True)
    previous_standard_status = models.CharField(max_length=100,
                                                db_column="LM_Char10_77",
                                                verbose_name="Previous Standard Status",
                                                null=True, blank=True)
    major_change_type = models.CharField(max_length=100,
                                         db_column="LM_Char10_78",
                                         verbose_name="Major Change Type",
                                         null=True, blank=True)
    tract_number = models.CharField(max_length=100, db_column="LM_Char10_81",
                                    verbose_name="Tract Number", null=True,
                                    blank=True)
    sidewalkscurbs = models.CharField(max_length=100, db_column="LM_char1_23",
                                      verbose_name="Sidewalks/Curbs", null=True,
                                      blank=True)
    land_fee = models.CharField(max_length=100, db_column="LM_Char1_24",
                                verbose_name="Land Fee", null=True, blank=True)
    land_lease = models.CharField(max_length=100, db_column="LM_Char1_25",
                                  verbose_name="Land Lease", null=True,
                                  blank=True)
    monthly_lease = models.CharField(max_length=100, db_column="LM_Char1_26",
                                     verbose_name="Monthly Lease", null=True,
                                     blank=True)
    yearly_lease = models.CharField(max_length=100, db_column="LM_Char1_27",
                                    verbose_name="Yearly Lease", null=True,
                                    blank=True)
    easements = models.CharField(max_length=100, db_column="LM_char1_28",
                                 verbose_name="Easements", null=True,
                                 blank=True)
    easement_fee = models.CharField(max_length=100, db_column="LM_Char1_29",
                                    verbose_name="Easement Fee", null=True,
                                    blank=True)
    cleared = models.CharField(max_length=100, db_column="LM_char1_30",
                               verbose_name="Cleared", null=True, blank=True)
    mineral_rights = models.CharField(max_length=100, db_column="LM_Char1_31",
                                      verbose_name="Mineral Rights", null=True,
                                      blank=True)
    unit_furnished_2 = models.CharField(max_length=100, db_column="LM_Char1_32",
                                        verbose_name="Unit Furnished (2)",
                                        null=True, blank=True)
    potable = models.CharField(max_length=100, db_column="LM_char1_33",
                               verbose_name="Potable", null=True, blank=True)
    city_water = models.CharField(max_length=100, db_column="LM_Char1_34",
                                  verbose_name="City Water", null=True,
                                  blank=True)
    unit_furnished_5 = models.CharField(max_length=100, db_column="LM_Char1_35",
                                        verbose_name="Unit Furnished (5)",
                                        null=True, blank=True)
    unit_furnished_6 = models.CharField(max_length=100, db_column="LM_Char1_36",
                                        verbose_name="Unit Furnished (6)",
                                        null=True, blank=True)
    unit_furnished_7 = models.CharField(max_length=100, db_column="LM_Char1_37",
                                        verbose_name="Unit Furnished (7)",
                                        null=True, blank=True)
    unit_furnished_8 = models.CharField(max_length=100, db_column="LM_Char1_38",
                                        verbose_name="Unit Furnished (8)",
                                        null=True, blank=True)
    unit_furnished_9 = models.CharField(max_length=100, db_column="LM_Char1_39",
                                        verbose_name="Unit Furnished (9)",
                                        null=True, blank=True)
    unit_furnished_10 = models.CharField(max_length=100,
                                         db_column="LM_Char1_40",
                                         verbose_name="Unit Furnished (10)",
                                         null=True, blank=True)
    tenant_pays_gas = models.CharField(max_length=100, db_column="LM_Char1_41",
                                       verbose_name="Tenant Pays Gas",
                                       null=True, blank=True)
    tenant_pays_water = models.CharField(max_length=100,
                                         db_column="LM_Char1_42",
                                         verbose_name="Tenant Pays Water",
                                         null=True, blank=True)
    tenant_pays_electric = models.CharField(max_length=100,
                                            db_column="LM_Char1_43",
                                            verbose_name="Tenant Pays Electric",
                                            null=True, blank=True)
    manager_operated = models.CharField(max_length=100, db_column="LM_Char1_44",
                                        verbose_name="Manager Operated",
                                        null=True, blank=True)
    ownlease_bar = models.CharField(max_length=100, db_column="LM_Char1_45",
                                    verbose_name="Own/Lease Bar", null=True,
                                    blank=True)
    ownlease_other_2 = models.CharField(max_length=100, db_column="LM_Char1_46",
                                        verbose_name="Own/Lease Other 2",
                                        null=True, blank=True)
    ownlease_other_1 = models.CharField(max_length=100, db_column="LM_Char1_47",
                                        verbose_name="Own/Lease Other 1",
                                        null=True, blank=True)
    ownlease_restaurant = models.CharField(max_length=100,
                                           db_column="LM_Char1_48",
                                           verbose_name="Own/Lease Restaurant",
                                           null=True, blank=True)
    ownlease_telephone = models.CharField(max_length=100,
                                          db_column="LM_Char1_49",
                                          verbose_name="Own/Lease Telephone",
                                          null=True, blank=True)
    ownlease_vending = models.CharField(max_length=100, db_column="LM_Char1_50",
                                        verbose_name="Own/Lease Vending",
                                        null=True, blank=True)
    owner_operated = models.CharField(max_length=100, db_column="LM_Char1_51",
                                      verbose_name="Owner Operated", null=True,
                                      blank=True)
    will_manager_stay = models.CharField(max_length=100,
                                         db_column="LM_Char1_53",
                                         verbose_name="Will Manager Stay",
                                         null=True, blank=True)
    well = models.CharField(max_length=100, db_column="LM_Char1_54",
                            verbose_name="Well", null=True, blank=True)
    public_sewage_facility = models.CharField(max_length=100,
                                              db_column="LM_Char1_55",
                                              verbose_name="Public Sewage Facility",
                                              null=True, blank=True)
    private_sewage_facility = models.CharField(max_length=100,
                                               db_column="LM_Char1_56",
                                               verbose_name="Private Sewage Facility",
                                               null=True, blank=True)
    sprinkler = models.CharField(max_length=100, db_column="LM_char1_57",
                                 verbose_name="Sprinkler", null=True,
                                 blank=True)
    railroad = models.CharField(max_length=100, db_column="LM_char1_58",
                                verbose_name="Railroad", null=True, blank=True)
    truck_dock = models.CharField(max_length=100, db_column="LM_Char1_59",
                                  verbose_name="Truck Dock", null=True,
                                  blank=True)
    truck_well = models.CharField(max_length=100, db_column="LM_Char1_60",
                                  verbose_name="Truck Well", null=True,
                                  blank=True)
    price_includes_equipment = models.CharField(max_length=255,
                                                db_column="LM_char255_1",
                                                verbose_name="Price Includes Equipment",
                                                null=True, blank=True)
    tenant_improvmnt_allowance = models.CharField(max_length=255,
                                                  db_column="LM_char255_2",
                                                  verbose_name="Tenant Improvement Allowance",
                                                  null=True, blank=True)
    proj_gross_sched_income = models.CharField(max_length=100,
                                               db_column="LM_char30_1",
                                               verbose_name="Proj. Gross Sched. Income",
                                               null=True, blank=True)
    distance_to_citywater = models.CharField(max_length=100,
                                             db_column="LM_char30_10",
                                             verbose_name="Distance to City/Water",
                                             null=True, blank=True)
    distance_to_sewer = models.CharField(max_length=100,
                                         db_column="LM_char30_11",
                                         verbose_name="Distance to Sewer",
                                         null=True, blank=True)
    distance_to_shopping = models.CharField(max_length=100,
                                            db_column="LM_char30_12",
                                            verbose_name="Distance to Shopping",
                                            null=True, blank=True)
    distance_to_school = models.CharField(max_length=100,
                                          db_column="LM_char30_13",
                                          verbose_name="Distance to School",
                                          null=True, blank=True)
    distance_to_church = models.CharField(max_length=100,
                                          db_column="LM_char30_14",
                                          verbose_name="Distance to Church",
                                          null=True, blank=True)
    distance_to_freeway = models.CharField(max_length=100,
                                           db_column="LM_char30_15",
                                           verbose_name="Distance to Freeway",
                                           null=True, blank=True)
    distance_to_bus = models.CharField(max_length=100, db_column="LM_char30_16",
                                       verbose_name="Distance to Bus",
                                       null=True, blank=True)
    sewer = models.CharField(max_length=100, db_column="LM_char30_17",
                             verbose_name="Sewer", null=True, blank=True)
    lease = models.CharField(max_length=100, db_column="LM_char30_18",
                             verbose_name="Lease $", null=True, blank=True)
    year_lease_expires = models.CharField(max_length=100,
                                          db_column="LM_char30_19",
                                          verbose_name="Year Lease Expires",
                                          null=True, blank=True)
    projected_other_income = models.CharField(max_length=100,
                                              db_column="LM_char30_2",
                                              verbose_name="Projected Other Income",
                                              null=True, blank=True)
    ingressegress = models.CharField(max_length=100, db_column="LM_char30_20",
                                     verbose_name="Ingress/Egress", null=True,
                                     blank=True)
    soil_type = models.CharField(max_length=100, db_column="LM_char30_21",
                                 verbose_name="Soil Type", null=True,
                                 blank=True)
    setbacks = models.CharField(max_length=100, db_column="LM_char30_22",
                                verbose_name="Setbacks", null=True, blank=True)
    actual_other_expense = models.CharField(max_length=100,
                                            db_column="LM_char30_23",
                                            verbose_name="Actual Other Expense",
                                            null=True, blank=True)
    actual_total_expense = models.CharField(max_length=100,
                                            db_column="LM_char30_24",
                                            verbose_name="Actual Total Expense",
                                            null=True, blank=True)
    projected_taxes_expense = models.CharField(max_length=100,
                                               db_column="LM_char30_25",
                                               verbose_name="Projected Taxes Expense",
                                               null=True, blank=True)
    projected_fl_ins_expense = models.CharField(max_length=100,
                                                db_column="LM_char30_26",
                                                verbose_name="Projected F&L Ins Expense",
                                                null=True, blank=True)
    projected_gas_electric = models.CharField(max_length=100,
                                              db_column="LM_char30_27",
                                              verbose_name="Projected Gas & Electric",
                                              null=True, blank=True)
    proj_wtrsewer_expense = models.CharField(max_length=100,
                                             db_column="LM_char30_28",
                                             verbose_name="Proj Wtr/Sewer Expense",
                                             null=True, blank=True)
    projected_trash_expense = models.CharField(max_length=100,
                                               db_column="LM_char30_29",
                                               verbose_name="Projected Trash Expense",
                                               null=True, blank=True)
    proj_vacancy_credit_los = models.CharField(max_length=100,
                                               db_column="LM_char30_3",
                                               verbose_name="Proj Vacancy & Credit Los",
                                               null=True, blank=True)
    number_of_wells = models.CharField(max_length=100, db_column="LM_char30_30",
                                       verbose_name="Number of Wells",
                                       null=True, blank=True)
    proj_gross_operating_inc = models.CharField(max_length=100,
                                                db_column="LM_char30_4",
                                                verbose_name="Proj Gross Operating Inc",
                                                null=True, blank=True)
    proj_operating_expense = models.CharField(max_length=100,
                                              db_column="LM_char30_5",
                                              verbose_name="Proj Operating Expense",
                                              null=True, blank=True)
    projected_net_income = models.CharField(max_length=100,
                                            db_column="LM_char30_6",
                                            verbose_name="Projected Net Income",
                                            null=True, blank=True)
    proj_annual_p_i_expense = models.CharField(max_length=100,
                                               db_column="LM_char30_7",
                                               verbose_name="Proj Annual P & I Expense",
                                               null=True, blank=True)
    projected_cash_flow = models.CharField(max_length=100,
                                           db_column="LM_char30_8",
                                           verbose_name="Projected Cash Flow",
                                           null=True, blank=True)
    projected_cash_on_cash = models.CharField(max_length=100,
                                              db_column="LM_char30_9",
                                              verbose_name="Projected Cash on Cash",
                                              null=True, blank=True)
    projected_license_expense = models.CharField(max_length=100,
                                                 db_column="LM_char50_10",
                                                 verbose_name="Projected License Expense",
                                                 null=True, blank=True)
    proj_gardener_expense = models.CharField(max_length=100,
                                             db_column="LM_char50_11",
                                             verbose_name="Proj Gardener Expense",
                                             null=True, blank=True)
    projected_manager_expense = models.CharField(max_length=100,
                                                 db_column="LM_char50_12",
                                                 verbose_name="Projected Manager Expense",
                                                 null=True, blank=True)
    proj_prop_management_exp = models.CharField(max_length=100,
                                                db_column="LM_char50_13",
                                                verbose_name="Proj Prop Management Exp",
                                                null=True, blank=True)
    projected_other_expense = models.CharField(max_length=100,
                                               db_column="LM_char50_14",
                                               verbose_name="Projected Other Expense",
                                               null=True, blank=True)
    projected_total_expense = models.CharField(max_length=100,
                                               db_column="LM_char50_15",
                                               verbose_name="Projected Total Expense",
                                               null=True, blank=True)
    income_year_1 = models.CharField(max_length=100, db_column="LM_char50_16",
                                     verbose_name="Income Year (1)", null=True,
                                     blank=True)
    first_loan_balance = models.CharField(max_length=100,
                                          db_column="LM_char50_17",
                                          verbose_name="1st Loan Balance",
                                          null=True, blank=True)
    loan_1_payment = models.CharField(max_length=100, db_column="LM_char50_18",
                                      verbose_name="Loan 1 Payment", null=True,
                                      blank=True)
    first_loan_interest = models.CharField(max_length=100,
                                           db_column="LM_char50_19",
                                           verbose_name="1st Loan Interest",
                                           null=True, blank=True)
    loan_1_balloon = models.CharField(max_length=100, db_column="LM_char50_20",
                                      verbose_name="Loan 1 Balloon", null=True,
                                      blank=True)
    loan_1_year_due = models.CharField(max_length=100, db_column="LM_char50_21",
                                       verbose_name="Loan 1 Year Due",
                                       null=True, blank=True)
    loan_2_balance = models.CharField(max_length=100, db_column="LM_char50_22",
                                      verbose_name="Loan 2 Balance", null=True,
                                      blank=True)
    loan_2_payment = models.CharField(max_length=100, db_column="LM_char50_23",
                                      verbose_name="Loan 2 Payment", null=True,
                                      blank=True)
    second_loan_interest_rate = models.CharField(max_length=100,
                                                 db_column="LM_char50_24",
                                                 verbose_name="2nd Loan Interest Rate",
                                                 null=True, blank=True)
    loan_2_balloon = models.CharField(max_length=100, db_column="LM_char50_25",
                                      verbose_name="Loan 2 Balloon", null=True,
                                      blank=True)
    loan_2_year_due = models.CharField(max_length=100, db_column="LM_char50_26",
                                       verbose_name="Loan 2 Year Due",
                                       null=True, blank=True)
    bln_balance = models.CharField(max_length=100, db_column="LM_char50_27",
                                   verbose_name="BLN Balance", null=True,
                                   blank=True)
    bln_payment = models.CharField(max_length=100, db_column="LM_char50_28",
                                   verbose_name="BLN Payment", null=True,
                                   blank=True)
    bln_interest = models.CharField(max_length=100, db_column="LM_char50_29",
                                    verbose_name="BLN Interest", null=True,
                                    blank=True)
    bln_balloon = models.CharField(max_length=100, db_column="LM_char50_30",
                                   verbose_name="BLN Balloon", null=True,
                                   blank=True)
    show_phone = models.CharField(max_length=100, db_column="LM_char50_31",
                                  verbose_name="Show Phone", null=True,
                                  blank=True)
    income_year_2 = models.CharField(max_length=100, db_column="LM_char50_32",
                                     verbose_name="Income Year (2)", null=True,
                                     blank=True)
    income_year_3 = models.CharField(max_length=100, db_column="LM_char50_33",
                                     verbose_name="Income Year (3)", null=True,
                                     blank=True)
    expense_1 = models.CharField(max_length=100, db_column="LM_char50_34",
                                 verbose_name="Expense 1", null=True,
                                 blank=True)
    expense_2 = models.CharField(max_length=100, db_column="LM_char50_35",
                                 verbose_name="Expense 2", null=True,
                                 blank=True)
    expense_3 = models.CharField(max_length=100, db_column="LM_char50_36",
                                 verbose_name="Expense 3", null=True,
                                 blank=True)
    second_improvement = models.CharField(max_length=100,
                                          db_column="LM_char50_37",
                                          verbose_name="2nd Improvement",
                                          null=True, blank=True)
    third_improvement = models.CharField(max_length=100,
                                         db_column="LM_char50_38",
                                         verbose_name="3rd Improvement",
                                         null=True, blank=True)
    present_use = models.CharField(max_length=100, db_column="LM_char50_39",
                                   verbose_name="Present Use", null=True,
                                   blank=True)
    distance_to_gas = models.CharField(max_length=100, db_column="LM_char50_40",
                                       verbose_name="Distance to Gas",
                                       null=True, blank=True)
    year_3 = models.CharField(max_length=100, db_column="LM_char50_6",
                              verbose_name="Year (3)", null=True, blank=True)
    motivewant = models.CharField(max_length=100, db_column="LM_char50_7",
                                  verbose_name="Motive/Want", null=True,
                                  blank=True)
    well_depth = models.CharField(max_length=100, db_column="LM_char50_8",
                                  verbose_name="Well Depth", null=True,
                                  blank=True)
    gallons_per_min = models.CharField(max_length=100, db_column="LM_char50_9",
                                       verbose_name="Gallons per Min.",
                                       null=True, blank=True)
    building_amenities = models.CharField(max_length=512,
                                          db_column="LM_char512_1",
                                          verbose_name="Building Amenities",
                                          null=True, blank=True)
    water_district_url = models.CharField(max_length=100,
                                          db_column="LM_char5_10",
                                          verbose_name="Water District URL",
                                          null=True, blank=True)
    trees_2 = models.CharField(max_length=100, db_column="LM_char5_11",
                               verbose_name="Trees (2)", null=True, blank=True)
    entry_level_building = models.CharField(max_length=100,
                                            db_column="LM_char5_12",
                                            verbose_name="Entry Level Building",
                                            null=True, blank=True)
    second_loan_assumable = models.CharField(max_length=100,
                                             db_column="LM_char5_13",
                                             verbose_name="2nd Loan Assumable",
                                             null=True, blank=True)
    fiscal_year_from = models.CharField(max_length=100, db_column="LM_char5_14",
                                        verbose_name="Fiscal Year From",
                                        null=True, blank=True)
    fiscal_year_to = models.CharField(max_length=100, db_column="LM_char5_15",
                                      verbose_name="Fiscal Year To", null=True,
                                      blank=True)
    bln_assumable = models.CharField(max_length=100, db_column="LM_char5_16",
                                     verbose_name="BLN Assumable", null=True,
                                     blank=True)
    trees_3 = models.CharField(max_length=100, db_column="LM_char5_17",
                               verbose_name="Trees (3)", null=True, blank=True)
    trees_4 = models.CharField(max_length=100, db_column="LM_char5_18",
                               verbose_name="Trees (4)", null=True, blank=True)
    trees_5 = models.CharField(max_length=100, db_column="LM_char5_19",
                               verbose_name="Trees (5)", null=True, blank=True)
    map_code_column = models.CharField(max_length=100, db_column="LM_char5_2",
                                       verbose_name="Map Code Column",
                                       null=True, blank=True)
    unit_number_9 = models.CharField(max_length=100, db_column="LM_char5_20",
                                     verbose_name="Unit Number (9)", null=True,
                                     blank=True)
    unit_number_10 = models.CharField(max_length=100, db_column="LM_char5_21",
                                      verbose_name="Unit Number (10)",
                                      null=True, blank=True)
    amps = models.CharField(max_length=100, db_column="LM_char5_22",
                            verbose_name="Amps", null=True, blank=True)
    well_casing_size = models.CharField(max_length=100, db_column="LM_char5_23",
                                        verbose_name="Well Casing Size",
                                        null=True, blank=True)
    water_table = models.CharField(max_length=100, db_column="LM_char5_24",
                                   verbose_name="Water Table", null=True,
                                   blank=True)
    well_pump_hp = models.CharField(max_length=100, db_column="LM_char5_25",
                                    verbose_name="Well Pump HP", null=True,
                                    blank=True)
    sub_flooring = models.CharField(max_length=100, db_column="LM_char5_26",
                                    verbose_name="Sub-Flooring", null=True,
                                    blank=True)
    animal_designation_code = models.CharField(max_length=100,
                                               db_column="LM_char5_27",
                                               verbose_name="Animal Designation Code",
                                               null=True, blank=True)
    land_use_code = models.CharField(max_length=100, db_column="LM_char5_28",
                                     verbose_name="Land Use Code", null=True,
                                     blank=True)
    home_owner_fee_reflects = models.CharField(max_length=100,
                                               db_column="LM_char5_29",
                                               verbose_name="Home Owner Fee Reflects",
                                               null=True, blank=True)
    map_code_page = models.CharField(max_length=100, db_column="LM_char5_3",
                                     verbose_name="Map Code Page", null=True,
                                     blank=True)
    home_owners_payment_freq = models.CharField(max_length=100,
                                                db_column="LM_char5_30",
                                                verbose_name="Home Owners Payment Freq.",
                                                null=True, blank=True)
    other_fees_reflect = models.CharField(max_length=100,
                                          db_column="LM_char5_31",
                                          verbose_name="Other Fees Reflect",
                                          null=True, blank=True)
    other_fees_payment_freq = models.CharField(max_length=100,
                                               db_column="LM_char5_32",
                                               verbose_name="Other Fees Payment Freq.",
                                               null=True, blank=True)
    cfdmello_roos_fee_reflct = models.CharField(max_length=100,
                                                db_column="LM_char5_34",
                                                verbose_name="CFD/Mello-Roos Fee Reflct",
                                                null=True, blank=True)
    cfdmello_roos_pay_freq = models.CharField(max_length=100,
                                              db_column="LM_char5_35",
                                              verbose_name="CFD/Mello-Roos Pay Freq.",
                                              null=True, blank=True)
    assessments = models.CharField(max_length=100, db_column="LM_char5_36",
                                   verbose_name="Assessments", null=True,
                                   blank=True)
    occupied = models.CharField(max_length=100, db_column="LM_char5_37",
                                verbose_name="Occupied", null=True, blank=True)
    mandatory_remarks = models.CharField(max_length=100,
                                         db_column="LM_char5_38",
                                         verbose_name="Mandatory Remarks",
                                         null=True, blank=True)
    map_code_row = models.CharField(max_length=100, db_column="LM_char5_4",
                                    verbose_name="Map Code Row", null=True,
                                    blank=True)
    length = models.CharField(max_length=100, db_column="LM_char5_42",
                              verbose_name="Length", null=True, blank=True)
    width = models.CharField(max_length=100, db_column="LM_char5_43",
                             verbose_name="Width", null=True, blank=True)
    association_id = models.CharField(max_length=100, db_column="LM_char5_44",
                                      verbose_name="Association ID", null=True,
                                      blank=True)
    unit_1_laundry_hook_ups = models.CharField(max_length=100,
                                               db_column="LM_char5_45",
                                               verbose_name="Unit 1 Laundry Hook Ups",
                                               null=True, blank=True)
    unit_2_laundry_hook_ups = models.CharField(max_length=100,
                                               db_column="LM_char5_46",
                                               verbose_name="Unit 2 Laundry Hook Ups",
                                               null=True, blank=True)
    unit_3_laundry_hook_ups = models.CharField(max_length=100,
                                               db_column="LM_char5_47",
                                               verbose_name="Unit 3 Laundry Hook Ups",
                                               null=True, blank=True)
    unit_4_laundry_hook_ups = models.CharField(max_length=100,
                                               db_column="LM_char5_48",
                                               verbose_name="Unit 4 Laundry Hook Ups",
                                               null=True, blank=True)
    unit_1_occupied = models.CharField(max_length=100, db_column="LM_char5_49",
                                       verbose_name="Unit 1 Occupied",
                                       null=True, blank=True)
    limited_service = models.CharField(max_length=100, db_column="LM_char5_5",
                                       verbose_name="Limited Service",
                                       null=True, blank=True)
    unit_2_occupied = models.CharField(max_length=100, db_column="LM_char5_50",
                                       verbose_name="Unit 2 Occupied",
                                       null=True, blank=True)
    unit_3_occupied = models.CharField(max_length=100, db_column="LM_char5_51",
                                       verbose_name="Unit 3 Occupied",
                                       null=True, blank=True)
    unit_4_occupied = models.CharField(max_length=100, db_column="LM_char5_52",
                                       verbose_name="Unit 4 Occupied",
                                       null=True, blank=True)
    parcel_map_number = models.CharField(max_length=100,
                                         db_column="LM_char5_53",
                                         verbose_name="Parcel Map Number",
                                         null=True, blank=True)
    tentative_map_number = models.CharField(max_length=100,
                                            db_column="LM_char5_54",
                                            verbose_name="Tentative Map Number",
                                            null=True, blank=True)
    price_reflects = models.CharField(max_length=100, db_column="LM_char5_55",
                                      verbose_name="Price Reflects", null=True,
                                      blank=True)
    lease_required = models.CharField(max_length=100, db_column="LM_char5_58",
                                      verbose_name="Lease Required", null=True,
                                      blank=True)
    rental_type = models.CharField(max_length=100, db_column="LM_char5_59",
                                   verbose_name="Rental Type", null=True,
                                   blank=True)
    first_loan_assumable = models.CharField(max_length=100,
                                            db_column="LM_char5_6",
                                            verbose_name="1st Loan Assumable",
                                            null=True, blank=True)
    jurisdiction = models.CharField(max_length=100, db_column="LM_char5_7",
                                    verbose_name="Jurisdiction", null=True,
                                    blank=True)
    listing_type = models.CharField(max_length=100, db_column="LM_char5_8",
                                    verbose_name="Listing Type", null=True,
                                    blank=True)
    water_district = models.CharField(max_length=100, db_column="LM_char5_9",
                                      verbose_name="Water District", null=True,
                                      blank=True)
    price_per_unit = models.IntegerField(db_column="LM_Int4_22",
                                         verbose_name="Price/Unit", null=True,
                                         blank=True)
    tax_year_from = models.IntegerField(db_column="LM_Int4_23",
                                        verbose_name="Tax Year From", null=True,
                                        blank=True)
    gross_equity = models.IntegerField(db_column="LM_Int4_24",
                                       verbose_name="Gross Equity", null=True,
                                       blank=True)
    tax_year_to = models.IntegerField(db_column="LM_Int4_25",
                                      verbose_name="Tax Year To", null=True,
                                      blank=True)
    tax_amount = models.IntegerField(db_column="LM_Int4_26",
                                     verbose_name="Tax Amount", null=True,
                                     blank=True)
    street_frontage = models.IntegerField(db_column="LM_Int4_27",
                                          verbose_name="Street Frontage",
                                          null=True, blank=True)
    accounts_receiveable = models.IntegerField(db_column="LM_Int4_28",
                                               verbose_name="Accounts Receiveable",
                                               null=True, blank=True)
    assets_equipment = models.IntegerField(db_column="LM_Int4_29",
                                           verbose_name="Assets Equipment",
                                           null=True, blank=True)
    assets_leasehold_imp = models.IntegerField(db_column="LM_Int4_30",
                                               verbose_name="Assets Leasehold Imp.",
                                               null=True, blank=True)
    assets_real_estate = models.IntegerField(db_column="LM_Int4_31",
                                             verbose_name="Assets Real Estate",
                                             null=True, blank=True)
    assets_other = models.IntegerField(db_column="LM_Int4_32",
                                       verbose_name="Assets Other", null=True,
                                       blank=True)
    assets_total = models.IntegerField(db_column="LM_Int4_33",
                                       verbose_name="Assets Total", null=True,
                                       blank=True)
    accounts_payable = models.IntegerField(db_column="LM_Int4_34",
                                           verbose_name="Accounts Payable",
                                           null=True, blank=True)
    monthly_rent_total = models.IntegerField(db_column="LM_Int4_35",
                                             verbose_name="Monthly Rent Total",
                                             null=True, blank=True)
    accrued_expenses = models.IntegerField(db_column="LM_Int4_36",
                                           verbose_name="Accrued Expenses",
                                           null=True, blank=True)
    long_term_liability = models.IntegerField(db_column="LM_Int4_37",
                                              verbose_name="Long Term Liability",
                                              null=True, blank=True)
    total_liability = models.IntegerField(db_column="LM_Int4_38",
                                          verbose_name="Total Liability",
                                          null=True, blank=True)
    retained_earnings = models.IntegerField(db_column="LM_Int4_39",
                                            verbose_name="Retained Earnings",
                                            null=True, blank=True)
    number_of_employees = models.IntegerField(db_column="LM_Int4_40",
                                              verbose_name="Number of Employees",
                                              null=True, blank=True)
    association_dues_2 = models.IntegerField(db_column="LM_Int4_41",
                                             verbose_name="Association Dues 2",
                                             null=True, blank=True)
    concessions_amount = models.IntegerField(db_column="LM_Int4_42",
                                             verbose_name="Concessions Amount",
                                             null=True, blank=True)
    land_lease_amount = models.IntegerField(db_column="LM_Int4_44",
                                            verbose_name="Land Lease Amount",
                                            null=True, blank=True)
    number_carport_spaces = models.IntegerField(db_column="LM_Int4_45",
                                                verbose_name="Number Carport Spaces",
                                                null=True, blank=True)
    open_house_count = models.IntegerField(db_column="LM_Int4_47",
                                           verbose_name="Open House Count",
                                           null=True, blank=True)
    crmls_listing_key_numeric = models.IntegerField(db_column="LM_Int4_50",
                                                    verbose_name="CRMLSListingKeyNumeric",
                                                    null=True, blank=True)
    neighboring_bus_type_3 = models.CharField(max_length=100,
                                              db_column="LR_remarks1010",
                                              verbose_name="Neighboring Bus. Type (3)",
                                              null=True, blank=True)
    remarks = models.CharField(max_length=1025, db_column="LR_remarks11",
                               verbose_name="Remarks", null=True, blank=True)
    neighboring_bus_type_4 = models.CharField(max_length=100,
                                              db_column="LR_remarks1111",
                                              verbose_name="Neighboring Bus. Type (4)",
                                              null=True, blank=True)
    neighboring_bus_type_5 = models.CharField(max_length=100,
                                              db_column="LR_remarks1212",
                                              verbose_name="Neighboring Bus. Type (5)",
                                              null=True, blank=True)
    neighboring_bus_type_6 = models.CharField(max_length=100,
                                              db_column="LR_remarks1313",
                                              verbose_name="Neighboring Bus. Type (6)",
                                              null=True, blank=True)
    selling_agent_bre = models.CharField(max_length=100,
                                         db_column="LR_remarks1515",
                                         verbose_name="Selling Agent BRE #",
                                         null=True, blank=True)
    full_address = models.CharField(max_length=150, db_column="LR_remarks1616",
                                    verbose_name="Full Address", null=True,
                                    blank=True)
    directions_to_property = models.CharField(max_length=500,
                                              db_column="LR_remarks44",
                                              verbose_name="Directions To Property",
                                              null=True, blank=True)
    selling_agent_2_bre = models.CharField(max_length=100,
                                           db_column="LR_remarks55",
                                           verbose_name="Selling Agent 2 BRE #",
                                           null=True, blank=True)
    supplement = models.CharField(max_length=4000, db_column="LR_remarks66",
                                  verbose_name="Supplement", null=True,
                                  blank=True)
    selling_agent_2_bre_2 = models.CharField(max_length=100,
                                             db_column="LR_remarks77",
                                             verbose_name="Selling Agent 2 BRE # 2",
                                             null=True, blank=True)
    neighboring_bus_type_1 = models.CharField(max_length=100,
                                              db_column="LR_remarks88",
                                              verbose_name="Neighboring Bus. Type (1)",
                                              null=True, blank=True)
    neighboring_bus_type_2 = models.CharField(max_length=100,
                                              db_column="LR_remarks99",
                                              verbose_name="Neighboring Bus. Type (2)",
                                              null=True, blank=True)


class FeatureCategory(models.Model):
    name = models.CharField(max_length=50)


class Feature(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    rets_name = models.CharField(max_length=50)
    category = models.ForeignKey(to=FeatureCategory, blank=True, null=True)

    class Meta:
        unique_together = ("rets_name", "value")


class Agent(models.Model):
    listing = models.ManyToManyField('Listing')
    # RETS PK Field
    agent_id = models.CharField(max_length=20, db_column="LA1_AgentID",
                                verbose_name="Agent ID", unique=True)
    user_designation = models.CharField(null=True, blank=True, max_length=255,
                                        db_column="LA1_Char255_1",
                                        verbose_name="User Designation")
    agent_logon_name = models.CharField(db_column="LA1_LoginName",
                                        max_length=100, null=True, blank=True,
                                        verbose_name="Agent Logon Name")
    assistant_for = models.CharField(null=True, blank=True, max_length=50,
                                     db_column="LA1_Char50_1",
                                     verbose_name="Assistant For")
    agent_full_name = models.CharField(null=True, blank=True, max_length=50,
                                       db_column="LA1_Char50_3",
                                       verbose_name="Agent Full Name")

    phone_number_1 = models.CharField(null=True, blank=True, max_length=30,
                                      db_column="LA1_PhoneNumber1",
                                      verbose_name="Agent Phone Number 1")
    phone_number_1_country_code_id = models.CharField(max_length=25, null=True,
                                                      blank=True,
                                                      db_column="LA1_PhoneNumber1CountryCodeId",
                                                      verbose_name="Agent Phone Number 1 Country Code")
    phone_number_1_desc = models.CharField(null=True, blank=True, max_length=5,
                                           db_column="LA1_PhoneNumber1Desc",
                                           verbose_name="Agent Phone Number 1 Description")
    phone_number_1_ext = models.CharField(null=True, blank=True, max_length=5,
                                          db_column="LA1_PhoneNumber1Ext",
                                          verbose_name="Agent Phone Number 1 Extension")
    phone_number_2 = models.CharField(null=True, blank=True, max_length=30,
                                      db_column="LA1_PhoneNumber2",
                                      verbose_name="Agent Phone Number 2")
    phone_number_2_country_code_id = models.CharField(max_length=25, null=True,
                                                      blank=True,
                                                      db_column="LA1_PhoneNumber2CountryCodeId",
                                                      verbose_name="Agent Phone Number 2 Country Code")
    phone_number_2_desc = models.CharField(null=True, blank=True, max_length=5,
                                           db_column="LA1_PhoneNumber2Desc",
                                           verbose_name="Agent Phone Number 2 Description")
    phone_number_2_ext = models.CharField(null=True, blank=True, max_length=5,
                                          db_column="LA1_PhoneNumber2Ext",
                                          verbose_name="Agent Phone Number 2 Extension")
    phone_number_3 = models.CharField(null=True, blank=True, max_length=30,
                                      db_column="LA1_PhoneNumber3",
                                      verbose_name="Agent Phone Number 3")
    phone_number_3_country_code_id = models.CharField(max_length=25, null=True,
                                                      blank=True,
                                                      db_column="LA1_PhoneNumber3CountryCodeId",
                                                      verbose_name="Agent Phone Number 3 Country Code")
    phone_number_3_desc = models.CharField(null=True, blank=True, max_length=5,
                                           db_column="LA1_PhoneNumber3Desc",
                                           verbose_name="Agent Phone Number 3 Description")
    phone_number_3_ext = models.CharField(null=True, blank=True, max_length=5,
                                          db_column="LA1_PhoneNumber3Ext",
                                          verbose_name="Agent Phone Number 3 Extension")
    phone_number_4 = models.CharField(null=True, blank=True, max_length=30,
                                      db_column="LA1_PhoneNumber4",
                                      verbose_name="Agent Phone Number 4 Number")
    phone_number_4_country_code_id = models.CharField(max_length=25, null=True,
                                                      blank=True,
                                                      db_column="LA1_PhoneNumber4CountryCodeId",
                                                      verbose_name="Agent Phone Number 4 Country Code")
    phone_number_4_desc = models.CharField(null=True, blank=True, max_length=5,
                                           db_column="LA1_PhoneNumber4Desc",
                                           verbose_name="Agent Phone Number 4 Description")
    phone_number_4_ext = models.CharField(null=True, blank=True, max_length=5,
                                          db_column="LA1_PhoneNumber4Ext",
                                          verbose_name="Agent Phone Number 4 Extension")
    phone_number_5 = models.CharField(null=True, blank=True, max_length=30,
                                      db_column="LA1_PhoneNumber5",
                                      verbose_name="Agent Phone Number 5")
    phone_number_5_country_code_id = models.CharField(max_length=25, null=True,
                                                      blank=True,
                                                      db_column="LA1_PhoneNumber5CountryCodeId",
                                                      verbose_name="Agent Phone Number 5 Country Code")
    phone_number_5_desc = models.CharField(null=True, blank=True, max_length=5,
                                           db_column="LA1_PhoneNumber5Desc",
                                           verbose_name="Agent Phone Number 5 Description")
    phone_number_5_ext = models.CharField(null=True, blank=True, max_length=5,
                                          db_column="LA1_PhoneNumber5Ext",
                                          verbose_name="Agent Phone Number 5 Extension")
    user_first_name = models.CharField(null=True, blank=True, max_length=50,
                                       db_column="LA1_UserFirstName",
                                       verbose_name="Agent First Name")
    user_last_name = models.CharField(null=True, blank=True, max_length=50,
                                      db_column="LA1_UserLastName",
                                      verbose_name="Agent Last Name")
    user_mi = models.CharField(null=True, blank=True, max_length=1,
                               db_column="LA1_UserMI",
                               verbose_name="Agent Middle Initial")


class Office(models.Model):
    listing = models.ManyToManyField('Listing')
    office_id = models.IntegerField(db_column="LO1_HiddenOrgID",
                                    verbose_name="Office Identifier",
                                    unique=True)
    main_office_id = models.IntegerField(null=True, blank=True,
                                         db_column="LO1_BranchOfOrgID",
                                         verbose_name="Main Office ID")
    organization_name = models.CharField(max_length=100,
                                         null=True, blank=True,
                                         db_column="LO1_OrganizationName",
                                         verbose_name="Office Name")
    phone_number = models.CharField(max_length=30, null=True, blank=True,
                                    db_column="LO1_PhoneNumber1",
                                    verbose_name="Office Phone Number")
    phone_number_country_code_id = models.CharField(max_length=25,
                                                    null=True, blank=True,
                                                    db_column="LO1_PhoneNumber1CountryCodeId",
                                                    verbose_name="Office Phone Number Country Code")
    phone_number_desc = models.CharField(max_length=10,
                                         null=True, blank=True,
                                         db_column="LO1_PhoneNumber1Desc",
                                         verbose_name="Office Phone Number Description")
    phone_number_ext = models.CharField(max_length=10,
                                        null=True, blank=True,
                                        db_column="LO1_PhoneNumber1Ext",
                                        verbose_name="Office Phone Number Extension")
    short_name = models.CharField(max_length=25, null=True, blank=True,
                                  db_column="LO1_ShortName",
                                  verbose_name="Office Abbreviation")
    board_id = models.CharField(max_length=50, null=True, blank=True,
                                db_column="LO1_board_id",
                                verbose_name="Board ID")
    internet_syndication_yn = models.CharField(max_length=10,
                                               null=True, blank=True,
                                               db_column="LO1_Char10_1",
                                               verbose_name="Internet Syndication (Y/N)")
    sign_on_san_diego_yn = models.CharField(db_column="LO1_Char50_1", null=True,
                                            blank=True, max_length=100,
                                            verbose_name="SignOnSanDiego Y/N")
    office_url = models.URLField(db_column="LO1_WebPage", null=True, blank=True,
                                 verbose_name="Office URL")


class Photo(models.Model):
    listing = models.ForeignKey('Listing', related_name='image')
    url = models.URLField()

    # Use this property in the actual app to return a placeholder image if image URL isn't available
    # @property
    # def get_image(self):
    #     response = requests.get(self.image)
    #     if not response.ok:
    #         return urljoin(settings.STATIC_URL, 'img/noImage.jpg')
    #     else:
    #         return self.image


class VirtualTour(models.Model):
    listing = models.ForeignKey('Listing', related_name='virtual_tour')
    vrbo_url = models.URLField(db_column="VT_ExtVTourURL1",
                               verbose_name="VRBO URL", null=True,
                               blank=True)
    virtual_tour_link_2 = models.URLField(db_column="VT_ExtVTourURL2",
                                          verbose_name="Virtual Tour Link 2",
                                          null=True, blank=True)
    pp_insta = models.URLField(db_column="VT_ExtVTourURL3",
                               verbose_name="PP_Insta", null=True, blank=True)
    three_d_url = models.URLField(db_column="VT_ExtVTourURL4",
                                  verbose_name="3D_URL",
                                  null=True, blank=True)
    virtual_tour_link = models.URLField(db_column="VT_VTourURL",
                                        verbose_name="Virtual Tour Link",
                                        null=True, blank=True)


class TaxInfo(models.Model):
    listing = models.ForeignKey('Listing', related_name='tax_info')
    tax_property_id = models.CharField(max_length=50,
                                       db_column="T_list_tax_property_id",
                                       verbose_name="Tax Property ID",
                                       null=True, blank=True)
