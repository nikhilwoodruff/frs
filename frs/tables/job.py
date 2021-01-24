from frs.table_utils import *
from datetime import datetime

def parse_job(line, person):
    # gross wage includes benefits and is before deductions
    person["gross_wage"] += yearly(safe(line["GRWAGE"], line["UGROSS"]), from_period=line["GRWAGPD"])
    person["pension_deductions"] += yearly(safe(line["DEDUC1"], line["UDEDUC1"]), from_period=line["GRWAGPD"])
    person["AVC_deductions"] += yearly(safe(line["DEDUC2"], line["DEDUC2"]), from_period=line["GRWAGPD"])
    person["union_fee_deductions"] += yearly(safe(line["DEDUC3"], line["DEDUC3"]), from_period=line["GRWAGPD"])
    person["friendly_soc_deductions"] += yearly(safe(line["DEDUC4"], line["DEDUC4"]), from_period=line["GRWAGPD"])
    person["club_deductions"] += yearly(safe(line["DEDUC5"], line["DEDUC5"]), from_period=line["GRWAGPD"])
    person["loan_repayment_deductions"] += yearly(safe(line["DEDUC6"], line["DEDUC6"]), from_period=line["GRWAGPD"])
    person["medical_insurance_deductions"] += yearly(safe(line["DEDUC7"], line["DEDUC7"]), from_period=line["GRWAGPD"])
    person["charity_deductions"] += yearly(safe(line["DEDUC8"], line["DEDUC8"]), from_period=line["GRWAGPD"])
    person["student_loan_deductions"] += yearly(safe(line["DEDUC9"], line["DEDUC9"]), from_period=line["GRWAGPD"])
    person["other_deductions"] += yearly(safe(line["DEDOTH"]), from_period=line["GRWAGPD"])

    person["num_FT_jobs"] += int(safe(line["FTPT"]) == 1)
    person["num_PT_jobs"] += int(safe(line["FTPT"]) == 2)

    person["paid_hourly"] = safe(line["HOURLY"]) == 1
    person["basic_hourly_rate"] = safe(line["HRRATE"])

    person["NI_reported"] += yearly(line["SENIRAMT"], from_period=line["SENIRPD"]) + yearly(line["NATINS"], from_period=line["GRWAGPD"])
    person["take_home_pay"] += yearly(line["PAYAMT"], from_period=line["PAYPD"])
    person["PAYE_deducted"] += yearly(line["PAYE"], from_period=line["PAYPD"])

    date_format = "%d/%m/%Y"
    a = datetime.strptime(line["SE1"], date_format)
    b = datetime.strptime(line["SE2"], date_format)
    num_days = (b - a).days
    person["gross_profit"] += adjust_period(line["PROFIT1"], period_code=num_days, target_period_code=YEAR, is_day_count=True)

    person["income_tax_reported"] += safe(line["SETAXAMT"]) + yearly(line["TAXDAMT"], from_period=line["TAXDPD"])
    person["NI_lump_sum_reported"] += safe(line["SENIIAMT"]) + safe(line["SENILAMT"])
    if safe(line["PROFIT2"]) == 2:
        person["gross_profit"] *= -1
    
    if safe(line["PROFTAX"]) == 2:
        person["gross_profit"] += person["income_tax_reported"]
    
    if safe(line["PROFNI"]) == 2:
        person["gross_profit"] += person["NI_reported"] + person["NI_lump_sum_reported"]
    
    person["salary_sacrifice_pension"] += yearly(line["SPNAMT"], from_period=line["SPNPD"])
    person["SPP"] += yearly(line["SPPAMT"], from_period=line["GRWAGPD"])
    person["SSP"] += yearly(line["SSPAMT"], from_period=line["GRWAGPD"])
    person["SMP"] += yearly(line["SSPAMT"], from_period=line["GRWAGPD"])
    person["SAP"] += yearly(line["SAPAMT"], from_period=line["GRWAGPD"])
    person["SHPP"] += yearly(line["SHPPAMT"], from_period=line["GRWAGPD"])

    person["weekly_unpaid_overtime"] += safe(line["UOTHR"])

    return person

JOB_FIELDNAMES = [
    "gross_wage",
    "pension_deductions",
    "AVC_deductions",
    "union_fee_deductions",
    "friendly_soc_deductions",
    "club_deductions",
    "loan_repayment_deductions",
    "medical_insurance_deductions",
    "charity_deductions",
    "student_loan_deductions",
    "other_deductions",
    "num_FT_jobs",
    "num_PT_jobs",
    "paid_hourly",
    "basic_hourly_rate",
    "NI_reported",
    "take_home_pay",
    "PAYE_deducted",
    "income_tax_reported",
    "gross_profit",
    "NI_lump_sum_reported",
    "salary_sacrifice_pension",
    "SPP",
    "SSP",
    "SMP",
    "SAP",
    "SHPP",
    "weekly_unpaid_overtime"
]

JOB_ENUMS = {}