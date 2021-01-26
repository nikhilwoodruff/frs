from frs.table_utils import *


def parse_pension(line, person):
    person["pension_income"] += yearly(line["PENPAY"])
    person["income_tax_reported"] += yearly(line["PTAMT"])
    if safe(line["PTINC"]) == 2:
        person["pension_income"] += yearly(line["PTAMT"])
    return person


PENSION_FIELDNAMES = ["pension_income"]

PENSION_ENUMS = {}
