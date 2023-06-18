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

"""
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
        "comorbidities_intensity": {"disease1": 0.8, "disease2": 1.2, "no_condition": 1.0},
    },
}
"""


FIXED_DATA = {
    "group": {
        "commute": {
            "transport_def": [
                {"description": "Work mainly at or from home", "is_public": False},
                {"description": "Underground, metro, light rail, tram", "is_public": True},
                {"description": "Train", "is_public": True},
                {"description": "Bus, minibus or coach", "is_public": True},
                {"description": "Taxi", "is_public": False},
                {"description": "Motorcycle, scooter or moped", "is_public": False},
                {"description": "Driving a car or van", "is_public": False},
                {"description": "Passenger in a car or van", "is_public": False},
                {"description": "Bicycle", "is_public": False},
                {"description": "On foot", "is_public": False},
                {"description": "Other method of travel to work", "is_public": False},
            ],
            "passage_seats_ratio": 1.3,
            "number_of_inter_city_stations": {
                "number_of_inter_city_stations": {
                    "Northland": 1,
                    "Otago": 1,
                    "Waikato": 1,
                    "Auckland": 3,
                    "Bay of Plenty": 1,
                    "Manawatu-Whanganui": 1,
                    "Southland": 1,
                    "Hawke's Bay": 1,
                    "Gisborne": 1,
                    "Taranaki": 1,
                    "Wellington": 2,
                    "Nelson": 1,
                    "Marlborough": 1,
                    "Canterbury": 2,
                    "Tasman": 1,
                    "West Coast": 1,
                }
            },
        },
        "company": {
            "employees": {"employment_rate": 0.7},
            "company_closure": {
                "company_closure": {
                    "sectors": {
                        "A": {"key_worker": 1.0, "furlough": 0.0, "random": 0.0},
                        "P": {"key_worker": 0.0, "furlough": 0.0833, "random": 0.9167},
                        "Q": {"key_worker": 0.0, "furlough": 0.0769, "random": 0.9231},
                        "B": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "C": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "D": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "E": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "F": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "G": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "H": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "I": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "J": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "K": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "L": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "M": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "N": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "O": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "R": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                        "S": {"key_worker": 0.0, "furlough": 0.0, "random": 1.0},
                    }
                }
            },
            "subsector_cfg": {
                "age_range": [18, 64],
                "sub_sector_ratio": {"P": {"m": 0.4, "f": 0.6}, "Q": {"m": 0.5, "f": 0.5}},
                "sub_sector_distr": {
                    "P": {
                        "label": ["teacher_secondary", "teacher_primary"],
                        "m": [0.72526887, 0.27473113],
                        "f": [0.72526887, 0.27473113],
                    },
                    "Q": {
                        "label": ["doctor", "nurse"],
                        "m": [0.65350126, 0.34649874],
                        "f": [0.16103136, 0.83896864],
                    },
                },
            },
        },
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
    "disease": {
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
        "comorbidities_intensity": {"disease1": 0.8, "disease2": 1.2, "no_condition": 1.0},
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

# https://wiki.openstreetmap.org/wiki/Key:amenity
# https://wiki.openstreetmap.org/wiki/Key:leisure
# https://wiki.openstreetmap.org/wiki/Key:building
OVERPY_QUERY_KEY = {
    "cinema": {"amenity": ["cinema"]},
    "pub": {"amenity": ["pub"]},
    "gym": {"leisure": ["fitness_centre"]},
    "grocery": {"shop": ["convenience", "supermarket"]},
}
