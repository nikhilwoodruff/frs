from frs.dataset import Table, Person, BenUnit, Household
from frs.utils import yearly, add


class Benunit(Table):
    enums = {}
    entity = BenUnit
    filename = "benunit.tab"

    @staticmethod
    def parse(benunit: dict, line: dict) -> dict:
        benunit["household_id"] = Household.id(line)
        benunit["benunit_id"] = BenUnit.id(line)
        benunit["benunit_weight"] = line["GROSS4"]
        return benunit
