from frs.dataset import Table, Person, BenUnit, Household
from frs.utils import yearly, add

class Childcare(Table):
    enums = {}
    entity = Person
    filename = "chldcare.tab"

    @staticmethod
    def parse(person: dict, line: dict) -> dict:
        person["childcare"] += line["CHAMT"] * (line["REGISTRD"] == 1)
        return person