from frs.frs_params import *

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


def adjust_period(value, period_code=WEEK, target_period_code=YEAR):
    """Adjusts a value from one period to another

    Args:
        value (float): The value
        period_code (int, optional): The original period code. Defaults to WEEK.
        target_period_code (int, optional): The target period code. Defaults to YEAR.

    Returns:
        float: The adjusted value
    """
    if not exists(value) or not exists(period_code):
        return 0
    relative_size = (
        PERIOD_CODES[target_period_code] / PERIOD_CODES[period_code]
    )
    return float(value) * relative_size

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

def parse_account(line, person):
    return person