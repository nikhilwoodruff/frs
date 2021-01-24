from frs.table_utils import *

def parse_renter(line, household):
    household["furnished"] = FURNISH_STATUS[safe(line["FURNISH"])]
    household["landlord"] = LANDLORD[safe(line["LANDLORD"])]
    household["full_rent"] = yearly(safe(line["RENTFULL"], line["RENT"]))
    household["rent_paid"] = yearly(line["RENT"])
    return household

FURNISH_STATUS = {
    NO_DATA: "no_data",
    1: "furnished",
    2: "partially_furnished",
    3: "unfirnished"
}

LANDLORD = {
    NO_DATA: "none",
    1: "local_authority",
    2: "housing_association",
    3: "employer_org",
    4: "other_org",
    5: "relative_or_friend",
    6: "employer_individual",
    7: "other"
}

RENTER_FIELDNAMES = ["furnished", "landlord", "full_rent", "rent_paid"]

RENTER_ENUMS = dict(
    furnished=FURNISH_STATUS,
    landlord=LANDLORD
)