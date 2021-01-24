import os

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
    95: 52,
    97: 1000,
}

def resolve(filename):
    return os.path.join(os.path.dirname(__file__), filename)

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


def add_up(line, *fieldnames):
    """Attempts to add up a list of fieldnames

    Args:
        line (dict): The row containing the fields

    Returns:
        float: The sum of valid fields
    """
    return sum(map(safe, map(lambda fieldname: line[fieldname], fieldnames)))


def adjust_period(value, period_code, target_period_code, is_day_count=False):
    """Adjusts a value from one period to another

    Args:
        value (float): The value
        period_code (int, optional): The original period code.
        target_period_code (int, optional): The target period code.

    Returns:
        float: The adjusted value
    """
    if safe(value) == 0:
        return 0
    if period_code == 0:
        period_code = 1
    if period_code not in PERIOD_CODES or target_period_code not in PERIOD_CODES:
        print("Warning: missing valid period code, writing as 0.")
        return 0
    if is_day_count:
        relative_size = PERIOD_CODES[target_period_code] / target_period_code
    else:
        if period_code != 97:
            period_code = WEEK
        relative_size = (
            PERIOD_CODES[target_period_code] / PERIOD_CODES[period_code]
        )
    return safe(value) * relative_size

def yearly(value, from_period=WEEK):
    return adjust_period(value, period_code=safe(from_period), target_period_code=YEAR)

# Recognising an ID:
# First digit: 1=person, 2=benunit, 3=household
# Digits 2-(n-1): household id
# Last digit: entity index within household

def person_id(line):
    return 1000000 + int(line["sernum"]) * 10 + int(line["PERSON"])

def benunit_id(line):
    return 2000000 + int(line["sernum"]) * 10 + int(line["BENUNIT"])

def household_id(line):
    return 3000000 + int(line["sernum"]) * 10

NO_DATA = 0

HOURS_CODES_BOUNDS = {
    NO_DATA: (0, 0),
    1: (0, 4),
    2: (5, 9),
    3: (10, 19),
    4: (20, 34),
    5: (35, 49),
    6: (50, 99),
    7: (100, 100),
    8: (0, 20),
    9: (20, 34),
    10: (35, 35)
}

HOURS_CODES_MEAN_VALUES = {x: (y[0] + y[1]) / 2 for x, y in HOURS_CODES_BOUNDS.items()}

PERSON_LEVEL_FILES = [
    "adult",
    "accounts",
    "assets",
    "benefits",
    "child",
    "chldcare",
    "govpay",
    "job",
    "maint",
    "oddjob",
    "penprov",
    "pension",
]

BENUNIT_LEVEL_FILES = [
    "benunit",
    "care",
    "extchild"
]

HOUSEHOLD_LEVEL_FILES = [
    "endowmnt",
    "household",
    "mortcont",
    "mortgage",
    "owner",
    "rentcont",
    "renter"
]