from csv import DictReader, DictWriter
from tqdm import tqdm
import os
import shutil

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
    69: "SFL_IS",
    70: "SFL_JSA",
    111: "SFL_UC",
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
    97: "PIP_M"
}

BENEFITS = {code: benefit + "_reported" for code, benefit in BENEFITS.items()}

AGES = [2, 7, 13, 18, 22, 27, 32, 37, 42, 47, 52, 57, 62, 67, 72, 77, 82, 90]

JSA_ESA_TYPES = {
    1: "income",
    2: "income",
    3: "contrib",
    4: "contrib",
    5: "income",
    6: "income"
}

PERSON_FIELDNAMES = [
    "person_id",
    "benunit_id",
    "household_id",
    "role",
    "is_male",
    "age",
    "is_head",
    "salary",
    "deductions",
    "profit",
    "pension_income",
    "total_benefits",
    "interest",
    "assets",
    "maintenance_expense",
    "misc_income",
    "JSA_contrib_eligible",
    "disabled",
    "adult_weight",
    "hours_worked"
] + list(BENEFITS.values())

BENUNIT_FIELDNAMES = [
    "benunit_id",
    "benunit_weight"
]

HOUSEHOLD_FIELDNAMES = [
    "household_id",
    "household_weight",
    "council_tax",
    "housing_costs",
    "service_charges"
]

AVERAGE_COUNCIL_TAX = [
    1114,
    1300,
    1486,
    1671,
    2043,
    2414,
    2786,
    3343,
    3900,
    0
]

def clean_dirs(output_dir):
    """
    Clears the output directory of any existing files.
    """
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

def exists(field):
    """
    Return true if the field is numeric.
    """
    try:
        float(field)
        return True
    except:
        return False

def safe(*backups):
    """
    Attempt to parse a text field as a numeric input.
    """
    for value in backups:
        if exists(value):
            return float(value)
    return 0

def add_up(line, *fieldnames):
    return sum(map(safe, map(lambda fieldname : line[fieldname], fieldnames)))

def init_data(dictionary, fieldnames):
    """
    Initialise a dictionary with fieldnames and zero values.
    """
    for key in fieldnames:
        dictionary[key] = 0

def parse_file(filename, id_func, parse_func, initial_fields=[], data={}, desc=None):
    """
    Read a data file, changing a data dictionary according to specified procedures.
    """
    if desc is None:
        desc = f"Reading {filename}"
    with open(os.path.join("data", filename), encoding="utf-8") as f:
        reader = DictReader(f, fieldnames=next(f).split("\t"), delimiter="\t")
        for line in tqdm(reader, desc=desc):
            identity = id_func(line)
            if identity not in data:
                entity = {field: 0 for field in initial_fields}
            else:
                entity = data[identity]
            try:
                data[identity] = parse_func(line, entity)
            except Exception as e:
                raise e
        return data

def write_file(data, filename, fieldnames):
    """
    Write a data dictionary to a CSV file.
    """
    with open(os.path.join("output", filename), "w+", encoding="utf-8", newline="") as f:
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in tqdm(data.values(), desc=f"Writing {filename} file"):
            for field in fieldnames:
                if field not in item:
                    item[field] = 0
            writer.writerow(item)

def person_id(line):
    return line["sernum"] + "p" + line["PERSON"]

def household_id(line):
    return line["sernum"]

def parse_adult(line, person):
    person["person_id"] = person_id(line)
    person["benunit_id"] = benunit_id(line)
    person["household_id"] = household_id(line)
    person["role"] = "adult"
    person["is_male"] = line["SEX"] == "1"
    person["age"] = AGES[int(line["IAGEGR4"])]
    person["misc_income"] = safe(line["NINRINC"])
    person["hours_worked"] = safe(line["TOTHOURS"])
    person["disabled"] = line["DISACTA1"] == "1"
    person["adult_weight"] = float(line["GROSS4"])
    person["is_head"] = line["COMBID"] == "1"
    return person

def parse_child(line, person):
    person["person_id"] = person_id(line)
    person["benunit_id"] = benunit_id(line)
    person["household_id"] = household_id(line)
    person["role"] = "child"
    person["is_male"] = line["SEX"] == "1"
    person["age"] = AGES[int(line["IAGEGRP"])]
    person["misc_income"] = safe(line["CHRINC"])
    person["disabled"] = line["DISACTC1"] == "1",
    return person

def parse_job(line, person):
    person["salary"] += safe(line["UGROSS"], line["GRWAGE"])
    person["deductions"] += add_up(line, "DEDOTH", "DEDUC1", "DEDUC2", "DEDUC3", "DEDUC4", "DEDUC5", "DEDUC6", "DEDUC7", "DEDUC8", "DEDUC9") - add_up(line, "UMILEAMT", "UMOTAMT")
    person["profit"] += safe(line["PRBEFORE"])
    return person

def parse_account(line, person):
    person["interest"] += safe(line["ACCINT"])
    return person

def parse_asset(line, person):
    person["assets"] += safe(line["HOWMUCHE"], line["HOWMUCH"])
    return person

def parse_maintenance(line, person):
    person["maintenance_expense"] += safe(line["MRUAMT"], line["MRAMT"])
    return person

def parse_benefit(line, person):
    code = int(line["BENEFIT"])
    if code not in BENEFITS:
        return person
    benefit_name = BENEFITS[code]
    amount = safe(line["BENAMT"])
    if code in [5, 6] and line["USUAL"] == "2":
        amount = safe(line["NOTUSAMT"])
    elif code == 30 and (line["PRES"] != "1" or int(safe(line["BENPD"])) >= 90):
        amount = 0
    elif code in [24, 22, 60]:
        amount *= 7 / 365
    elif code in [65, 66, 110] and line["VAR2"] == "1":
        amount = 0
    elif code == 33:
        JSA_type = JSA_ESA_TYPES[int(line["VAR2"])]
        benefit_name = benefit_name.replace("JSA", f"JSA_{JSA_type}")
    elif code == 54:
        ESA_type = JSA_ESA_TYPES[int(line["VAR2"])]
        benefit_name = benefit_name.replace("ESA", f"ESA_{ESA_type}")
    person["total_benefits"] += amount
    person[benefit_name] += amount
    return person

def parse_pension(line, person):
    person["pension_income"] += safe(line["PENPAY"]) + safe(line["PTAMT"])
    return person

def benunit_id(line):
    return line["sernum"] + "b" + line["BENUNIT"]

def parse_benunit(line, benunit):
    benunit["benunit_id"] = benunit_id(line)
    benunit["benunit_weight"] = float(line["GROSS4"])
    return benunit

def parse_household(line, household):
    household["household_id"] = household_id(line)
    band = int(safe(line["CTBAND"]))
    household["council_tax"] = safe(line["CTANNUAL"], AVERAGE_COUNCIL_TAX[band - 1]) / 52
    household["housing_costs"] = safe(line["GBHSCOST"]) + safe(line["NIHSCOST"])
    household["service_charges"] = safe(line["CHRGAMT1"]) + safe(line["CHRGAMT3"]) + safe(line["CHRGAMT4"]) + safe(line["CHRGAMT5"]) + safe(line["CHRGAMT6"]) + safe(line["CHRGAMT7"]) + safe(line["CHRGAMT8"]) + safe(line["CHRGAMT9"]) + safe(line["RTANNUAL"])
    household["household_weight"] = float(line["GROSS4"])
    return household

def get_person_data():
    """
    Return a dictionary of person-level data.
    """
    person_data = parse_file("adult.tab", person_id, parse_adult, initial_fields=PERSON_FIELDNAMES, data={})
    person_data = parse_file("child.tab", person_id, parse_child, initial_fields=PERSON_FIELDNAMES, data=person_data)
    person_data = parse_file("job.tab", person_id, parse_job, initial_fields=PERSON_FIELDNAMES, data=person_data)
    person_data = parse_file("pension.tab", person_id, parse_pension, initial_fields=PERSON_FIELDNAMES, data=person_data)
    person_data = parse_file("benefits.tab", person_id, parse_benefit, initial_fields=PERSON_FIELDNAMES, data=person_data)
    person_data = parse_file("accounts.tab", person_id, parse_account, initial_fields=PERSON_FIELDNAMES, data=person_data)
    person_data = parse_file("assets.tab", person_id, parse_asset, initial_fields=PERSON_FIELDNAMES, data=person_data)
    person_data = parse_file("maint.tab", person_id, parse_maintenance, initial_fields=PERSON_FIELDNAMES, data=person_data)
    write_file(person_data, "person.csv", PERSON_FIELDNAMES)
    benunit_data = parse_file("benunit.tab", benunit_id, parse_benunit, initial_fields=BENUNIT_FIELDNAMES, data={})
    write_file(benunit_data, "benunit.csv", BENUNIT_FIELDNAMES)
    household_data = parse_file("househol.tab", household_id, parse_household, initial_fields=HOUSEHOLD_FIELDNAMES, data={})
    write_file(household_data, "household.csv", HOUSEHOLD_FIELDNAMES)

clean_dirs("output")
get_person_data()