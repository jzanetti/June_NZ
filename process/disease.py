from os.path import join

from june.epidemiology.epidemiology import Epidemiology
from june.epidemiology.infection import (
    B117,
    B16172,
    Covid19,
    ImmunitySetter,
    InfectionSelector,
    InfectionSelectors,
)
from june.epidemiology.infection.health_index.data_to_rates import (
    convert_comorbidities_prevalence_to_dict,
    read_comorbidity_csv,
)
from june.epidemiology.infection_seed import InfectionSeed, InfectionSeeds
from june.world import World as World_class
from yaml import safe_load as yaml_safe_load

from process.utils import read_simulation_info


def create_comorbidity_info(base_dir: str, comorbidity_cfg: dict) -> dict:
    """Create comorbidity information

    Args:
        base_dir (str): Base directory
        comorbidity_cfg (dict): Comorbidity configuration

    Returns:
        dict: Comorbidity information
    """
    prevalence_female = read_comorbidity_csv(join(base_dir, comorbidity_cfg["female"]))
    prevalence_male = read_comorbidity_csv(join(base_dir, comorbidity_cfg["male"]))

    comorbidity_prevalence = convert_comorbidities_prevalence_to_dict(
        prevalence_female, prevalence_male
    )

    with open(join(base_dir, comorbidity_cfg["intensity"]), "r") as stream:
        comorbidity_intensity = yaml_safe_load(stream)

    return {
        "comorbidity_prevalence": comorbidity_prevalence,
        "comorbidity_intensity": comorbidity_intensity,
    }


def create_virus_info(base_dir: str, virus_cfg: dict) -> dict:
    """Get virus intensity

    Args:
        base_dir (str): Base data directory
        virus_cfg (dict): Virus configuration
    """
    with open(join(base_dir, virus_cfg["intensity"]), "r") as stream:
        virus_intensity = yaml_safe_load(stream)

    virus_intensity_output = {}
    for virus_key in virus_intensity:
        if virus_key == "Covid19":
            virus_intensity_output[Covid19.infection_id()] = virus_intensity[virus_key]
        elif virus_key == "B117":
            virus_intensity_output[B117.infection_id()] = virus_intensity[virus_key]
        elif virus_key == "B16172":
            virus_intensity_output[B16172.infection_id()] = virus_intensity[virus_key]

    return {"virus_intensity": virus_intensity_output}


def create_disease_wrapper(
    world: World_class, base_dir: str, disease_cfg: dict, simulation_path: str
):
    """Create disease wrapper

    Args:
        world (World_class): An world class
        base_dir (str): Base directory
        disease_cfg (dict): Disease configuration
        simulation_path (str): Simulation configuration path

    Returns:
        _type_: Epidemiology object
    """
    selector = InfectionSelector.from_file(
        transmission_config_path=join(base_dir, disease_cfg["transmission_profile"]),
        rates_file=join(base_dir, disease_cfg["infection_outcome"]),
    )

    simulation_info = read_simulation_info(simulation_path)

    selectors = InfectionSelectors([selector])
    infection_seed = InfectionSeed.from_uniform_cases(
        world=world,
        infection_selector=selector,
        cases_per_capita=simulation_info["seed_cases_per_capita"],
        date=simulation_info["initial_day"],
        seed_past_infections=False,
    )
    infection_seeds = InfectionSeeds([infection_seed])

    """
    female_filename = (
        "/home/zhangs/Github/June_NZ/etc/data/singleobs/demography/comorbidities_female.csv"
    )
    male_filename = (
        "/home/zhangs/Github/June_NZ/etc/data/singleobs/demography/comorbidities_male.csv"
    )
    prevalence_female = read_comorbidity_csv(female_filename)
    prevalence_male = read_comorbidity_csv(male_filename)

    prevalence_reference_population = convert_comorbidities_prevalence_to_dict(
        prevalence_female, prevalence_male
    )

    comorbidity_multipliers = {"disease1": 0.8, "disease2": 1.2, "no_condition": 1.0}
    """
    comorbidity_info = create_comorbidity_info(base_dir, disease_cfg["comorbidity"])
    virus_info = create_virus_info(base_dir, disease_cfg["virus"])

    # A dictionary mapping infection_id -> symptoms reduction by age.
    # infection_id = {"Covid19": 170852960, "B117": 37224668, "B16172": 76677444}
    # multiplier_dict = {
    #    infection_id["Covid19"]: {"0-50": 1.0, "50-100": 1.5},
    #    infection_id["B117"]: {"0-50": 1.0, "50-100": 1.5},
    #    infection_id["B16172"]: {"0-50": 1.0, "50-100": 1.5},
    # }

    multiplier_setter = ImmunitySetter(
        multiplier_by_comorbidity=comorbidity_info["comorbidity_intensity"],
        comorbidity_prevalence_reference_population=comorbidity_info["comorbidity_prevalence"],
        multiplier_dict=virus_info["virus_intensity"],
    )

    epidemiology = Epidemiology(
        infection_selectors=selectors,
        infection_seeds=infection_seeds,
        immunity_setter=multiplier_setter,
    )

    return epidemiology
