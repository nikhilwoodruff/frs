from frs.table_utils import *


def parse_pension(line, person):
    person["pension_income"] += yearly(line["PENPAY"]) + safe(line["PLUMPAMT"])
    if safe(line["PTINC"]) == 2:
        person["pension_income"] += yearly(line["PTAMT"])
    if safe(line["POINC"]) == 2:
        person["pension_income"] += yearly(line["POAMT"])
    return person


PENSION_FIELDNAMES = ["pension_income"]

PENSION_ENUMS = {}
