from frs.tables.adult import parse_adult, ADULT_FIELDNAMES
from frs.tables.accounts import parse_account, ACCOUNTS_FIELDNAMES
from frs.tables.assets import parse_asset, ASSETS_FIELDNAMES
from frs.tables.benefits import parse_benefit, BENEFITS_FIELDNAMES
from frs.tables.benunit import parse_benunit, BENUNIT_FIELDNAMES
from frs.tables.care import parse_care, CARE_FIELDNAMES

PERSON_FIELDNAMES = ADULT_FIELDNAMES + ACCOUNTS_FIELDNAMES + ASSETS_FIELDNAMES + BENEFITS_FIELDNAMES + CARE_FIELDNAMES
BENUNIT_FIELDNAMES = BENUNIT_FIELDNAMES