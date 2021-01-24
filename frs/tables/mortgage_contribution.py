from frs.table_utils import *

def parse_mortgage_contribution(line, household):
    household["ext_mortgage_contribution"] += yearly(line["OUTSAMT"], from_period=line["OUTSPD"])
    return household

MORTGAGE_CONTRIBUTION_FIELDNAMES = ["ext_mortgage_contribution"]

MORTGAGE_CONTRIBUTION_ENUMS = {}