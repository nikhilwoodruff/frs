from frs.table_utils import *

def parse_account(line, person):
    """Parse account.tab values into person-level data.

    Args:
        line (dict): The line to read from
        person (dict): The current person object containin a dictionary for each person

    Returns:
        dict: The person object with the values added
    """
    # account type and income
    account_type = ACCOUNT_TYPES[safe(line["ACCOUNT"])]
    account_income = yearly(line["ACCINT"])
    person[account_type + "_income"] = account_income

    # tax status
    # ACCTAX and INVTAX presence is mutually exclusive
    pre_tax_code = add_up(line, "ACCTAX", "INVTAX")
    if pre_tax_code != POST_TAX_CODE:
        pre_tax = True
    else:
        pre_tax = False
    person[account_type + "_pre_tax"] = pre_tax

    # National Savings value
    NS_value = NS_MEAN_VALUES[safe(line["NSAMT"])]
    person["NS_value"] = NS_value

    return person


ACCOUNT_TYPES = {
    1: "current_account",
    2: "NSI_direct_saver",
    3: "NSI_investment",
    5: "savings_and_investment",
    6: "GGES",
    7: "unit_or_inv_trusts",
    8: "stocks_and_shares",
    9: "PEP",
    10: "NS_capital_bonds",
    11: "ILNSC",
    12: "FINSC",
    13: "PGB",
    14: "SAYE",
    15: "premium_bonds",
    16: "NS_income_bonds",
    17: "NS_deposit_bonds",
    18: "first_option_bonds",
    19: "yearly_plan",
    21: "ISA",
    22: "profit_sharing",
    23: "CSOP",
    24: "member_of_share_club",
    25: "guaranteed_income",
    26: "GEB",
    27: "basic_account",
    28: "credit_unions",
    29: "EPNL",
    30: "post_office_card_account"
}

POST_TAX_CODE = 1

NS_VALUE_BOUNDS = {
    NO_DATA: (0, 0),
    1: (1, 50),
    2: (51, 100),
    3: (101, 250),
    4: (251, 500),
    5: (501, 1000),
    6: (1001, 2000),
    7: (2001, 3000),
    8: (3001, 5000),
    9: (5001, 10000),
    10: (10001, 20000),
    11: (20001, 30000),
    12: (30001, 30001)
}

NS_MEAN_VALUES = {x: (y[0] + y[1]) / 2 for x, y in NS_VALUE_BOUNDS.items()}

ACCOUNTS_FIELDNAMES = list(map(lambda x : x + "_income", ACCOUNT_TYPES.values())) + list(map(lambda x : x + "_pre_tax", ACCOUNT_TYPES.values())) + ["NS_value"]

ACCOUNTS_ENUMS = {}