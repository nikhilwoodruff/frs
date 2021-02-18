from frs.table_utils import *
from frs.tables.accounts import ACCOUNT_TYPES


def parse_asset(line, person):
    account_type = ACCOUNT_TYPES[safe(line["ASSETYPE"])]
    person[account_type + "_is_joint"] = safe(line["ACCNAME"]) == 2
    value = safe(line["HOWMUCH"], line["HOWMUCHE"])
    person[account_type + "_value"] = value
    return person


ASSETS_FIELDNAMES = list(
    map(lambda x: x + "_value", ACCOUNT_TYPES.values())
) + list(map(lambda x: x + "_is_joint", ACCOUNT_TYPES.values()))

ASSETS_ENUMS = {}
