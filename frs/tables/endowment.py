from frs.table_utils import *

def parse_endowment(line, household):
    household["endowment_premium"] = yearly(line["MENPOLAM"], from_period=line["MENPOLPD"])
    return household

ENDOWMENT_FIELDNAMES = ["endowment_premium"]

ENDOWMENT_ENUMS = {}