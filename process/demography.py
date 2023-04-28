from june.demography import Demography
from june.demography.demography import Demography as Demography_class
from june.geography.geography import Geography as Geography_class
from os.path import join
from pandas import DataFrame
from copy import deepcopy

def create_person(geography: Geography_class, base_dir: str, demography_individual_cfg: dict) -> Demography_class:
    """Create individual person

    Args:
        geography (Geography_class): Geography (e.g., where people will live)
        base_dir (str): Base configuration folder
        demography_individual_cfg (dict): Demography configuration (individual)
    """

    for gender in ["male", "female"]:
        demography_individual_cfg["comorbidity"][gender] = join(
            base_dir,
            demography_individual_cfg["comorbidity"][gender]
        )

    demography = Demography.for_geography(
        geography,
        data_path={
            "age_profile": join(base_dir, demography_individual_cfg["age"]),
            "gender_profile": join(base_dir, demography_individual_cfg["gender"]),
            "ethnicity_profile": join(base_dir, demography_individual_cfg["ethnicity"]),
            "comorbidities": demography_individual_cfg["comorbidity"]
        })

    return {
        "data": demography,
        "df": demography2df(demography)
    }


def demography2df(demography_input: Demography_class) -> DataFrame:
    """Convert demography to a dataframe summary

    Args:
        demography (_type_): Calculated demography

    Returns:
        _type_: _description_
    """
    demography = deepcopy(demography_input)
    all_demography = demography.age_sex_generators

    demography_info = {
        "area": [],
        "sex": [],
        "age": [],
        "ethnicity": []
    }

    for proc_area_name in all_demography:
        proc_demography = all_demography[proc_area_name]

        all_sex = list(proc_demography.sex_iterator)
        all_age = list(proc_demography.age_iterator)
        all_ethnicity = list(proc_demography.ethnicity_iterator)

        for i in range(proc_demography.n_residents):
            demography_info["area"].append(proc_area_name)
            demography_info["sex"].append(all_sex[i])
            demography_info["age"].append(all_age[i])
            demography_info["ethnicity"].append(all_ethnicity[i])
    

    return {
        "comorbidity": demography.comorbidity_data,
        "df": DataFrame.from_dict(demography_info)}