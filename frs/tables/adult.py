from frs.table_utils import *


def parse_adult(line, person):
    person["is_adult"] = True
    person["is_child"] = False

    # absence
    person["is_absent"] = safe(line["ABSWK"]) == 1
    person["reason_for_absence"] = ABSENCE_REASON[safe(line["ABSWHY"])]
    person["absence_pay"] = ABSENCE_PAY[safe(line["ABSPAY"])]

    # accounts
    person["access_fund"] = yearly(line["ACCSSAMT"])
    person["has_direct_payment_account"] = safe(line["ACTACCI"]) == 1
    person["EMA"] = yearly(line["ADEMAAMT"])

    person["age"] = safe(line["AGE80"])

    # allowances
    person["alimony_payments_received"] = yearly(
        safe(line["ALUAMT"], line["ALIAMT"])
    )
    person["allowance_from_friend"] = yearly(line["ALLPAY1"])
    person["allowance_from_org"] = yearly(line["ALLPAY2"])
    person["allowance_from_LA_fostered"] = yearly(line["ALLPAY3"])
    person["allowance_from_LA_adoption"] = yearly(line["ALLPAY4"])

    # accounts
    person["has_funds"] = safe(line["ANYMON"]) != 2
    person["in_education"] = safe(line["ANYED"]) == 1
    person["num_employee_pensions"] = safe(line["ANYPNNM1"])
    person["num_individual_pensions"] = safe(line["ANYPNNM2"])
    person["num_survivor_pensions"] = safe(line["ANYPNNM3"])
    person["num_annuities"] = safe(line["ANYPNNM4"])
    person["num_trusts"] = safe(line["ANYPNNM5"])

    # partner
    person["payments_to_absent_partner"] = yearly(line["APAMT"])
    person["received_babybox"] = safe(line["BABYBOX"]) == 1

    person["person_id"] = person_id(line)
    person["benunit_id"] = benunit_id(line)
    person["household_id"] = household_id(line)

    person["bursary_fund"] = yearly(line["BFDAMT"])

    person["is_informal_carer"] = safe(line["CAREFL"]) == 1

    person["est_value"] = ACCOUNT_ESTIMATES_MEAN[safe(line["CBAAMT2"])]

    person["moved_house"] = safe(line["CHANGE"]) == 1

    # head status
    person["is_household_head"] = safe(line["PERSON"]) == 1
    person["is_benunit_head"] = safe(line["UPERSON"]) == 1

    person["is_boarder"] = safe(line["CONVBL"]) == 1
    person["is_lodger"] = safe(line["CONVBL"]) == 2

    # disability
    person["dis_equality_act_core"] = safe(line["DISCORA1"]) == 1
    person["dis_equality_act_core"] = safe(line["DISACTA1"]) == 1
    person["vision_difficulty"] = safe(line["DISD01"]) == 1
    person["hearing_difficulty"] = safe(line["DISD02"]) == 1
    person["mobility_difficulty"] = safe(line["DISD03"]) == 1
    person["dexterity_difficulty"] = safe(line["DISD04"]) == 1
    person["learning_difficulty"] = safe(line["DISD05"]) == 1
    person["memory_difficulty"] = safe(line["DISD06"]) == 1
    person["mental_health_difficulty"] = safe(line["DISD07"]) == 1
    person["stamina_difficulty"] = safe(line["DISD08"]) == 1
    person["social_difficulty"] = safe(line["DISD09"]) == 1
    person["other_difficulty"] = safe(line["DISD10"]) == 1

    # education
    person["highest_qualification"] = QUALIFICATIONS[safe(line["DVHIQUAL"])]
    person["education_type"] = EDU_TYPE[safe(line["EDTYP"])]

    # employment status
    person["is_temp"] = safe(line["EMPCONTR"]) == 2
    person["employment_status"] = EMPLOYMENT_STATUS[safe(line["EMPSTATB"])]

    # ethnicity
    person["ethnicity"] = ETHNIC_GROUP_BASE[safe(line["ETHGR3"])]
    person["ethnicity_detailed"] = ETHNIC_GROUP_FINE[safe(line["ETNGRP"])]

    # historical employment
    person["ever_worked"] = safe(line["EVERWRK"]) < 2
    person["years_in_FT_work"] = safe(line["FTWK"])

    person["adult_weight"] = safe(line["GROSS4"])

    person["long_standing_illness"] = safe(line["HEALTH1"]) == 1

    # care
    person["care_hours_received"] = safe(line["HOURCARE"])
    person["care_hours_given"] = HOURS_CODES_MEAN_VALUES[safe(line["HOURTOT"])]

    # income
    person["earnings"] = yearly(line["INEARS"])
    person["pension_income"] = yearly(line["INPENINC"])
    person["free_TV_license_value"] = yearly(line["INTVLIC"])
    person["FRS_net_income"] = yearly(line["NINDINC"])

    person["registered_disabled"] = safe(line["LAREG"]) == 1
    person["marital_status"] = MARITAL_STATUS[safe(line["MARITAL"])]
    person["is_married"] = person["marital_status"] == "married"

    person["in_private_sector"] = safe(line["MJOBSECT"]) == 1
    person["in_public_sector"] = safe(line["MJOBSECT"]) == 2

    person["child_maintenance_received"] = yearly(line["MNTAMT1"])
    person["payments_to_absent_partner"] = yearly(line["OTAPAMT"])
    person["parental_contributions"] = yearly(line["PAREAMT"])

    person["rental_income"] = yearly(line["ROYYR1"])

    person["is_male"] = safe(line["SEX"]) == 1
    person["is_female"] = safe(line["SEX"]) == 2

    person["student_loan_repayments"] = yearly(line["SLREPAMT"])

    person["standard_occ_class"] = STANDARD_OCC_CLASS[safe(line["SOC2010"])]

    person["is_blind"] = safe(line["SPCREG1"]) == 1
    person["is_partial_sighted"] = safe(line["SPCREG2"]) == 1
    person["is_deaf"] = safe(line["SPCREG3"]) == 1

    person["edu_grants"] = safe(line["TOTGRANT"])
    person["hours"] = yearly(line["TOTHOURS"])

    person["misc_income"] = yearly(line["INRINC"])

    person["is_employee"] = safe(line["EMPSTAT"]) == 1
    person["is_self_employed"] = safe(line["EMPSTATB"]) == 2

    person["total_benefits"] = yearly(
        add_up(line, "INDISBEN", "INOTHBEN", "INTXCRED", "INDUC", "INRPINC")
    )
    return person


ACCOUNT_ESTIMATES = {
    NO_DATA: (0, 0),
    14: (-1, -1),
    1: (0, 0),
    2: (1, 50),
    3: (51, 100),
    4: (101, 250),
    5: (251, 500),
    6: (501, 1000),
    7: (1001, 2000),
    8: (2001, 3000),
    9: (3001, 5000),
    10: (5001, 10000),
    11: (10001, 20000),
    12: (20001, 30000),
    13: (30001, 30001),
}

ACCOUNT_ESTIMATES_MEAN = {
    x: (y[0] + y[1]) / 2 for x, y in ACCOUNT_ESTIMATES.items()
}


ABSENCE_REASON = {
    NO_DATA: "unknown",
    1: "pattern_of_shifts",
    2: "illness_or_accident",
    3: "holiday",
    4: "strike",
    5: "laid_off",
    6: "maternity_leave",
    7: "paternity_leave",
    8: "compassionate_leave",
    9: "parental_leave",
    10: "other",
}

ABSENCE_PAY = {
    NO_DATA: "unknown",
    1: "full_pay",
    2: "over_half_pay",
    3: "under_half_pay",
    4: "no_pay",
}

QUALIFICATIONS = {
    NO_DATA: "unknown",
    1: "doctorate",
    2: "postgraduate_degree",
    3: "degree",
    4: "teaching_qual",
    5: "foreign_degree_level",
    6: "work_degree_level",
    7: "other_prof_degree_level",
    8: "HE_below_degree",
    9: "nursing",
    10: "diploma_in_HE",
    11: "HNC",
    12: "BTEC_higher",
    13: "SCOTVEC",
    14: "NVQ_level_4",
    15: "NVQ_level_5",
    16: "OCT_level_4",
    17: "A_level",
    18: "welsh_bacc_advanced",
    19: "scot_bacc",
    20: "IB",
    21: "AS_level",
    22: "CSYS",
    23: "access_HE",
    24: "advanced_higher_qual",
    25: "skills_for_work_higher",
    26: "ONC",
    27: "BTEC_Nat",
    28: "SCOTVEC_full",
    29: "new_diploma_advanced",
    30: "new_diploma_progression",
    31: "NVQ",
    32: "GNVQ",
    33: "OCR_advanced",
    34: "city_and_guilds",
    35: "welsh_bacc_intermediate",
    36: "5_O_levels",
    37: "5_SG_scot",
    38: "GCSE",
    39: "5_CSEs",
    40: "scot_nat_level_5",
    41: "skills_for_work_level_5",
    42: "BTEC_general_diploma",
    43: "SCOTVEC_general_diploma",
    44: "new_diploma_higher",
    45: "NVQ_level_2",
    46: "GNVQ_full_intermediate",
    47: "OCR_level_2",
    48: "city_and_guilds_part_2",
    49: "other_HS_leaver_qual",
    50: "BTEC",
    51: "BTEC_general_cert",
    52: "SCOTVEC",
    53: "SCOTVEC_general_cert",
    54: "SCOTVEC_nat_modules",
    55: "new_diploma",
    56: "new_diploma_foundation",
    57: "welsh_bacc",
    58: "welsh_bacc_foundation",
    59: "NVQ",
    60: "NVQ_level_1",
    61: "GNVQ",
    62: "GNVQ_part_one",
    63: "GNVQ_full_foundation",
    64: "GNVQ_part_one_foundation",
    65: "5_O_levels",
    66: "under_5_O_levels",
    67: "5_SGs",
    68: "under_5_SGs",
    69: "5_GCSEs",
    70: "under_5_GCSEs",
    71: "scot_nat_level_1",
    72: "scot_nat",
    73: "skills_for_work_nat_level_3",
    74: "skills_for_work",
    75: "5_CSEs",
    76: "under_5_CSEs",
    77: "OCR",
    78: "OCR",
    79: "city_and_guilds",
    80: "city_and_guilds_foundation",
    81: "YTP",
    82: "core_skills",
    83: "basic_skills",
    84: "entry_level_qual",
    85: "entry_level_award",
    86: "other_qual",
}

EDU_TYPE = {
    NO_DATA: "unknown",
    1: "school_full_time",
    2: "school_part_time",
    3: "sandwich_course",
    4: "uni_or_college",
    5: "training",
    6: "uni_or_college_PT",
    7: "open_college",
    8: "open_university",
    9: "other_correspondence_course",
    10: "other_course",
}

EMPLOYMENT_STATUS = {
    NO_DATA: "unknown",
    1: "self_employed",
    2: "FT_employee",
    3: "PT_employee",
    4: "FT_employee_sick",
    5: "PT_employee_sick",
    6: "industrial_action",
    7: "unemployed",
    8: "work_govt_training",
    9: "retired",
    10: "unocupied_under_SP_age",
    11: "temp_sick",
    12: "long_term_sick",
    13: "student",
    14: "unpaid_family_worker",
}

ETHNIC_GROUP_BASE = {
    NO_DATA: "unknown",
    1: "white",
    2: "mixed",
    3: "asian",
    4: "black",
    5: "other",
}

ETHNIC_GROUP_FINE = {
    NO_DATA: "unknown",
    1: "white_non_irish",
    2: "white_irish",
    3: "white_gypsy",
    4: "white_other",
    5: "mixed_white_black_caribbean",
    6: "mixed_white_black_african",
    7: "mixed_white_asian",
    8: "mixed_other",
    9: "asian_indian",
    10: "asian_pakistani",
    11: "asian_bangladeshi",
    12: "chinese",
    13: "asian_other",
    14: "black_african",
    15: "black_caribbean",
    16: "black_other",
    17: "arab",
    18: "other",
}

MARITAL_STATUS = {
    NO_DATA: "unknown",
    1: "married",
    2: "cohabiting",
    3: "single",
    4: "widowed",
    5: "separated",
    6: "divorced",
}

STANDARD_OCC_CLASS = {
    NO_DATA: "unknown",
    1000: "managerial",
    2000: "professional",
    3000: "techical",
    4000: "admin",
    5000: "skilled_trades",
    6000: "care",
    7000: "sales",
    8000: "manufacturing",
    9000: "elementary",
}

ADULT_FIELDNAMES = [
    "is_adult",
    "is_child",
    "is_absent",
    "reason_for_absence",
    "absence_pay",
    "access_fund",
    "has_direct_payment_account",
    "EMA",
    "age",
    "alimony_payments_received",
    "allowance_from_friend",
    "allowance_from_org",
    "allowance_from_LA_fostered",
    "allowance_from_LA_adoption",
    "has_funds",
    "in_education",
    "num_employee_pensions",
    "num_individual_pensions",
    "num_survivor_pensions",
    "num_annuities",
    "num_trusts",
    "received_babybox",
    "person_id",
    "benunit_id",
    "household_id",
    "bursary_fund",
    "is_informal_carer",
    "est_value",
    "moved_house",
    "is_household_head",
    "is_benunit_head",
    "is_boarder",
    "is_lodger",
    "dis_equality_act_core",
    "dis_equality_act_wider",
    "vision_difficulty",
    "hearing_difficulty",
    "mobility_difficulty",
    "dexterity_difficulty",
    "learning_difficulty",
    "memory_difficulty",
    "mental_health_difficulty",
    "stamina_difficulty",
    "social_difficulty",
    "other_difficulty",
    "highest_qualification",
    "education_type",
    "is_temp",
    "employment_status",
    "ethnicity",
    "ethnicity_detailed",
    "ever_worked",
    "years_in_FT_work",
    "adult_weight",
    "long_standing_illness",
    "care_hours_received",
    "care_hours_given",
    "free_TV_license_value",
    "FRS_net_income",
    "registered_disabled",
    "marital_status",
    "in_private_sector",
    "in_public_sector",
    "child_maintenance_received",
    "payments_to_absent_partner",
    "parental_contributions",
    "rental_income",
    "is_male",
    "is_female",
    "student_loan_repayments",
    "standard_occ_class",
    "is_blind",
    "is_partial_sighted",
    "is_deaf",
    "hours",
    "misc_income",
    "is_married",
    "total_benefits",
    "is_employee",
    "is_self_employed",
]

ADULT_ENUMS = dict(
    reason_for_absence=ABSENCE_REASON,
    absence_pay=ABSENCE_PAY,
    highest_qualification=QUALIFICATIONS,
    education_type=EDU_TYPE,
    employment_status=EMPLOYMENT_STATUS,
    ethnicity=ETHNIC_GROUP_BASE,
    ethicity_detailed=ETHNIC_GROUP_FINE,
    marital_status=MARITAL_STATUS,
    standard_occ_class=STANDARD_OCC_CLASS,
)
