from frs.tables.adult import *
from frs.tables.accounts import *
from frs.tables.assets import *
from frs.tables.benefits import *
from frs.tables.benunit import *
from frs.tables.care import *
from frs.tables.child import *
from frs.tables.childcare import *
from frs.tables.endowment import *
from frs.tables.extchild import *
from frs.tables.govpay import *
from frs.tables.household import *
from frs.tables.job import *
from frs.tables.maintenance import *
from frs.tables.mortgage_contribution import *
from frs.tables.mortgage import *
from frs.tables.oddjob import *
from frs.tables.owner import *
from frs.tables.pension_provision import *
from frs.tables.pension import *
from frs.tables.rent_contribution import *
from frs.tables.renter import *

PERSON_FIELDNAMES = (
    ADULT_FIELDNAMES
    + ACCOUNTS_FIELDNAMES
    + ASSETS_FIELDNAMES
    + BENEFITS_FIELDNAMES
    + CHILD_FIELDNAMES
    + CHILDCARE_FIELDNAMES
    + GOVPAY_FIELDNAMES
    + JOB_FIELDNAMES
    + MAINTENANCE_FIELDNAMES
    + ODDJOB_FIELDNAMES
    + PENSION_PROVISION_FIELDNAMES
    + PENSION_FIELDNAMES
)
BENUNIT_FIELDNAMES = BENUNIT_FIELDNAMES + CARE_FIELDNAMES + EXTCHILD_FILENAMES
HOUSEHOLD_FIELDNAMES = (
    ENDOWMENT_FIELDNAMES
    + HOUSEHOLD_FIELDNAMES
    + MORTGAGE_CONTRIBUTION_FIELDNAMES
    + MORTGAGE_FIELDNAMES
    + OWNER_FIELDNAMES
    + RENT_CONTRIBUTION_FIELDNAMES
    + RENTER_FIELDNAMES
)

parse_func = dict(
    accounts=parse_account,
    adult=parse_adult,
    assets=parse_asset,
    benefits=parse_benefit,
    benunit=parse_benunit,
    care=parse_care,
    child=parse_child,
    chldcare=parse_childcare,
    endowmnt=parse_endowment,
    extchild=parse_extchild,
    govpay=parse_govpay,
    househol=parse_household,
    job=parse_job,
    maint=parse_maintenance,
    mortcont=parse_mortgage_contribution,
    mortgage=parse_mortgage,
    oddjob=parse_oddjob,
    owner=parse_owner,
    penprov=parse_pension_provision,
    pension=parse_pension,
    rentcont=parse_rent_contribution,
    renter=parse_renter,
)
