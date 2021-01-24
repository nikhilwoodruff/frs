from frs.tables.adult import parse_adult, ADULT_FIELDNAMES
from frs.tables.accounts import parse_account, ACCOUNTS_FIELDNAMES
from frs.tables.assets import parse_asset, ASSETS_FIELDNAMES
from frs.tables.benefits import parse_benefit, BENEFITS_FIELDNAMES
from frs.tables.benunit import parse_benunit, BENUNIT_FIELDNAMES
from frs.tables.care import parse_care, CARE_FIELDNAMES
from frs.tables.child import parse_child, CHILD_FIELDNAMES
from frs.tables.childcare import parse_childcare, CHILDCARE_FIELDNAMES
from frs.tables.endowment import parse_endowment, ENDOWMENT_FIELDNAMES
from frs.tables.extchild import parse_extchild, EXTCHILD_FILENAMES
from frs.tables.govpay import parse_govpay, GOVPAY_FIELDNAMES

PERSON_FIELDNAMES = ADULT_FIELDNAMES + ACCOUNTS_FIELDNAMES + ASSETS_FIELDNAMES + BENEFITS_FIELDNAMES + CARE_FIELDNAMES + CHILD_FIELDNAMES + CHILDCARE_FIELDNAMES + GOVPAY_FIELDNAMES
BENUNIT_FIELDNAMES = BENUNIT_FIELDNAMES + EXTCHILD_FILENAMES
HOUSEHOLD_FIELDNAMES = ENDOWMENT_FIELDNAMES