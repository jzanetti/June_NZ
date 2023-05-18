MODEL_PATH = "lib/JUNE_v1.2.0"

JUNE_MODEL = {
    "link": "https://github.com/jzanetti/JUNE.git",
    "branch": "sijin_dev",
    "model_name": "JUNE_v1.2.0",
}

SECTOR_CODES = {
    "A": "Agriculture, forestry and fishing",
    "Q": "Human health and social work activities",
    "P": "Education",
}

REGION_CODES = {
    "North Island": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "South Island": [12, 13, 14, 15, 16, 17, 18],
    "Others": [99],
}
REGION_NAMES_CONVERSIONS = {
    1: "Northland",
    14: "Otago",
    3: "Waikato",
    99: "Area Outside",
    2: "Auckland",
    4: "Bay of Plenty",
    8: "Manawatu-Whanganui",  # Manawatu-Whanganui
    15: "Southland",
    6: "Hawke's Bay",
    5: "Gisborne",
    7: "Taranaki",
    9: "Wellington",
    17: "Nelson",
    18: "Marlborough",
    13: "Canterbury",
    16: "Tasman",
    12: "West Coast",
}
