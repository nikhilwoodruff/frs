from frs.table_utils import *


def parse_job(line, person):
    if safe(line["ETYPE"]) == 1:
        person["earnings"] += yearly(safe(line["UGRSPAY\n"]))
        person["pension_deduction"] += yearly(
            safe(line["DEDUC1"], line["UDEDUC1"])
        )
        person["AVC_deductions"] += yearly(
            safe(line["DEDUC2"], line["DEDUC2"])
        )
        person["union_fee_deductions"] += yearly(
            safe(line["DEDUC3"], line["DEDUC3"])
        )
        person["friendly_society_deductions"] += yearly(
            safe(line["DEDUC4"], line["DEDUC4"])
        )
        person["club_deductions"] += yearly(
            safe(line["DEDUC5"], line["DEDUC5"])
        )
        person["loan_repayment_deductions"] += yearly(
            safe(line["DEDUC6"], line["DEDUC6"])
        )
        person["medical_insurance_deductions"] += yearly(
            safe(line["DEDUC7"], line["DEDUC7"])
        )
        person["charity_deductions"] += yearly(
            safe(line["DEDUC8"], line["DEDUC8"])
        )
        person["student_loan_deductions"] += yearly(
            safe(line["DEDUC9"], line["DEDUC9"])
        )
        person["other_deductions"] += yearly(safe(line["DEDOTH"]))
        person["fuel_expenses"] += yearly(line["FUELUAMT"], line["FUELAMT"])
        person["PAYE_deducted"] += yearly(line["PAYE"])

        person["paid_hourly"] = safe(line["HOURLY"]) == 1
        person["basic_hourly_rate"] = safe(line["HRRATE"])

        person["weekly_unpaid_overtime"] += safe(line["UOTHR"])
        person["salary_sacrifice_pension"] += yearly(line["SPNAMT"])
        person["SPP"] += yearly(line["SPPAMT"])
        person["SSP"] += yearly(line["SSPAMT"])
        person["SMP"] += yearly(line["SSPAMT"])
        person["SAP"] += yearly(line["SAPAMT"])
        person["SHPP"] += yearly(line["SHPPAMT"])
    else:
        person["profit"] = yearly(line["SEINCAMT"])
        if safe(line["CHECKTAX"]) == 2:
            person["profit"] += yearly(
                add_up(
                    line,
                    "SEINCAMT",
                    "SENIRAMT",
                    "SETAXAMT",
                    "TAXDAMT",
                    "NIDAMT",
                )
            )
            person["profit"] += safe(line["SENILAMT"])

    person["num_FT_jobs"] += int(safe(line["FTPT"]) == 1)
    person["num_PT_jobs"] += int(safe(line["FTPT"]) == 2)

    return person


JOB_FIELDNAMES = [
    "earnings",
    "profit",
    "pension_deduction",
    "AVC_deductions",
    "union_fee_deductions",
    "friendly_society_deductions",
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
    "NI_lump_sum_reported",
    "salary_sacrifice_pension",
    "SPP",
    "SSP",
    "SMP",
    "SAP",
    "SHPP",
    "weekly_unpaid_overtime",
    "fuel_expenses",
]

JOB_ENUMS = {}
