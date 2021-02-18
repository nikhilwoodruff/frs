from csv import DictReader, DictWriter
from tqdm import tqdm
import os
import shutil
import numpy as np
from frs import tables
from frs import table_utils
import sys
import pandas as pd
import argparse
from colorama import init, Fore
from termcolor import colored
import json
import warnings
import webbrowser
from frs.post_processing import run_adjustments

init()

__version__ = "0.1.0"


def clean_dirs(output_dir):
    """
    Clears the output directory of any existing files.
    """
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)


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


def resolve(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def ensure_folders_exist():
    path = os.path.dirname(__file__)
    if "csv" not in os.listdir(path):
        os.makedirs(os.path.join(path, "csv"))
    if "raw" not in os.listdir(path):
        os.makedirs(os.path.join(path, "raw"))

def encode_enums(data, name):
    for record in tqdm(data.values(), desc=f"Encoding enums for {name}s"):
        for field in record:
            if field in tables.COMBINED_ENCODE:
                record[field] = tables.COMBINED_ENCODE[field][record[field]]

def write_files(decode_enums=False):
    """
    Write OpenFisca-UK input CSV files.
    """
    person_data, benunit_data, household_data = {}, {}, {}
    data = dict(
        person=person_data, benunit=benunit_data, household=household_data
    )
    for filename in os.listdir(resolve("raw")):
        name = filename.replace(".tab", "")
        if name in tables.parse_func:
            if name in table_utils.PERSON_LEVEL_FILES:
                entity = "person"
                id_func = table_utils.person_id
                initial_fields = tables.PERSON_FIELDNAMES
            elif name in table_utils.BENUNIT_LEVEL_FILES:
                entity = "benunit"
                id_func = table_utils.benunit_id
                initial_fields = tables.BENUNIT_FIELDNAMES
            else:
                entity = "household"
                id_func = table_utils.household_id
                initial_fields = tables.HOUSEHOLD_FIELDNAMES
            parse_function = tables.parse_func[name]
            data[entity] = parse_file(
                filename,
                id_func,
                parse_function,
                initial_fields=initial_fields,
                data=data[entity],
            )
    
    if not decode_enums:
        for entity, entity_data in data.items():
            encode_enums(entity_data, entity)
        
        with open(resolve("key.json"), "w+") as f:
            json.dump(tables.COMBINED_DECODE, f)

    write_file(person_data, "person.csv", tables.PERSON_FIELDNAMES)
    write_file(benunit_data, "benunit.csv", tables.BENUNIT_FIELDNAMES)
    write_file(household_data, "household.csv", tables.HOUSEHOLD_FIELDNAMES)

    run_adjustments()


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
        webbrowser.open("file:///" + resolve("."))


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


if __name__ == "__main__":
    main()
