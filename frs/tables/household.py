from frs.dataset import Table, Person, BenUnit, Household
from frs.utils import yearly, add

class HHold(Table):
    enums = {}
    entity = Household
    filename = "househol.tab"

    @staticmethod
    def parse(household: dict, line: dict) -> dict:
        household["household_id"] = Household.id(line)
        household["household_weight"] = line["GROSS4"]
        household["country"] = COUNTRY[line["COUNTRY"]]
        household["num_rooms"] = line["ROOMS10"]
        household["rent"] = line["HHRENT"]
        household["is_shared"] = line["HHSTAT"] == 2
        household["housing_costs"] = line["GBHSCOST"] + line["NIHSCOST"]
        band = line["CTBAND"]
        household["council_tax"] = line["CTANNUAL"] or AVERAGE_COUNCIL_TAX[int(band - 1)]
        household["is_social"] = line["PTENTYP2"] in [1, 2]
        household["region"] = REGIONS_TO_NUM[GOVTREGNO[int(line["GVTREGNO"])]]
        return household


COUNTRY = {1: "ENGLAND", 2: "WALES", 3: "SCOTLAND", 4: "NI"}

AVERAGE_COUNCIL_TAX = [1114, 1300, 1486, 1671, 2043, 2414, 2786, 3343, 3900, 0]



GOVTREGNO = {
    1: "NORTH_EAST",
    2: "NORTH_WEST",
    4: "YORKSHIRE",
    5: "EAST_MIDLANDS",
    6: "WEST_MIDLANDS",
    7: "EAST_OF_ENGLAND",
    8: "LONDON",
    9: "SOUTH_EAST",
    10: "SOUTH_WEST",
    11: "WALES",
    12: "SCOTLAND",
    13: "NORTHERN_IRELAND",
}


REGIONS_TO_NUM = {
    region: i for region, i in zip(GOVTREGNO.values(), range(len(GOVTREGNO)))
}