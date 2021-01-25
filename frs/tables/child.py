from frs.table_utils import *
from frs.tables.adult import MARITAL_STATUS

def parse_child(line, person):
    person["is_adult"] = False
    person["is_child"] = True

    # disability
    person["dis_equality_act_core"] = safe(line["DISCORC1"]) == 1
    person["vision_difficulty"] = safe(line["CDISD01"]) == 1
    person["hearing_difficulty"] = safe(line["CDISD02"]) == 1
    person["mobility_difficulty"] = safe(line["CDISD03"]) == 1
    person["dexterity_difficulty"] = safe(line["CDISD04"]) == 1
    person["learning_difficulty"] = safe(line["CDISD05"]) == 1
    person["memory_difficulty"] = safe(line["CDISD06"]) == 1
    person["mental_health_difficulty"] = safe(line["CDISD07"]) == 1
    person["stamina_difficulty"] = safe(line["CDISD08"]) == 1
    person["social_difficulty"] = safe(line["CDISD09"]) == 1
    person["other_difficulty"] = safe(line["CDISD10"]) == 1

    person["bursary_fund"] = yearly(line["CHBFDAMT"])

    person["earnings"] = yearly(line["CHEARNS1"]) + yearly(line["CHEARNS2"])
    person["trust_income"] = yearly(line["CHEARNS3"])
    
    person["is_boarder"] = safe(line["CONVBL"]) == 1
    person["is_lodger"] = safe(line["CONVBL"]) == 2

    person["free_school_breakfast"] = yearly(line["FSBVAL"])
    person["free_school_fruit_veg"] = yearly(line["FSFVVAL"])
    person["free_school_milk"] = yearly(line["FSMVAL"])
    person["free_school_meals"] = yearly(line["FSMVAL"])

    person["age"] = safe(line["AGE"])

    person["care_hours_given"] = safe(line["HOURTOT"])
    person["registered_disabled"] = safe(line["LAREG"]) == 1
    person["is_blind"] = safe(line["SPCREG1"]) == 1
    person["is_partial_sighted"] = safe(line["SPCREG2"]) == 1
    person["is_deaf"] = safe(line["SPCREG3"]) == 1

    person["EMA"] = yearly("CHEMAAMT")

    if safe(line["MS"]) in MARITAL_STATUS:
        person["marital_status"] = MARITAL_STATUS[safe(line["MS"])]
    
    person["is_male"] = safe(line["SEX"]) == 1
    person["is_female"] = safe(line["SEX"]) == 2

    person["tax_free_childcare_paid_in"] = yearly(safe(line["TFCAMT"], line["UTFCAMT"]))
    person["tax_free_childcare_paid_out"] = yearly(safe(line["TFCOAMT"], line["UTFCOAMT"]))
    person["est_value"] = safe(line["TOTSAVE"])
    person["edu_grants"] = yearly(line["TOTGNTCH"])
    person["school_type"] = SCHOOL_TYPE[safe(line["TYPEED2"])]
    
    person["person_id"] = person_id(line)
    person["benunit_id"] = benunit_id(line)
    person["household_id"] = household_id(line)

    person["is_benunit_head"] = False
    person["is_household_head"] = False

    person["misc_income"] = yearly(line["CHRINC"])
    return person

CHILD_FIELDNAMES = [
    "free_school_breakfast",
    "free_school_fruit_veg",
    "free_school_milk",
    "free_school_meals",
    "tax_free_childcare_paid_in",
    "tax_free_childcare_paid_out",
    "est_value",
    "edu_grants",
    "school_type",
    "trust_income"
]

SCHOOL_TYPE = {
    NO_DATA: "unknown",
    1: "pre_school",
    2: "primary_school",
    3: "special_school",
    4: "middle_primary_school",
    5: "middle_secondary_school",
    6: "secondary_school",
    7: "non_adv_FE",
    8: "private",
    9: "HE"
}

CHILD_ENUMS = dict(
    school_type=SCHOOL_TYPE
)