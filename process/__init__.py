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
                # {"description": "Work mainly at or from home", "is_public": False},
                {"description": "Drive_a_private_car_truck_or_van", "is_public": False},
                {"description": "Drive_a_company_car_truck_or_van", "is_public": True},
                {"description": "Passenger_in_a_car_truck_van_or_company_bus", "is_public": True},
                {"description": "Public_bus", "is_public": True},
                {"description": "Train", "is_public": True},
                {"description": "Bicycle", "is_public": False},
                {"description": "Ferry", "is_public": True},
                {"description": "Other", "is_public": False},
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
            "household_def": {
                "kid_max_age": 17,
                "student_min_age": 18,
                "student_max_age": 25,
                "old_min_age": 65,
                "old_max_age": 99,
                "adult_min_age": 18,
                "adult_max_age": 64,
                "young_adult_min_age": 18,
                "young_adult_max_age": 35,
                "max_age_to_be_parent": 64,
                "max_household_size": 8,
                "allowed_household_compositions": [
                    "1 0 >=0 1 0",
                    ">=2 0 >=0 1 0",
                    "1 0 >=0 2 0",
                    ">=2 0 >=0 2 0",
                    "1 0 >=0 >=1 >=0",
                    ">=2 0 >=0 >=1 >=0",
                    "0 0 0 0 >=2",
                    "0 >=1 0 0 0",
                    "0 0 0 0 1",
                    "0 0 0 0 2",
                    "0 0 0 1 0",
                    "0 0 0 2 0",
                    "0 0 >=1 1 0",
                    "0 0 >=1 2 0",
                    "0 0 >=0 >=0 >=0",
                    ">=0 >=0 >=0 >=0 >=0",
                ],
                "ignore_orphans": False,
            },
        },
        "hospital": {
            "icu_beds_ratio": 0.1,
            "hospital_cfg": {
                "medic_min_age": 25,
                "patients_per_medic": 10,
                "healthcare_sector_label": "Q",
            },
            "neighbour_hospitals": {"neighbour_hospitals": 3},
        },
        "leisure": {
            "pub": {
                "times_per_week": {
                    "weekday": {
                        "male": {
                            "0-9": 0.032,
                            "9-15": 0.106,
                            "15-19": 0.126,
                            "19-31": 0.738,
                            "31-51": 0.421,
                            "51-66": 0.533,
                            "66-86": 0.15,
                            "86-100": 0.033,
                        },
                        "female": {
                            "0-9": 0.135,
                            "9-15": 0.147,
                            "15-19": 0.358,
                            "19-31": 0.544,
                            "31-51": 0.4,
                            "51-66": 0.409,
                            "66-86": 0.101,
                            "86-100": 0.02,
                        },
                    },
                    "weekend": {
                        "male": {
                            "0-9": 0.038,
                            "9-15": 0.101,
                            "15-19": 0.106,
                            "19-31": 0.321,
                            "31-51": 0.262,
                            "51-66": 0.304,
                            "66-86": 0.176,
                            "86-100": 0.063,
                        },
                        "female": {
                            "0-9": 0.043,
                            "9-15": 0.081,
                            "15-19": 0.141,
                            "19-31": 0.251,
                            "31-51": 0.231,
                            "51-66": 0.18,
                            "66-86": 0.146,
                            "86-100": 0.06,
                        },
                    },
                },
                "hours_per_day": {
                    "weekday": {
                        "male": {"0-65": 3, "65-100": 11},
                        "female": {"0-65": 3, "65-100": 11},
                    },
                    "weekend": {"male": {"0-100": 12}, "female": {"0-100": 12}},
                },
                "drags_household_probability": 0,
                "neighbours_to_consider": 7,
                "maximum_distance": 10,
            },
            "grocery": {
                "times_per_week": {
                    "weekday": {
                        "male": {
                            "0-9": 0.143,
                            "9-15": 0.196,
                            "15-19": 0.215,
                            "19-31": 0.267,
                            "31-51": 0.381,
                            "51-66": 0.395,
                            "66-86": 0.196,
                            "86-100": 0.065,
                        },
                        "female": {
                            "0-9": 0.236,
                            "9-15": 0.263,
                            "15-19": 0.324,
                            "19-31": 0.492,
                            "31-51": 0.62,
                            "51-66": 0.815,
                            "66-86": 0.246,
                            "86-100": 0.091,
                        },
                    },
                    "weekend": {
                        "male": {
                            "0-9": 0.107,
                            "9-15": 0.114,
                            "15-19": 0.111,
                            "19-31": 0.174,
                            "31-51": 0.201,
                            "51-66": 0.245,
                            "66-86": 0.175,
                            "86-100": 0.082,
                        },
                        "female": {
                            "0-9": 0.111,
                            "9-15": 0.199,
                            "15-19": 0.19,
                            "19-31": 0.229,
                            "31-51": 0.266,
                            "51-66": 0.281,
                            "66-86": 0.229,
                            "86-100": 0.15,
                        },
                    },
                },
                "hours_per_day": {
                    "weekday": {
                        "male": {"0-65": 3, "65-100": 11},
                        "female": {"0-65": 3, "65-100": 11},
                    },
                    "weekend": {"male": {"0-100": 12}, "female": {"0-100": 12}},
                },
                "drags_household_probability": 0,
                "neighbours_to_consider": 15,
                "maximum_distance": 10,
            },
            "gym": {
                "times_per_week": {
                    "weekday": {
                        "male": {
                            "0-9": 0.124,
                            "9-15": 0.231,
                            "15-19": 0.587,
                            "19-31": 0.402,
                            "31-51": 0.274,
                            "51-66": 0.268,
                            "66-86": 0.103,
                            "86-100": 0.019,
                        },
                        "female": {
                            "0-9": 0.404,
                            "9-15": 0.367,
                            "15-19": 0.168,
                            "19-31": 0.213,
                            "31-51": 0.18,
                            "51-66": 0.184,
                            "66-86": 0.036,
                            "86-100": 0.011,
                        },
                    },
                    "weekend": {
                        "male": {
                            "0-9": 0.185,
                            "9-15": 0.19,
                            "15-19": 0.237,
                            "19-31": 0.145,
                            "31-51": 0.13,
                            "51-66": 0.146,
                            "66-86": 0.089,
                            "86-100": 0.0,
                        },
                        "female": {
                            "0-9": 0.074,
                            "9-15": 0.132,
                            "15-19": 0.044,
                            "19-31": 0.067,
                            "31-51": 0.077,
                            "51-66": 0.041,
                            "66-86": 0.031,
                            "86-100": 0.004,
                        },
                    },
                },
                "hours_per_day": {
                    "weekday": {
                        "male": {"0-65": 3, "65-100": 11},
                        "female": {"0-65": 3, "65-100": 11},
                    },
                    "weekend": {"male": {"0-100": 12}, "female": {"0-100": 12}},
                },
                "drags_household_probability": 0,
                "neighbours_to_consider": 7,
                "maximum_distance": 10,
            },
            "cinema": {
                "times_per_week": {
                    "weekday": {
                        "male": {
                            "0-9": 0.0,
                            "9-15": 0.027,
                            "15-19": 0.006,
                            "19-31": 0.016,
                            "31-51": 0.009,
                            "51-66": 0.009,
                            "66-86": 0.015,
                            "86-100": 0.0,
                        },
                        "female": {
                            "0-9": 0.112,
                            "9-15": 0.033,
                            "15-19": 0.099,
                            "19-31": 0.033,
                            "31-51": 0.014,
                            "51-66": 0.031,
                            "66-86": 0.008,
                            "86-100": 0.0,
                        },
                    },
                    "weekend": {
                        "male": {
                            "0-9": 0.019,
                            "9-15": 0.013,
                            "15-19": 0.0,
                            "19-31": 0.0,
                            "31-51": 0.009,
                            "51-66": 0.004,
                            "66-86": 0.01,
                            "86-100": 0.0,
                        },
                        "female": {
                            "0-9": 0.033,
                            "9-15": 0.014,
                            "15-19": 0.014,
                            "19-31": 0.012,
                            "31-51": 0.011,
                            "51-66": 0.01,
                            "66-86": 0.008,
                            "86-100": 0.0,
                        },
                    },
                },
                "hours_per_day": {
                    "weekday": {
                        "male": {"0-65": 3, "65-100": 11},
                        "female": {"0-65": 3, "65-100": 11},
                    },
                    "weekend": {"male": {"0-100": 12}, "female": {"0-100": 12}},
                },
                "drags_household_probability": 0,
                "neighbours_to_consider": 5,
                "maximum_distance": 15,
            },
            "household_visits": {
                "times_per_week": {
                    "weekday": {
                        "male": {
                            "0-9": 2.312,
                            "9-15": 1.715,
                            "15-19": 1.62,
                            "19-31": 1.382,
                            "31-51": 0.629,
                            "51-66": 0.819,
                            "66-86": 0.799,
                            "86-100": 0.473,
                        },
                        "female": {
                            "0-9": 2.331,
                            "9-15": 1.598,
                            "15-19": 2.618,
                            "19-31": 1.37,
                            "31-51": 0.73,
                            "51-66": 1.095,
                            "66-86": 1.113,
                            "86-100": 0.323,
                        },
                    },
                    "weekend": {
                        "male": {
                            "0-9": 1.124,
                            "9-15": 1.107,
                            "15-19": 1.01,
                            "19-31": 0.875,
                            "31-51": 0.444,
                            "51-66": 0.456,
                            "66-86": 0.366,
                            "86-100": 0.149,
                        },
                        "female": {
                            "0-9": 1.485,
                            "9-15": 1.314,
                            "15-19": 1.215,
                            "19-31": 1.036,
                            "31-51": 0.518,
                            "51-66": 0.517,
                            "66-86": 0.447,
                            "86-100": 0.202,
                        },
                    },
                },
                "hours_per_day": {
                    "weekday": {
                        "male": {"0-65": 3, "65-100": 3},
                        "female": {"0-65": 3, "65-100": 3},
                    },
                    "weekend": {"male": {"0-100": 12}, "female": {"0-100": 12}},
                },
                "drags_household_probability": 0,
                "residence_type_probabilities": {"household": 0.66, "care_home": 0.34},
            },
        },
    },
    "interaction": {
        "contact_matrices": {
            "commute": {
                "city_transport": {
                    "contacts": [[6]],
                    "proportion_physical": [[0.07]],
                    "characteristic_time": 2,
                    "type": "Age",
                    "bins": [0, 100],
                },
                "inter_city_transport": {
                    "contacts": [[4]],
                    "proportion_physical": [[0.05]],
                    "characteristic_time": 2,
                    "type": "Age",
                    "bins": [0, 100],
                },
            },
            "grocery": {
                "grocery": {
                    "contacts": [[1.5]],
                    "proportion_physical": [[0.12]],
                    "characteristic_time": 3,
                    "type": "Age",
                    "bins": [0, 100],
                }
            },
            "pub": {
                "pub": {
                    "contacts": [[3]],
                    "proportion_physical": [[0.12]],
                    "characteristic_time": 3,
                    "type": "Age",
                    "bins": [0, 100],
                }
            },
            "cinema": {
                "cinema": {
                    "contacts": [[3]],
                    "proportion_physical": [[0.12]],
                    "characteristic_time": 3,
                    "type": "Age",
                    "bins": [0, 100],
                }
            },
            "company": {
                "company": {
                    "contacts": [[4.8]],
                    "proportion_physical": [[0.07]],
                    "characteristic_time": 8,
                    "type": "Discrete",
                    "bins": ["workers"],
                }
            },
            "household": {
                "household": {
                    "contacts": [
                        [1.368, 1.297, 1.485, 1.485],
                        [1.302, 2.477, 1.312, 1.312],
                        [1.302, 0.928, 1.192, 1.192],
                        [1.302, 0.928, 1.192, 1.305],
                    ],
                    "proportion_physical": [
                        [0.79, 0.7, 0.7, 0.7],
                        [0.7, 0.34, 0.4, 0.4],
                        [0.7, 0.4, 0.62, 0.62],
                        [0.7, 0.62, 0.62, 0.45],
                    ],
                    "characteristic_time": 12,
                    "type": "Discrete",
                    "bins": ["kids", "young_adults", "adults", "old_adults"],
                }
            },
            "gym": {
                "gym": {
                    "contacts": [[3]],
                    "proportion_physical": [[0.12]],
                    "characteristic_time": 3,
                    "type": "Age",
                    "bins": [0, 100],
                }
            },
            "school": {
                "school": {
                    "contacts": [[5, 15], [0.75, 2.5]],
                    "proportion_physical": [[0.05, 0.08], [0.08, 0.15]],
                    "xi": 0.3,
                    "characteristic_time": 8,
                    "type": "Discrete",
                    "bins": ["teachers", "students"],
                }
            },
            "hospital": {
                "hospital": {
                    "contacts": [[5.0, 10.0, 10.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
                    "proportion_physical": [[0.05, 1.0, 1.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
                    "characteristic_time": 8,
                    "type": "Discrete",
                    "bins": ["workers", "patients", "icu_patients"],
                }
            },
        },
        "general": {
            "susceptibilities": {"0-13": 0.5, "13-100": 1.0},
            "alpha_physical": 2.0,
            "betas": {
                "hospital": 0.1168,
                "company": 0.371,
                "household": 0.208,
                "household_visit": 0.208,
                "city_transport": 0.107969,
                "inter_city_transport": 0.383,
                "school": 0.07,
                "pub": 0.42941,
                "gym": 0.42941,
                "grocery": 0.04137,
                "cinema": 0.157461,
            },
        },
    },
}


EXCLUDED_AREAS = [258000, 258100]

AREAS_CONSISTENCY_CHECK = {
    # "geography_hierarchy_definition": None,
    # "super_area_location": None,
    "geography_hierarchy_definition": {"super_area": "super_area", "area": "area"},
    # "geography_hierarchy_definition": None,
    "super_area_location": {"super_area": "super_area"},
    "area_location": {"area": "area"},
    "area_socialeconomic_index": {"area": "area"},
    "gender_profile_female_ratio": {"area": "output_area"},
    "ethnicity_profile": {"area": "output_area"},
    "age_profile": {"area": "output_area"},
    "employees": {"area": "oareas"},
    "employers_by_firm_size": {"super_area": "MSOA"},
    "employers_by_sector": {"super_area": "MSOA"},
    "hospitals": None,
    "schools": None,
    # "hospitals": {"super_area": "super_area", "area": "area"},
    "transport_mode": {"area": "geography"},
    "super_area_name": {"super_area": "super_area"},
    "household_number": {"area": "output_area"},
    "workplace_and_home": {"super_area": ["Area of residence", "Area of workplace"]},
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
    "dormitory": {"building": ["dormitory"]},
}
