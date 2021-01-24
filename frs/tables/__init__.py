from frs.tables.adult import parse_adult, ADULT_FIELDNAMES
from frs.tables.accounts import parse_account, ACCOUNTS_FIELDNAMES
from frs.tables.assets import parse_asset, ASSETS_FIELDNAMES
from frs.tables.benefits import parse_benefit, BENEFITS_FIELDNAMES

PERSON_FIELDNAMES = ADULT_FIELDNAMES + ACCOUNTS_FIELDNAMES + ASSETS_FIELDNAMES + BENEFITS_FIELDNAMES