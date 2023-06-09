from os.path import join

from june.geography.geography import Geography as Geography_class
from june.groups import Companies, Hospitals, Schools
from june.groups.leisure import Cinemas, Groceries, Gyms, Pubs
from pandas import DataFrame

from process.interaction import LEISURE_OBJS


def create_group_locations(
    geography: Geography_class, base_dir: str, group_and_interaction_cfg: dict
) -> Geography_class:
    """Create groups and attach the groups to geography

    Args:
        geography (Geography_class): Created geography
        base_dir (str): Base directory
        group_and_interaction_cfg (dict): Group and interaction configuration
    """

    output = {"df": {}}
    for group_name in group_and_interaction_cfg:
        if group_name == "hospital":
            geography.hospitals = Hospitals.for_geography(
                geography,
                config_filename=join(
                    base_dir,
                    group_and_interaction_cfg[group_name]["defination"]["neighbour_hospitals"],
                ),
                filename=join(
                    base_dir, group_and_interaction_cfg[group_name]["defination"]["location"]
                ),
            )
            output["df"]["hospital"] = hospital2df(geography)

        elif group_name == "company":
            geography.companies = Companies.for_geography(
                geography,
                size_nr_file=join(
                    base_dir,
                    group_and_interaction_cfg[group_name]["defination"]["employees_by_super_area"],
                ),
                sector_nr_per_msoa_file=join(
                    base_dir,
                    group_and_interaction_cfg[group_name]["defination"]["sectors_by_super_area"],
                ),
            )
            output["df"]["company"] = company2df(geography)

        elif group_name == "school":
            geography.schools = Schools.for_geography(
                geography,
                data_file=join(
                    base_dir, group_and_interaction_cfg[group_name]["defination"]["location"]
                ),
                config_file=None,
            )

        elif group_name == "leisure":
            for leisure_key in group_and_interaction_cfg["leisure"]:
                if leisure_key == "household_visits":
                    continue

                setattr(
                    geography,
                    leisure_key,
                    LEISURE_OBJS[leisure_key].for_geography(
                        geography,
                        coordinates_filename=join(
                            base_dir,
                            group_and_interaction_cfg[group_name][leisure_key]["defination"][
                                "location"
                            ],
                        ),
                        max_distance_to_super_area=200.0,
                    ),
                )

    output["data"] = geography

    return output


def company2df(geography: Geography_class) -> DataFrame:
    """Convert company to Dataframe

    Args:
        geography (Geography_class): Geography dataframe

    Returns:
        DataFrame: Pandas dataframe
    """
    all_companies = geography.companies

    company_info = {
        "region": [],
        "super_area": [],
        "coord": [],
        "name": [],
        "n_workers_max": [],
        "sector": [],
    }

    for proc_company in all_companies.members:
        company_info["region"].append(proc_company.region.name)
        company_info["super_area"].append(proc_company.super_area.name)
        company_info["coord"].append(proc_company.coordinates)
        company_info["name"].append(proc_company.name)
        company_info["n_workers_max"].append(proc_company.n_workers_max)
        company_info["sector"].append(proc_company.sector)

    return DataFrame.from_dict(company_info)


def hospital2df(geography: Geography_class) -> dict:
    """Convert hospital to Dataframe

    Args:
        geography (Geography_class): Geography dataframe

    Returns:
        DataFrame: Pandas dataframe
    """
    all_hospitals = geography.hospitals
    interactions = all_hospitals.venue_class.subgroup_params.params

    hospital_info = {
        "region": [],
        "super_area": [],
        "area": [],
        "coord": [],
        "name": [],
        "n_beds": [],
        "n_icu_beds": [],
    }

    for proc_hospital in all_hospitals.members:
        hospital_info["region"].append(proc_hospital.region.name)
        hospital_info["super_area"].append(proc_hospital.super_area.name)
        hospital_info["area"].append(proc_hospital.area.name)
        hospital_info["coord"].append(proc_hospital.coordinates)
        hospital_info["name"].append(proc_hospital.name)
        hospital_info["n_beds"].append(proc_hospital.n_beds)
        hospital_info["n_icu_beds"].append(proc_hospital.n_icu_beds)

    return {"interactions": interactions, "df": DataFrame.from_dict(hospital_info)}
