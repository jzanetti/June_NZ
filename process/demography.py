from copy import deepcopy
from os.path import join

from june.demography import Demography
from june.demography.demography import Demography as Demography_class
from june.geography.geography import Geography as Geography_class
from pandas import DataFrame


def create_person(
    geography: Geography_class, base_dir: str, demography_individual_cfg: dict
) -> Demography_class:
    """Create individual person

    Args:
        geography (Geography_class): Geography (e.g., where people will live)
        base_dir (str): Base configuration folder
        demography_individual_cfg (dict): Demography configuration (individual)
    """

    for gender in ["male", "female"]:
        demography_individual_cfg["comorbidity"][gender] = join(
            base_dir, demography_individual_cfg["comorbidity"][gender]
        )

    demography = Demography.for_geography(
        geography,
        data_path={
            "age_profile": join(base_dir, demography_individual_cfg["age"]),
            "gender_profile": join(base_dir, demography_individual_cfg["gender"]),
            "ethnicity_profile": join(base_dir, demography_individual_cfg["ethnicity"]),
            "comorbidities": demography_individual_cfg["comorbidity"],
        },
    )

    return {"data": demography, "df": demography2df(demography)}


def demography2df(demography_input: Demography_class) -> DataFrame:
    """Convert demography to a dataframe summary

    Args:
        demography (_type_): Calculated demography

    Returns:
        _type_: _description_
    """
    demography = deepcopy(demography_input)
    all_demography = demography.age_sex_generators

    demography_info = {"area": [], "sex": [], "age": [], "ethnicity": []}

    for proc_area_name in all_demography:
        proc_demography = all_demography[proc_area_name]

        all_sex = list(proc_demography.sex_iterator)
        all_age = list(proc_demography.age_iterator)
        all_ethnicity = list(proc_demography.ethnicity_iterator)

        for i in range(proc_demography.n_residents):
            try:
                proc_sex = all_sex[i]
                proc_age = all_age[i]
                proc_ethnicity = all_ethnicity[i]
            except IndexError:
                break

            demography_info["area"].append(proc_area_name)
            demography_info["sex"].append(proc_sex)
            demography_info["age"].append(proc_age)
            demography_info["ethnicity"].append(proc_ethnicity)

    return {"comorbidity": demography.comorbidity_data, "df": DataFrame.from_dict(demography_info)}
