from frs.dataset import Table, Person, BenUnit, Household
from frs.utils import yearly, add


BENEFITS = {
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
    14: "JSA",
    14.1: "JSA_contrib",
    14.2: "JSA_income",
    16: "ESA",
    16.1: "ESA_contrib",
    16.2: "ESA_income",
    15: "IIDB",
    17: "incapacity_benefit",
    19: "income_support",
    21: "maternity_allowance",
    37: "guardians_allowance",
    36: "GTA",
    30: "other_benefit",
    90: "working_tax_credit",
    91: "child_tax_credit",
    92: "WTC_lump_sum",
    93: "CTC_lump_sum",
    94: "housing_benefit",
    69: "SFL_IS",
    70: "SFL_JSA",
    111: "SFL_UC",
    62: "winter_fuel_allowance",
    65: "DWP_IS",
    66: "DWP_JSA",
    110: "DWP_UC",
    24: "FG",
    22: "MG",
    60: "widows_payment",
    98: "DWP_loan",
    99: "LA_loan",
    95: "universal_credit",
    96: "PIP_DL",
    97: "PIP_M",
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


SIMULATED = [
    "working_tax_credit",
    "child_tax_credit",
    "JSA_income",
    "income_support",
    "ESA_income",
    "housing_benefit",
    "pension_credit",
    "universal_credit",
    "child_benefit",
    "child_benefit",
    "AA",
    "DLA_M",
    "DLA_SC",
    "incapacity_benefit",
    "SDA",
    "carers_allowance",
    "BSP",
    "JSA_contrib",
    "ESA_contrib",
    "state_pension",
    "PIP_DL",
    "PIP_M",
    "IIDB",
]

BENUNIT_LEVEL_BENEFITS = [
    "working_tax_credit",
    "child_tax_credit",
    "JSA_income",
    "ESA_income",
    "income_support",
    "housing_benefit",
    "pension_credit",
    "universal_credit",
    "child_benefit",
]


class Benefit(Table):
    enums = {}
    entity = [Person, BenUnit]
    filename = "benefits.tab"
    fieldnames = {}
    fieldnames[Person] = [
        benefit + "_reported"
        for benefit in BENEFITS.values()
        if benefit not in BENUNIT_LEVEL_BENEFITS
        and benefit in SIMULATED
        and benefit
    ] + ["ESA_income_reported_personal"]
    fieldnames[BenUnit] = [
        benefit + "_reported"
        for benefit in BENEFITS.values()
        if benefit in BENUNIT_LEVEL_BENEFITS and benefit in SIMULATED
    ]

    @staticmethod
    def parse(person: dict, benunit: dict, line: dict) -> dict:
        code = line["BENEFIT"]
        if code in BENEFITS:
            name = BENEFITS[code]
            amount = line["BENAMT"]
            if code == 5:
                amount = yearly(line["BENAMT"])
            elif code == 14:
                JSA_type = JSA_ESA_TYPES[line["VAR2"]]
                name = name.replace("JSA", f"JSA_{JSA_type}")
            elif code == 16:
                ESA_type = JSA_ESA_TYPES[line["VAR2"]]
                name = name.replace("ESA", f"ESA_{ESA_type}")
            if name in BENUNIT_LEVEL_BENEFITS:
                if name in SIMULATED:
                    benunit[name + "_reported"] = amount
            else:
                if name in SIMULATED:
                    person[name + "_reported"] = amount
            if code == 16:
                person["ESA_income_reported_personal"] = amount
        return person, benunit

