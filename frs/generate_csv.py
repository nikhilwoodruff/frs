from csv import DictReader, DictWriter
from tqdm import tqdm
import os
import shutil
import numpy as np
from frs.frs_params import *
import sys
import pandas as pd
import argparse
from colorama import init, Fore
from termcolor import colored
import json
import warnings
import webbrowser

init()

__version__ = "0.1.0"


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
    return sum(map(safe, map(lambda fieldname: line[fieldname], fieldnames)))


def adjust_period(value, period_code=WEEK, target_period_code=YEAR):
    if not exists(value) or not exists(period_code):
        return 0
    relative_size = (
        PERIOD_CODES[target_period_code] / PERIOD_CODES[period_code]
    )
    return float(value) * relative_size


def init_data(dictionary, fieldnames):
    """
    Initialise a dictionary with fieldnames and zero values.
    """
    for key in fieldnames:
        dictionary[key] = 0


def parse_file(
    filename,
    id_func,
    parse_func,
    initial_fields=[],
    data={},
    desc=None,
    multiple_levels=False,
):
    """
    Read a data file, changing a data dictionary according to specified procedures.
    """
    if desc is None:
        desc = f"Reading {filename}"
    with open(os.path.join(resolve("raw"), filename), encoding="utf-8") as f:
        reader = DictReader(f, fieldnames=next(f).split("\t"), delimiter="\t")
        for line in tqdm(reader, desc=desc):
            if multiple_levels:
                identity = [func(line) for func in id_func]
            else:
                identity = id_func(line)
            if multiple_levels:
                entities = []
                for dat, ident in zip(data, identity):
                    if ident not in dat or dat[ident] is None:
                        entity = {field: 0 for field in initial_fields}
                    else:
                        entity = dat[ident]
                    entities += [entity]
                entity = entities
            else:
                if identity not in data or data[identity] is None:
                    entity = {field: 0 for field in initial_fields}
                else:
                    entity = data[identity]
            try:
                if multiple_levels:
                    dat = parse_func(line, *entity)
                    for i, level_identity, level_dat in zip(
                        range(len(data)), identity, dat
                    ):
                        data[i][level_identity] = level_dat
                else:
                    data[identity] = parse_func(line, entity)
            except Exception as e:
                raise e
        return data


def write_file(data, filename, fieldnames):
    """
    Write a data dictionary to a CSV file.
    """
    with open(
        os.path.join(resolve("csv"), filename),
        "w+",
        encoding="utf-8",
        newline="",
    ) as f:
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in tqdm(data.values(), desc=f"Writing {filename} file"):
            for field in fieldnames:
                if field not in item:
                    item[field] = 0
            writer.writerow(item)


def person_id(line):
    return 1000000 + int(line["sernum"]) * 10 + int(line["PERSON"])


def household_id(line):
    return 1000000 + int(line["sernum"]) * 10


def parse_adult(line, person):
    person["person_id"] = person_id(line)
    person["is_adult"] = True
    person["is_child"] = False
    person["benunit_id"] = benunit_id(line)
    person["household_id"] = household_id(line)
    person["adult_weight"] = safe(line["GROSS4"])
    person["role"] = "adult"
    person["earnings"] = adjust_period(line["INEARNS"], WEEK, YEAR)
    person["profit"] = adjust_period(line["SEINCAM2"], WEEK, YEAR)
    person["pension_income"] = adjust_period(line["INPENINC"], WEEK, YEAR)
    person["age"] = safe(line["AGE80"])
    person["care_hours"] = CARE_HOURS_CODES[safe(line["HOURTOT"])]
    person["hours"] = safe(line["TOTHOURS"])
    person["savings_interest"] = adjust_period(line["ININV"], WEEK, YEAR)
    person["misc_income"] = adjust_period(line["INRINC"], WEEK, YEAR)
    person["total_benefits"] = add_up(
        line, "INDISBEN", "INOTHBEN", "INTXCRED", "INDUC"
    )
    person["is_household_head"] = int(line["PERSON"]) == 1
    person["is_benunit_head"] = int(line["UPERSON"]) == 1
    person["FRS_net_income"] = (
        adjust_period(safe(line["NINDINC"]), WEEK, YEAR)
        - person["misc_income"]
    )
    person["student_loan_repayment"] = safe(line["SLREPAMT"])
    person["registered_disabled"] = safe(line["LAREG"]) == 1
    person["dis_equality_act_core"] = safe(line["DISCORA1"]) == 1
    person["dis_equality_act_wider"] = safe(line["DISACTA1"]) == 1
    return person


def parse_childcare(line, person):
    if line["REGISTRD"] == "1":
        person["childcare"] += safe(line["CHAMT"])
    return person


def parse_child(line, person):
    person["person_id"] = person_id(line)
    person["is_adult"] = False
    person["is_child"] = True
    person["benunit_id"] = benunit_id(line)
    person["household_id"] = household_id(line)
    person["role"] = "child"
    person["age"] = safe(line["AGE"])
    person["misc_income"] = adjust_period(line["CHRINC"], WEEK, YEAR)
    person["earnings"] = adjust_period(line["CHEARNS"], WEEK, YEAR)
    person["FRS_net_income"] = safe(line["CHINCDV"]) - person["misc_income"]
    person["registered_disabled"] = safe(line["LAREG"]) == 1
    person["dis_equality_act_core"] = safe(line["DISCORC1"]) == 1
    person["dis_equality_act_wider"] = safe(line["DISACTC1"]) == 1
    person["is_benunit_head"] = False
    person["is_household_head"] = False
    return person


def parse_job(line, person):
    return person


def parse_account(line, person):
    return person


def parse_asset(line, person):
    return person


def parse_maintenance(line, person):
    person["maintenance_payments"] = safe(line["MRUAMT"], line["MRAMT"])
    return person


def parse_benefit(line, person, benunit):
    code = safe(int(line["BENEFIT"]))
    if code in BENEFITS:
        name = BENEFITS[code]
        amount = safe(line["BENAMT"])
        if code == 5:
            amount = adjust_period(safe(line["BENAMT"]), WEEK, YEAR)
        elif code == 14:
            JSA_type = JSA_ESA_TYPES[int(safe(line["VAR2"]))]
            name = name.replace("JSA", f"JSA_{JSA_type}")
        elif code == 16:
            ESA_type = JSA_ESA_TYPES[int(safe(line["VAR2"]))]
            name = name.replace("ESA", f"ESA_{ESA_type}")
        if name in BENUNIT_LEVEL_BENEFITS:
            if name in SIMULATED:
                benunit[name + "_reported"] = amount
        else:
            if name in SIMULATED:
                person[name + "_reported"] = amount
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
    household["rent"] = safe(line["HHRENT"])
    household["is_shared"] = safe(line["HHSTAT"]) == 2
    household["housing_costs"] = safe(line["GBHSCOST"]) + safe(
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


def resolve(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def ensure_folders_exist():
    path = os.path.dirname(__file__)
    if "csv" not in os.listdir(path):
        os.makedirs(os.path.join(path, "csv"))
    if "raw" not in os.listdir(path):
        os.makedirs(os.path.join(path, "raw"))


def main():
    ensure_folders_exist()
    existing_raw = os.listdir(resolve("raw"))
    existing_csv = os.listdir(resolve("csv"))
    parser = argparse.ArgumentParser(
        description="Utility for managing Family Resources Survey microdata"
    )
    parser.add_argument(
        "mode",
        choices=["status", "gen", "regen", "show"],
        help="The action to take on stored data",
    )
    parser.add_argument(
        "--path", required=False, help="The path to the FRS data"
    )
    args = parser.parse_args()
    if args.mode == "status":
        print("FRS status:")
        print("\tFRS TAB files stored?\t\t\t\t", end="")
        if existing_raw:
            print(colored("Yes", "green"))
        else:
            print(colored("No", "red"))
        print("\tFRS OpenFisca-UK input files generated?\t\t", end="")
        if existing_csv:
            print(colored("Yes", "green"))
        else:
            print(colored("No", "red"))
        print("\tOpenFisca-UK input files outdated?\t\t", end="")
        if existing_csv:
            current_version = __version__
            with open(resolve("metadata.json"), "r") as f:
                gen_version = json.load(f)["version"]
            outdated = current_version != gen_version
            if not outdated:
                print(
                    colored("No", "green")
                    + f" (files generated with current version, {current_version})"
                )
            else:
                print(
                    colored("Yes", "red")
                    + f" (generated with {gen_version}, current is {current_version})"
                )
        else:
            print(colored("N/A", "yellow"))
    elif args.mode == "gen":
        if not args.path or not os.path.exists(args.path):
            print("Please specify a valid path to FRS TAB files.")
            return
        filenames = [
            filename
            for filename in os.listdir(args.path)
            if filename[-4:].lower() == ".tab"
        ]
        if not filenames:
            print("No FRS files were found.")
            return
        for filename in tqdm(filenames, desc="Storing FRS files"):
            shutil.copyfile(
                os.path.join(args.path, filename),
                os.path.join(resolve("raw"), filename),
            )
        print("Stored FRS source files successfully.")
        print("Generating OpenFisca-UK input datasets:")
        write_files()
        print("Completed generation.")
    elif args.mode == "regen":
        if not existing_raw:
            print(
                "No FRS source data stored; use 'frs gen --path [PATH]' to load it."
            )
            return
        print("Re-generating OpenFisca-UK input datasets:")
        write_files()
        print("Completed generation.")
    elif args.mode == "show":
        webbrowser.open('file:///' + resolve("."))


def load():
    ensure_folders_exist()
    if not os.listdir(resolve("csv")) and not os.listdir(resolve("raw")):
        raise Exception(
            "No OpenFisca-UK input files found, and no FRS source data found either. Load the TAB files with 'frs [PATH]'."
        )
    elif not os.listdir(resolve("csv")):
        raise warnings.warn(
            "No OpenFisca-UK-compatible data files found, regenerating from FRS TAB sources."
        )
        write_files()
    return [
        pd.read_csv(resolve(os.path.join("csv", filename)), low_memory=False)
        for filename in ("person.csv", "benunit.csv", "household.csv")
    ]
