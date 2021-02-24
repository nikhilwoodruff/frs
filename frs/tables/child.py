from frs.dataset import Table, Person, BenUnit, Household
from frs.utils import yearly, add


class Child(Table):
    enums = {}
    entity = Person
    filename = "child.tab"

    @staticmethod
    def parse(person: dict, line: dict) -> dict:
        person["person_id"] = Person.id(line)
        person["is_adult"] = False
        person["is_child"] = True
        person["benunit_id"] = BenUnit.id(line)
        person["household_id"] = Household.id(line)
        person["role"] = "child"
        person["age"] = line["AGE"]
        person["misc_income"] = yearly(line["CHRINC"])
        person["earnings"] = yearly(line["CHEARNS"])
        person["FRS_net_income"] = line["CHINCDV"] - person["misc_income"]
        person["registered_disabled"] = line["LAREG"] == 1
        person["dis_equality_act_core"] = line["DISCORC1"] == 1
        person["dis_equality_act_wider"] = line["DISACTC1"] == 1
        person["is_benunit_head"] = False
        person["is_household_head"] = False
        return person
