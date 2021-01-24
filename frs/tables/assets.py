from frs.table_utils import *
from frs.tables.accounts import ACCOUNT_TYPES

def parse_asset(line, person):
    person["is_joint_account"] = safe(line["ACCNAME"]) == 2
    account_type = ACCOUNT_TYPES[safe(line["ACCTYPE"])]
    value = safe(line["HOWMUCH"], line["HOWMUCHE"])
    person[account_type + "_value"] = value
    return person

ASSETS_FIELDNAMES = list(map(lambda x : x + "_value", ACCOUNT_TYPES.values()))