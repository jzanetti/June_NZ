MODEL_PATH = "lib/JUNE_v1.2.0"

JUNE_MODEL = {
    "link": "https://github.com/jzanetti/JUNE.git",
    "branch": "sijin_dev",
    "model_name": "JUNE_v1.2.0",
}

USE_POLARS = False

SECTOR_CODES = {
    "A": "Agriculture, Forestry and Fishing",
    "B": "Mining",
    "C": "Manufacturing",
    "D": "Electricity, Gas, Water and Waste Services",
    "E": "Construction",
    "F": "Wholesale Trade",
    "G": "Retail Trade",
    "H": "Accommodation and Food Services",
    "I": "Transport, Postal and Warehousing",
    "J": "Information Media and Telecommunications",
    "K": "Financial and Insurance Services",
    "L": "Rental, Hiring and Real Estate Services",
    "M": "Professional, Scientific and Technical Services",
    "N": "Administrative and Support Services",
    "O": "Public Administration and Safety",
    "P": "Education and Training",
    "Q": "Health Care and Social Assistanc",
    "R": "Arts and Recreation Services",
    "S": "Other Services",
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
    8: "Manawatu-Whanganui",
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

FIXED_DATA = {
    "group": {
        "household": {
            "age_difference_couple": {
                "age_difference": [-5, 0, 5, 10],
                "frequency": [0.1, 0.7, 0.1, 0.1],
            },
            "age_difference_parent_child": {
                "age_difference": [25, 50],
                "0": [0.1, 0.9],
                "1": [0.1, 0.9],
                "2": [0.2, 0.8],
                "3": [0.3, 0.7],
                "4 or more": [0.3, 0.7],
            },
        },
        "hospital": {"icu_beds_ratio": 0.1},
    },
    "demography": {
        "comorbidities_female": {
            "comorbidity": ["disease1", "disease2", "no_condition"],
            5: [0, 0, 1.0],
            10: [0, 0, 1.0],
            20: [0, 0, 1.0],
            50: [0, 0.1, 0.9],
            75: [0, 0.2, 0.8],
            100: [0.9, 0.0, 0.1],
        },
        "comorbidities_male": {
            "comorbidity": ["disease1", "disease2", "no_condition"],
            5: [0, 0, 1.0],
            10: [0, 0, 1.0],
            20: [0, 0, 1.0],
            50: [0, 0.1, 0.9],
            75: [0, 0.2, 0.8],
            100: [0.9, 0.0, 0.1],
        },
    },
}


EXCLUDED_AREAS = [258000, 258100]

AREAS_CONSISTENCY_CHECK = {
    "geography_hierarchy_definition": {"super_area": "super_area", "area": "area"},
    "super_area_location": {"super_area": "super_area"},
    "area_location": {"area": "area"},
    "area_socialeconomic_index": {"area": "area"},
    "gender_profile_female_ratio": {"area": "output_area"},
    "ethnicity_profile": {"area": "output_area"},
    "age_profile": {"area": "output_area"},
    "sectors_employee_genders": {"area": "oareas"},
    "employees_by_super_area": {"super_area": "MSOA"},
    "sectors_by_super_area": {"super_area": "MSOA"},
    "hospital_locations": None,
    "schools": None,
    # "hospital_locations": {"super_area": "super_area", "area": "area"},
    "transport_mode": {"area": "geography"},
    "super_area_name": {"super_area": "super_area"},
    "household_number": {"area": "output_area"},
    "workplace_and_home": None,
    "household_communal": {"area": "output_area"},
    "household_student": {"area": "area"},
}


SCHOOL_AGE_TABLE = {
    "Secondary (Year 9-15)": "secondary (14-19)",
    "Composite": "primary_secondary (5-19)",
    "Full Primary": "primary (5-13)",
    "Secondary (Year 7-15)": "secondary (11-19)",
    "Contributing": "primary (5-11)",
    "Special School": "primary_secondary (8-15)",
    "Secondary (Year 7-10)": "secondary (11-14)",
    "Intermediate": "secondary (11-13)",
    "Secondary (Year 11-15)": "secondary (15-19)",
    "Restricted Composite (Year 7-10)": "secondary (11-14)",
    "Composite (Year 1-10)": "primary_secondary (5-14)",
    "Activity Centre": "secondary (14-17)",
}
