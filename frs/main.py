from csv import DictWriter
from frs.utils import resolve, clean_dirs, ensure_folders_exist
import os
import argparse
from colorama import init, Fore
from termcolor import colored
import webbrowser
import json
import warnings
from tqdm import tqdm
import shutil
from pathlib import Path
from frs.dataset import Dataset
from frs.tables import tables
import pandas as pd

__version__ = "0.2.0"


def get_args():
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
    return args


def run_status():
    tab_files = os.listdir(resolve("tab"))
    csv_files = os.listdir(resolve("csv"))
    print("FRS status:")
    print("\tFRS TAB files stored?\t\t\t\t", end="")
    if tab_files:
        print(colored("Yes", "green"))
    else:
        print(colored("No", "red"))
    print("\tFRS OpenFisca-UK input files generated?\t\t", end="")
    if csv_files:
        print(colored("Yes", "green"))
    else:
        print(colored("No", "red"))
    print("\tOpenFisca-UK input files outdated?\t\t", end="")
    if csv_files:
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


def import_files(path: Path):
    filenames = [
        filename
        for filename in os.listdir(path)
        if filename[-4:].lower() == ".tab"
    ]
    if not filenames:
        print("No FRS files were found.")
        return
    for filename in tqdm(filenames, desc="Storing FRS files"):
        shutil.copyfile(
            path / filename,
            resolve("tab") / filename,
        )
    print("Stored FRS source files successfully.")


def generate_csv(path: Path = resolve("tab")):
    dataset = Dataset(tables)
    entity_data, fieldnames = dataset.parse()
    for entity, data in entity_data.items():
        name = entity.__name__.lower() + ".csv"
        with open(
            resolve("csv") / name, "w", encoding="utf-8", newline=""
        ) as f:
            writer = DictWriter(f, fieldnames=fieldnames[entity])
            writer.writeheader()
            for item in tqdm(data.entries.values(), desc=f"Writing {name}"):
                for field in fieldnames[entity]:
                    if field not in item:
                        item[field] = 0
                writer.writerow(item)
    with open(resolve("metadata.json"), "w+") as f:
        json.dump(dict(version=__version__), f)


def main():
    ensure_folders_exist()
    args = get_args()
    if args.mode == "status":
        run_status()
    elif args.mode == "gen":
        if not args.path or not os.path.exists(args.path):
            print("Please specify a valid path to FRS TAB files.")
            return
        path = Path(args.path)
        import_files(path)
        print("Generating OpenFisca-UK input datasets:")
        generate_csv(path)
        print("Completed generation.")
    elif args.mode == "regen":
        tab_files = os.listdir(resolve("tab"))
        if not tab_files:
            print(
                "No FRS source data stored; use 'frs gen --path [PATH]' to load it."
            )
            return
        print("Re-generating OpenFisca-UK input datasets:")
        generate_csv()
        print("Completed generation.")
    elif args.mode == "show":
        webbrowser.open("file:///" + resolve("."))


def load():
    ensure_folders_exist()
    if not os.listdir(resolve("csv")) and not os.listdir(resolve("tab")):
        raise Exception(
            "No OpenFisca-UK input files found, and no FRS source data found either. Load the TAB files with 'frs gen --path [PATH]'."
        )
    elif not os.listdir(resolve("csv")):
        raise warnings.warn(
            "No OpenFisca-UK-compatible data files found, regenerating from FRS TAB sources."
        )
        generate_csv()
    return [
        pd.read_csv(resolve(os.path.join("csv", filename)), low_memory=False)
        for filename in ("person.csv", "benunit.csv", "household.csv")
    ]
