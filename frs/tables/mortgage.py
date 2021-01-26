from frs.table_utils import *


def parse_mortgage(line, household):
    household["original_mortgage_amount"] = safe(line["BORRAMT"])
    household["MPP"] = yearly(
        safe(line["INCMPAM1"])
        + safe(line["INCMPAM2"])
        + safe(line["INCMPAM3"])
    )
    household["mortgage_payments"] = yearly(line["INTPRPAY"]) + yearly(
        line["MORINPAY"]
    )
    household["outstanding_mortgage"] = safe(line["MORTLEFT"])
    household["mortgage_term"] = safe(line["MORTEND"])
    household["mortgage_types"] = MORTGAGE_TYPES[safe(line["MORTTYPE"])]
    household["remortgage_amount"] = safe(line["RMAMT"])
    return household


MORTGAGE_TYPES = {
    NO_DATA: "repayment",
    1: "endowment",
    2: "repayment",
    3: "pension",
    4: "ISA",
    5: "endowment_and_repayment",
    6: "interest_only_inv_linked",
    7: "interest_only_non_inv_linked",
    8: "other",
}

MORTGAGE_FIELDNAMES = [
    "original_mortgage_amount",
    "MPP",
    "mortgage_payments",
    "outstanding_mortgage",
    "mortgage_term",
    "mortgage_types",
    "remortgage_amount",
]

MORTGAGE_ENUMS = dict(mortgage_type=MORTGAGE_TYPES)
