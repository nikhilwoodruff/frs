from frs.table_utils import *

def parse_oddjob(line, person):
    if safe(line["OJREG"]) == 1:
        person["oddjob_income"] += yearly(line["OJAMT"])
    else:
        person["oddjob_income"] += safe(line["OJAMT"])
    return person

ODDJOB_FIELDNAMES = ["oddjob_income"]

ODDJOB_ENUMS = {}