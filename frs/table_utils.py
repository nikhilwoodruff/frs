WEEK = 1
MONTH = 5
YEAR = 52

PERIOD_CODES = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 4.35,
    7: 8.7,
    8: 6.52,
    9: 5.8,
    10: 5.22,
    13: 13,
    17: 17.4,
    26: 26,
    52: 52,
    90: 0.5,
    95: 52,
    97: 1000,
}

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


def adjust_period(value, period_code, target_period_code):
    """Adjusts a value from one period to another

    Args:
        value (float): The value
        period_code (int, optional): The original period code.
        target_period_code (int, optional): The target period code.

    Returns:
        float: The adjusted value
    """
    if safe(value) == 0:
        return 0
    if period_code == 0:
        period_code = 1
    if period_code not in PERIOD_CODES or target_period_code not in PERIOD_CODES:
        print("Warning: missing valid period code, writing as 0.")
        return 0
    relative_size = (
        PERIOD_CODES[target_period_code] / PERIOD_CODES[period_code]
    )
    return safe(value) * relative_size

def yearly(value, from_period=WEEK):
    return adjust_period(value, period_code=safe(from_period), target_period_code=YEAR)

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

NO_DATA = 0

HOURS_CODES_BOUNDS = {
    NO_DATA: (0, 0),
    1: (0, 4),
    2: (5, 9),
    3: (10, 19),
    4: (20, 34),
    5: (35, 49),
    6: (50, 99),
    7: (100, 100),
    8: (0, 20),
    9: (20, 34),
    10: (35, 35)
}

HOURS_CODES_MEAN_VALUES = {x: (y[0] + y[1]) / 2 for x, y in HOURS_CODES_BOUNDS.items()}

COUNTRY_CODES = {
    NO_DATA: "none",
    4: "afghanistan",
    8: "albania",
    10: "antarctica",
    12: "algeria",
    16: "american_samoa",
    20: "andorra",
    24: "angola",
    28: "antigua_and_barbuda",
    31: "azerbaijan",
    32: "argentina",
    36: "australia",
    40: "austria",
    44: "bahamas_the",
    48: "bahrain",
    50: "bangladesh",
    51: "armenia",
    52: "barbados",
    56: "belgium",
    60: "bermuda",
    64: "bhutan",
    68: "bolivia",
    70: "bosnia_and_herzegovina",
    72: "botswana",
    74: "bouvet_island",
    76: "brazil",
    84: "belize",
    86: "british_indian_ocean_territory",
    90: "solomon_islands",
    92: "british_virgin_islands",
    96: "brunei_brunei_darussalam",
    100: "bulgaria",
    104: "myanmar_burma",
    108: "burundi",
    112: "belarus",
    116: "cambodia",
    120: "cameroon",
    124: "canada",
    132: "cape_verde",
    136: "cayman_islands",
    140: "central_african_republic",
    144: "sri_lanka",
    148: "chad",
    152: "chile",
    156: "china_peoples_republic_of",
    158: "china_taiwan",
    162: "christmas_island",
    166: "cocos_keeling_islands",
    170: "colombia",
    174: "comoros",
    175: "mayotte_mahore",
    178: "congo_congo_brazzaville",
    180: "congo_democratic_republic_of_congo_kinsala",
    184: "cook_islands",
    188: "costa_rica",
    191: "croatia",
    192: "cuba",
    203: "czech_republic",
    204: "benin",
    208: "denmark",
    212: "dominica",
    214: "dominican_republic",
    218: "ecuador",
    222: "el_salvador",
    226: "equatorial_guinea",
    231: "ethiopia",
    232: "eritrea",
    233: "estonia",
    234: "faroe_islands",
    238: "falkland_islands",
    239: "south_georgia_and_the_south_sandwich_islands",
    242: "fiji",
    246: "finland",
    248: "aland_islands",
    250: "france",
    254: "french_guiana",
    258: "french_polynesia",
    260: "french_southern_territories",
    262: "djibouti",
    266: "gabon",
    268: "georgia",
    270: "gambia_the",
    275: "occupied_palestinian_territories",
    276: "germany",
    288: "ghana",
    292: "gibraltar",
    296: "kiribati",
    300: "greece_hellenic_republic",
    304: "greenland",
    308: "grenada",
    312: "guadeloupe",
    316: "guam",
    320: "guatemala",
    324: "guinea",
    328: "guyana",
    332: "haiti",
    334: "heard_island_and_mcdonald_islands",
    336: "vatican_city_holy_see",
    340: "honduras",
    344: "hong_kong_special_admin_region_of_china",
    348: "hungary",
    352: "iceland",
    356: "india_bharat",
    360: "indonesia",
    364: "iran",
    368: "iraq",
    372: "ireland",
    376: "israel",
    380: "italy",
    384: "ivory_coast_cote_divoire",
    388: "jamaica",
    392: "japan",
    398: "kazakhstan",
    400: "jordan",
    404: "kenya",
    408: "korea_north",
    410: "korea_south",
    414: "kuwait",
    417: "kyrgystan_kirgizia",
    418: "laos",
    422: "lebanon",
    426: "lesotho",
    428: "latvia",
    430: "liberia",
    434: "libya_libyan_arab_jamahiriya",
    438: "liechtenstein",
    440: "lithuania",
    442: "luxembourg",
    446: "macao_special_admin_region_of_china",
    450: "madagascar_malagasy_republic",
    454: "malawi",
    458: "malaysia",
    462: "maldives",
    466: "mali",
    470: "malta",
    474: "martinique",
    478: "mauritania",
    480: "mauritius",
    484: "mexico_united_mexican_states",
    492: "monaco",
    496: "mongolia",
    498: "moldova",
    499: "montenegro",
    500: "montserrat",
    504: "morocco",
    508: "mozambique",
    512: "oman",
    516: "namibia",
    520: "nauru",
    524: "nepal",
    528: "netherlands",
    530: "dutch_west_indies_netherlands_antilles",
    531: "curacao",
    533: "aruba",
    534: "st_maarten_dutch_part",
    535: "bonaire_st_eustatius_&_saba",
    540: "new_caledonia",
    548: "vanuatu",
    554: "new_zealand",
    558: "nicaragua",
    562: "niger",
    566: "nigeria",
    570: "niue",
    574: "norfolk_island",
    578: "norway",
    580: "northern_mariana_islands",
    581: "united_states_minor_outlying_islands",
    583: "micronesia",
    584: "marshall_islands",
    585: "palau",
    586: "pakistan",
    591: "panama",
    598: "papua_new_guinea",
    600: "paraguay",
    604: "peru",
    608: "philippines",
    612: "pitcairn_henderson_ducie_ans_oeno_islands",
    616: "poland",
    620: "portugal",
    624: "guinea_bissau",
    626: "east_timor_timor_leste",
    630: "puerto_rico_porto_rico",
    634: "qatar",
    638: "reunion",
    642: "romania",
    643: "russia_russian_federation",
    646: "rwanda",
    652: "st_barthelemy",
    654: "st_helena",
    659: "st_kitts_and_nevis",
    660: "anguilla",
    662: "st_lucia",
    663: "st_martin_french_part",
    666: "st_pierre_and_miquelon",
    670: "st_vincent_and_the_grenadines",
    674: "san_marino",
    678: "sao_tome_and_principe",
    682: "saudi_arabia",
    686: "senegal",
    688: "serbia",
    690: "seychelles",
    694: "sierra_leone",
    702: "singapore",
    703: "slovakia",
    704: "vietnam",
    705: "slovenia",
    706: "somalia",
    710: "south_africa",
    716: "zimbabwe",
    728: "south_sudan",
    729: "sudan",
    732: "western_sahara",
    736: "sudan",
    740: "surinam_sranang",
    744: "svalbard_and_jan_mayen",
    748: "swaziland",
    752: "sweden",
    756: "switzerland_swiss_helvetic_confederation",
    760: "syria_syrian_arab_republic",
    762: "tajikistan",
    764: "thailand",
    768: "togo",
    772: "tokelau",
    776: "tonga",
    780: "trinidad_and_tobago",
    784: "united_arab_emirates",
    788: "tunisia_tunisian_republic",
    792: "turkey",
    795: "turkmenistan_turkmania",
    796: "turks_and_caicos_islands",
    798: "tuvalu",
    800: "uganda",
    804: "ukraine",
    807: "macedonia",
    818: "egypt",
    831: "guernsey",
    832: "jersey",
    833: "isle_of_man",
    834: "tanzania",
    840: "united_states_of_america_usa",
    850: "united_states_virgin_islands",
    854: "burkina_faso",
    858: "uruguay",
    860: "uzbekistan",
    862: "venezuela",
    876: "wallis_and_futuna",
    882: "samoa",
    887: "yemen",
    891: "vojvodina",
    894: "zambia",
    901: "cyprus_and_sovereign_base_areas_overseas_territory",
    902: "cyprus_non_european_union_northern_cyprus",
    903: "cyprus_not_otherwise_specified",
    911: "spain_exc_canary_islands",
    912: "canary_islands",
    913: "spain_not_specified_if_mainland_or_canaries",
    921: "england",
    922: "northern_ireland",
    923: "scotland",
    924: "wales",
    925: "great_britain_not_otherwise_specified",
    926: "united_kingdom_not_otherwise_specified",
    931: "channel_islands_not_otherwise_specified",
    951: "kosovo",
    971: "czechoslovakia_not_otherwise_specified",
    972: "soviet_union_ussr_not_otherwise_specified",
    973: "yugoslavia_not_otherwise_specified",
    974: "serbia_and_montenegro_not_otherwise_specified",
    981: "europe_not_otherwise_specified",
    982: "africa_not_otherwise_specified",
    983: "middle_east_not_otherwise_specified",
    984: "asia_exc_middle_east_not_otherwise_specified",
    985: "north_america_not_otherwise_specified",
    986: "central_america_not_otherwise_specified",
    987: "south_america_not_otherwise_specified",
    988: "caribbean_and_west_indies_not_else_where_specified",
    989: "antarctica_and_oceania_not_otherwise_specifd",
    990: "netherlands_antilles_not_otherwise_specified",
    991: "at_sea",
    992: "in_the_air"
}