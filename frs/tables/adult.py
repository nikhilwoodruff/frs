from frs.dataset import Table, Person, BenUnit, Household
from frs.utils import yearly, add


class Adult(Table):
    enums = {}
    entity = Person
    filename = "adult.tab"

    @staticmethod
    def parse(person: dict, line: dict) -> dict:
        person["person_id"] = Person.id(line)
        person["benunit_id"] = BenUnit.id(line)
        person["household_id"] = Household.id(line)
        person["is_adult"] = True
        person["is_child"] = False
        person["adult_weight"] = line["GROSS4"]
        person["role"] = "adult"
        person["earnings"] = yearly(line["INEARNS"])
        person["pension_income"] = yearly(line["INPENINC"])
        person["age"] = line["AGE80"]
        person["care_hours"] = CARE_HOURS_CODES[line["HOURTOT"]]
        person["hours"] = line["TOTHOURS"]
        person["savings_interest"] = yearly(line["ININV"])
        person["misc_income"] = yearly(line["INRINC"])
        person["total_benefits"] = add(
            line, "INDISBEN", "INOTHBEN", "INTXCRED", "INDUC"
        )
        person["is_household_head"] = int(line["PERSON"]) == 1
        person["is_benunit_head"] = int(line["UPERSON"]) == 1
        person["FRS_net_income"] = (
            yearly(line["NINDINC"]) - person["misc_income"]
        )
        person["student_loan_repayment"] = line["SLREPAMT"]
        person["registered_disabled"] = line["LAREG"] == 1
        person["dis_equality_act_core"] = line["DISCORA1"] == 1
        person["dis_equality_act_wider"] = line["DISACTA1"] == 1
        return person


CARE_HOURS_CODES = {
    0: 0,
    1: 2,
    2: 7,
    3: 14,
    4: 27,
    5: 44,
    6: 70,
    7: 100,
    8: 10,
    9: 30,
    10: 35,
}
