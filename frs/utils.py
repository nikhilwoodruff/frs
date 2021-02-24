import os
import shutil
from pathlib import Path

WEEK = 1
MONTH = 5
YEAR = 52

PERIOD_CODES = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 4.35,
    7: 8.7,
    8: 6.52,
    9: 5.8,
    10: 5.22,
    13: 13,
    17: 17.4,
    26: 26,
    52: 52,
    90: 0.5,
    95: 1000,
    97: 1000,
}

def exists(field):
    """Determines if there is a numeric value in the field

    Args:
        field (str): The field

    Returns:
        bool: Whether the field is numeric
    """
    try:
        float(field)
        return True
    except:
        return False


def safe(*backups):
    """Attempts to parse a field, with a list of backups

    Returns:
        float: The numeric result
    """
    for value in backups:
        if exists(value):
            return float(value)
    return 0


def add(line, *fieldnames):
    """Attempts to add up a list of fieldnames

    Args:
        line (dict): The row containing the fields

    Returns:
        float: The sum of valid fields
    """
    return sum(map(safe, map(lambda fieldname: line[fieldname], fieldnames)))

PERIOD_CODES = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 4.35,
    7: 8.7,
    8: 6.52,
    9: 5.8,
    10: 5.22,
    13: 13,
    17: 17.4,
    26: 26,
    52: 52,
    90: 0.5,
    95: 1000,
    97: 1000,
}

WEEK = 1
MONTH = 5
YEAR = 52


def adjust_period(value, period_code=WEEK, target_period_code=YEAR):
    """Adjusts a value from one period to another

    Args:
        value (float): The value
        period_code (int, optional): The original period code. Defaults to WEEK.
        target_period_code (int, optional): The target period code. Defaults to YEAR.

    Returns:
        float: The adjusted value
    """
    relative_size = (
        PERIOD_CODES[target_period_code] / PERIOD_CODES[period_code]
    )
    return value * relative_size

def yearly(value):
    return adjust_period(value, WEEK, YEAR)

def resolve(filename):
    return Path(os.path.dirname(__file__)) /  filename

def clean_dirs(output_dir):
    """
    Clears the output directory of any existing files.
    """
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

def ensure_folders_exist():
    path = os.path.dirname(__file__)
    if "csv" not in os.listdir(path):
        os.makedirs(os.path.join(path, "csv"))
    if "tab" not in os.listdir(path):
        os.makedirs(os.path.join(path, "tab"))