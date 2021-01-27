from frs.table_utils import *
from frs.tables.accounts import ACCOUNT_TYPES


def parse_benefit(line, person):
    if safe(line["BENEFIT"]) in list(BENEFITS) + [14, 16]:
        if safe(line["BENEFIT"]) in BENEFITS:
            benefit = BENEFITS[safe(line["BENEFIT"])]
        if safe(line["BENEFIT"]) == 14:
            JSA_type = JSA_ESA_TYPES[int(safe(line["VAR2"]))]
            benefit = f"JSA_{JSA_type}"
        elif safe(line["BENEFIT"]) == 16:
            ESA_type = JSA_ESA_TYPES[int(safe(line["VAR2"]))]
            benefit = f"ESA_{ESA_type}"
        amount = yearly(safe(line["BENAMT"], line["NOTUSAMT"]))
        person[benefit + "_reported"] = amount
        person["total_benefits"] += amount
    return person


BENEFITS = {
    NO_DATA: "unknown",
    1: "DLA_SC",
    2: "DLA_M",
    3: "child_benefit",
    4: "pension_credit",
    5: "state_pension",
    6: "BSP",
    8: "AFCS",
    9: "war_pension",
    10: "SDA",
    12: "AA",
    13: "carers_allowance",
    14.1: "JSA_contrib",
    14.2: "JSA_income",
    15: "IIDB",
    16.1: "ESA_contrib",
    16.2: "ESA_income",
    17: "incapacity_benefit",
    19: "income_support",
    21: "maternity_allowance",
    22: "sure_start_maternity_grant",
    24: "funeral_grant_from_social_fund",
    30: "other_benefit",
    31: "trade_union_strike_sick_pay",
    32: "friendly_society_benefits",
    33: "private_sickness_scheme",
    34: "accident_insurance_scheme",
    35: "hospital_savings_scheme",
    36: "GTA",
    37: "guardians_allowance",
    60: "widows_payment",
    61: "unemployment_insurance",
    62: "winter_fuel_allowance",
    65: "DWP_IS",
    66: "DWP_JSA",
    69: "SFL_IS",
    70: "SFL_JSA",
    78: "extended_HB",
    81: "permanent_health_insurance",
    82: "other_sickness_insurance",
    83: "critical_illness_cover",
    90: "working_tax_credit",
    91: "child_tax_credit",
    92: "WTC_lump_sum",
    93: "CTC_lump_sum",
    94: "housing_benefit",
    95: "universal_credit",
    96: "PIP_DL",
    97: "PIP_M",
    98: "DWP_loan",
    99: "LA_loan",
    110: "DWP_UC",
    111: "SFL_UC",
}

JSA_ESA_TYPES = {
    0: "income",
    1: "income",
    2: "income",
    3: "contrib",
    4: "contrib",
    5: "contrib",
    6: "contrib",
}

BENEFITS_FIELDNAMES = list(map(lambda x: x + "_reported", BENEFITS.values())) + ["total_benefits"]

BENEFITS_ENUMS = {}
