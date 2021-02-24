from frs.dataset import Table, Person, BenUnit, Household
from frs.utils import yearly, add

class Maintenance(Table):
    enums = {}
    entity = Person
    filename = "maint.tab"

    @staticmethod
    def parse(person: dict, line: dict) -> dict:
        person["maintenance_payments"] = line["MRUAMT"] or line["MRAMT"]
        return person