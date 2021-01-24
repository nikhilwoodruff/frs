from frs.table_utils import *

def parse_rent_contribution(line, household):
    household["rent_contribution"] += yearly("ACCAMT")
    if safe(line["ACCCHK"]) == 2:
        household["rent_paid"] += household["rent_contribution"]
    return household

RENT_CONTRIBUTION_FIELDNAMES = ["rent_contribution", "rent_paid"]

RENT_CONTRIBUTION_ENUMS = {}