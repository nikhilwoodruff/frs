from frs.table_utils import *


def parse_oddjob(line, person):
    if safe(line["OJREG"]) == 1:
        person["odd_job_income"] += yearly(line["OJAMT"])
    else:
        person["odd_job_income"] += safe(line["OJAMT"])
    return person


ODDJOB_FIELDNAMES = ["odd_job_income"]

ODDJOB_ENUMS = {}
