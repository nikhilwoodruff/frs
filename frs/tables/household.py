from frs.table_utils import *


def parse_household(line, household):
    household["household_id"] = household_id(line)
    household["num_bedrooms"] = safe(line["BEDROOM6"])
    household["num_benunits"] = safe(line["BENUNITS"])

    # bills
    household["ground_rent"] = yearly(line["CHRGAMT1"])
    household["chief_rent"] = yearly(line["CHRGAMT3"])
    household["service_charge"] = yearly(line["CHRGAMT4"])
    household["regular_maintenance"] = yearly(line["CHRGAMT5"])
    household["site_rent"] = yearly(line["CHRGAMT6"])
    household["factoring"] = yearly(line["CHRGAMT7"])
    household["other_regular_charges"] = yearly(line["CHRGAMT8"])
    household["combined_services"] = yearly(line["CHRGAMT9"])

    household["country"] = COUNTRIES[safe(line["COUNTRY"])]

    household["building_insured"] = safe(line["COVOTHS"]) in [1, 2]
    household["contents_insured"] = safe(line["COVOTHS"]) == 2

    household["council_tax_discount"] = COUNCIL_TAX_DISCOUNT[
        safe(line["CT25D50D"])
    ]
    household["council_tax_band"] = COUNCIL_TAX_BAND[safe(line["CTBAND"])]
    household["council_tax_benefit"] = yearly(line["CTREBAMT"])
    household["council_tax"] = (
        safe(line["CTANNUAL"]) - household["council_tax_benefit"]
    ) / (1 - household["council_tax_discount"])

    household["total_housing_costs"] = yearly(line["GBHSCOST"]) + yearly(
        line["NIHSCOST"]
    )

    household["household_weight"] = safe(line["GROSS4"])

    household["region"] = REGIONS[safe(line["GVTREGNO"])]

    household["rent"] = yearly(line["HHRENT"])
    household["is_shared"] = safe(line["HHSTAT"]) == 2
    household["in_inner_london"] = safe(line["LONDON"]) == 1
    household["in_outer_london"] = safe(line["LONDON"]) == 2
    household["household_type"] = HOUSEHOLD_TYPE[safe(line["MAINACC"])]

    household["domestic_rates"] = yearly(safe(line["NIRATLIA"]))
    household["business_rooms"] = safe(line["PTBSROOM"])
    household["num_rooms"] = safe(line["ROOMS10"])

    household["rates_rebate"] = yearly(line["RTREBAMT"])
    household["rate_relief"] = yearly(line["RTRTRAMT"])
    household["sewerage_rate"] = yearly(line["SEWANUL"])

    household["insurance_premium"] = yearly(line["STRAMT2"])
    household["rent_from_subletting"] = yearly(line["SUBRENT"])
    household["tenure"] = TENURE[safe(line["TENURE"])]
    household["water_rate"] = yearly(line["WATANUL"])
    household["is_social"] = safe(line["PTENTYP2"]) in [1, 2]
    return household


TENURE = {
    NO_DATA: "owned",
    1: "owned",
    2: "mortgage",
    3: "part_own_part_rent",
    4: "rented",
    5: "rent_free",
    6: "squatting",
}

HOUSEHOLD_TYPE = {
    NO_DATA: "house",
    1: "house",
    2: "flat",
    3: "room",
    4: "other",
}

COUNTRIES = {
    NO_DATA: "england",
    1: "england",
    2: "wales",
    3: "scotland",
    4: "northern_ireland",
}

REGIONS = {
    NO_DATA: "unknown",
    1: "north_east",
    2: "north_west",
    4: "yorkshire",
    5: "east_midlands",
    6: "west_midlands",
    7: "east_of_england",
    8: "london",
    9: "south_east",
    10: "south_west",
    11: "wales",
    12: "scotland",
    13: "northern_ireland",
}

COUNCIL_TAX_DISCOUNT = {0: 0, 1: 0.25, 2: 0.5}

COUNCIL_TAX_BAND = {
    NO_DATA: "unknown",
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H",
    9: "I",
    10: "unknown",
}

HOUSEHOLD_FIELDNAMES = [
    "household_id",
    "num_bedrooms",
    "num_benunits",
    "ground_rent",
    "chief_rent",
    "service_charge",
    "regular_maintenance",
    "site_rent",
    "factoring",
    "other_regular_charges",
    "combined_services",
    "country",
    "building_insured",
    "contents_insured",
    "council_tax_discount",
    "council_tax_band",
    "council_tax",
    "council_tax_benefit",
    "total_housing_costs",
    "household_weight",
    "region",
    "rent",
    "is_shared",
    "in_inner_london",
    "in_outer_london",
    "household_type",
    "domestic_rates",
    "business_rooms",
    "num_rooms",
    "rates_rebate",
    "rate_relief",
    "sewerage_rate",
    "insurance_premium",
    "rent_from_subletting",
    "tenure",
    "water_rate",
    "is_social",
]

HOUSEHOLD_ENUMS = dict(
    country=COUNTRIES,
    council_tax_band=COUNCIL_TAX_BAND,
    region=REGIONS,
    household_type=HOUSEHOLD_TYPE,
    tenure=TENURE,
)
