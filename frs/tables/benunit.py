from frs.table_utils import *

def parse_benunit(line, benunit):
    benunit["benunit_id"] = benunit_id(line)
    benunit["benunit_weight"] = safe(line["GROSS4"])
    benunit["can_pay_200_pounds"] = safe(line["OAEXPNS"]) != 2
    benunit["benunit_expenditure"] = yearly(line["TEXPMTH"])
    return benunit

BENUNIT_FIELDNAMES = [
    "benunit_id",
    "benunit_weight",
    "can_pay_200_pounds",
    "benunit_expenditure"
]

BENUNIT_ENUMS = {}