

def parse_adult(line, person):
    person["person_id"] = person_id(line)
    person["is_adult"] = True
    person["is_child"] = False
    person["benunit_id"] = benunit_id(line)
    person["household_id"] = household_id(line)
    person["adult_weight"] = safe(line["GROSS4"])
    person["role"] = "adult"
    person["earnings"] = adjust_period(line["INEARNS"])
    person["pension_income"] = adjust_period(line["INPENINC"])
    person["age"] = safe(line["AGE80"])
    person["care_hours"] = CARE_HOURS_CODES[safe(line["HOURTOT"])]
    person["hours"] = safe(line["TOTHOURS"])
    person["savings_interest"] = adjust_period(line["ININV"])
    person["misc_income"] = adjust_period(line["INRINC"])
    person["total_benefits"] = adjust_period(add_up(
        line, "INDISBEN", "INOTHBEN", "INTXCRED", "INDUC"
    ))
    person["is_household_head"] = int(line["PERSON"]) == 1
    person["is_benunit_head"] = int(line["UPERSON"]) == 1
    person["FRS_net_income"] = (
        adjust_period(safe(line["NINDINC"]))
        - person["misc_income"]
    )
    person["student_loan_repayment"] = adjust_period(line["SLREPAMT"])
    person["registered_disabled"] = safe(line["LAREG"]) == 1
    person["dis_equality_act_core"] = safe(line["DISCORA1"]) == 1
    person["dis_equality_act_wider"] = safe(line["DISACTA1"]) == 1
    return person


def parse_childcare(line, person):
    if line["REGISTRD"] == "1":
        person["childcare"] += adjust_period(safe(line["CHAMT"]))
    return person


def parse_child(line, person):
    person["person_id"] = person_id(line)
    person["is_adult"] = False
    person["is_child"] = True
    person["benunit_id"] = benunit_id(line)
    person["household_id"] = household_id(line)
    person["role"] = "child"
    person["age"] = safe(line["AGE"])
    person["misc_income"] = adjust_period(line["CHRINC"])
    person["earnings"] = adjust_period(line["CHEARNS"])
    person["FRS_net_income"] = adjust_period(line["CHINCDV"]) - adjust_period(person["misc_income"])
    person["registered_disabled"] = safe(line["LAREG"]) == 1
    person["dis_equality_act_core"] = safe(line["DISCORC1"]) == 1
    person["dis_equality_act_wider"] = safe(line["DISACTC1"]) == 1
    person["is_benunit_head"] = False
    person["is_household_head"] = False
    return person


def parse_job(line, person):
    person["profit"] += adjust_period(line["SEINCAMT"])
    return person



def parse_asset(line, person):
    return person


def parse_maintenance(line, person):
    person["maintenance_payments"] = adjust_period(safe(line["MRUAMT"], line["MRAMT"]))
    return person


def parse_benefit(line, person, benunit):
    code = safe(int(line["BENEFIT"]))
    if code in BENEFITS:
        name = BENEFITS[code]
        amount = safe(line["BENAMT"])
        if code == 5:
            amount = safe(line["BENAMT"])
        elif code == 14:
            JSA_type = JSA_ESA_TYPES[int(safe(line["VAR2"]))]
            name = name.replace("JSA", f"JSA_{JSA_type}")
        elif code == 16:
            ESA_type = JSA_ESA_TYPES[int(safe(line["VAR2"]))]
            name = name.replace("ESA", f"ESA_{ESA_type}")
        if name in BENUNIT_LEVEL_BENEFITS:
            if name in SIMULATED:
                benunit[name + "_reported"] = adjust_period(amount)
        else:
            if name in SIMULATED:
                person[name + "_reported"] = adjust_period(amount)
        if code == 16:
            person["ESA_income_reported_personal"] = adjust_period(amount)
    return person, benunit


def parse_pension(line, person):
    return person


def benunit_id(line):
    return 1000000 + int(line["sernum"]) * 10 + int(line["BENUNIT"])


def parse_benunit(line, benunit):
    benunit["benunit_id"] = benunit_id(line)
    benunit["benunit_weight"] = float(line["GROSS4"])
    return benunit


def parse_household(line, household):
    household["household_id"] = household_id(line)
    household["household_weight"] = float(line["GROSS4"])
    household["country"] = COUNTRY[safe(line["COUNTRY"])]
    household["num_rooms"] = safe(line["ROOMS10"])
    household["rent"] = adjust_period(line["HHRENT"])
    household["is_shared"] = safe(line["HHSTAT"]) == 2
    household["housing_costs"] = adjust_period(line["GBHSCOST"]) + safe(
        line["NIHSCOST"]
    )
    band = int(safe(line["CTBAND"]))
    household["council_tax"] = safe(
        line["CTANNUAL"], AVERAGE_COUNCIL_TAX[band - 1]
    )
    household["is_social"] = safe(line["PTENTYP2"]) in [1, 2]
    household["region"] = REGIONS_TO_NUM[GOVTREGNO[int(line["GVTREGNO"])]]
    return household


def parse_extchild(line, benunit):
    return benunit

def write_files():
    """
    Write OpenFisca-UK input CSV files.
    """
    person_data = parse_file(
        "adult.tab",
        person_id,
        parse_adult,
        initial_fields=PERSON_FIELDNAMES,
        data={},
    )
    benunit_data = parse_file(
        "benunit.tab",
        benunit_id,
        parse_benunit,
        initial_fields=BENUNIT_FIELDNAMES,
        data={},
    )
    person_data = parse_file(
        "child.tab",
        person_id,
        parse_child,
        initial_fields=PERSON_FIELDNAMES,
        data=person_data,
    )
    person_data = parse_file(
        "job.tab",
        person_id,
        parse_job,
        initial_fields=PERSON_FIELDNAMES,
        data=person_data,
    )
    person_data = parse_file(
        "pension.tab",
        person_id,
        parse_pension,
        initial_fields=PERSON_FIELDNAMES,
        data=person_data,
    )
    person_data, benunit_data = parse_file(
        "benefits.tab",
        (person_id, benunit_id),
        parse_benefit,
        initial_fields=PERSON_FIELDNAMES,
        data=(person_data, benunit_data),
        multiple_levels=True,
    )
    person_data = parse_file(
        "accounts.tab",
        person_id,
        parse_account,
        initial_fields=PERSON_FIELDNAMES,
        data=person_data,
    )
    person_data = parse_file(
        "assets.tab",
        person_id,
        parse_asset,
        initial_fields=PERSON_FIELDNAMES,
        data=person_data,
    )
    person_data = parse_file(
        "maint.tab",
        person_id,
        parse_maintenance,
        initial_fields=PERSON_FIELDNAMES,
        data=person_data,
    )
    person_data = parse_file(
        "chldcare.tab",
        person_id,
        parse_childcare,
        initial_fields=PERSON_FIELDNAMES,
        data=person_data,
    )
    write_file(person_data, "person.csv", PERSON_FIELDNAMES)
    benunit_data = parse_file(
        "extchild.tab",
        benunit_id,
        parse_extchild,
        initial_fields=BENUNIT_FIELDNAMES,
        data=benunit_data,
    )
    write_file(benunit_data, "benunit.csv", BENUNIT_FIELDNAMES)
    household_data = parse_file(
        "househol.tab",
        household_id,
        parse_household,
        initial_fields=HOUSEHOLD_FIELDNAMES,
        data={},
    )
    write_file(household_data, "household.csv", HOUSEHOLD_FIELDNAMES)
    with open(resolve("metadata.json"), "w+") as f:
        json.dump(dict(version=__version__), f)
