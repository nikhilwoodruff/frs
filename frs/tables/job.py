from frs.dataset import Table, Person, BenUnit, Household
from frs.utils import yearly, add


class Job(Table):
    enums = {}
    entity = Person
    filename = "job.tab"

    @staticmethod
    def parse(person: dict, line: dict) -> dict:
        person["profit"] += yearly(line["SEINCAMT"])
        return person
