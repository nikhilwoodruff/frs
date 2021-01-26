from frs.table_utils import *


def parse_owner(line, household):
    household["purchase_price"] = safe(line["PURCAMT"])
    return household


OWNER_FIELDNAMES = ["purchase_price"]

OWNER_ENUMS = {}
