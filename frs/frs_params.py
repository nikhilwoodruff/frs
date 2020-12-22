CARE_HOURS_CODES = {
    0: 0,
    1: 2,
    2: 7,
    3: 14,
    4: 27,
    5: 44,
    6: 70,
    7: 100,
    8: 10,
    9: 30,
    10: 35,
}

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

COUNTRY = {1: "ENGLAND", 2: "WALES", 3: "SCOTLAND", 4: "NI"}

WEEK = 1
MONTH = 5
YEAR = 52

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


PERSON_FIELDNAMES = [
    "person_id",
    "benunit_id",
    "household_id",
    "role",
    "adult_weight",
    "earnings",
    "profit",
    "childcare",
    "pension_income",
    "age",
    "care_hours",
    "hours",
    "savings_interest",
    "misc_income",
    "total_benefits",
    "is_household_head",
    "is_benunit_head",
    "FRS_net_income",
    "maintenance_payments",
    "student_loan_repayment",
    "is_adult",
    "is_child",
    "registered_disabled",
    "dis_equality_act_core",
    "dis_equality_act_wider",
    "ESA_income_reported_personal"
] + [
    benefit + "_reported"
    for benefit in BENEFITS.values()
    if benefit not in BENUNIT_LEVEL_BENEFITS
    and benefit in SIMULATED
    and benefit
]

BENUNIT_FIELDNAMES = ["benunit_id", "benunit_weight"] + [
    benefit + "_reported"
    for benefit in BENEFITS.values()
    if benefit in BENUNIT_LEVEL_BENEFITS and benefit in SIMULATED
]

HOUSEHOLD_FIELDNAMES = [
    "household_id",
    "household_weight",
    "country",
    "rent",
    "is_shared",
    "housing_costs",
    "is_social",
    "num_rooms",
    "region",
    "council_tax",
]

PERIOD_CODES = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 4.35,
    7: 8.7,
    8: 6.52,
    9: 5.8,
    10: 5.22,
    13: 13,
    17: 17.4,
    26: 26,
    52: 52,
    90: 0.5,
    95: 1000,
    97: 1000,
}

GOVTREGNO = {
    1: "NORTH_EAST",
    2: "NORTH_WEST",
    4: "YORKSHIRE",
    5: "EAST_MIDLANDS",
    6: "WEST_MIDLANDS",
    7: "EAST_OF_ENGLAND",
    8: "LONDON",
    9: "SOUTH_EAST",
    10: "SOUTH_WEST",
    11: "WALES",
    12: "SCOTLAND",
    13: "NORTHERN_IRELAND",
}

REGIONS_TO_NUM = {
    region: i for region, i in zip(GOVTREGNO.values(), range(len(GOVTREGNO)))
}

AVERAGE_COUNCIL_TAX = [1114, 1300, 1486, 1671, 2043, 2414, 2786, 3343, 3900, 0]
