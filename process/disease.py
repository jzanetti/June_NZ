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
    world: World_class,
    base_dir: str,
    disease_cfg: dict,
    simulation_path: str,
    apply_vaccine: bool = False,
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

    comorbidity_info = create_comorbidity_info(base_dir, disease_cfg["comorbidity"])
    virus_info = create_virus_info(base_dir, disease_cfg["virus"])

    multiplier_setter = ImmunitySetter(
        multiplier_by_comorbidity=comorbidity_info["comorbidity_intensity"],
        comorbidity_prevalence_reference_population=comorbidity_info["comorbidity_prevalence"],
        multiplier_dict=virus_info["virus_intensity"],
    )

    vaccination_campaigns = None
    if apply_vaccine:
        from june.epidemiology.vaccines.vaccination_campaign import (
            VaccinationCampaign,
            VaccinationCampaigns,
        )
        from june.epidemiology.vaccines.vaccines import Vaccine

        effectiveness = [
            {"Delta": {"0-100": 0.3}, "Omicron": {"0-100": 0.3}},
            {"Delta": {"0-100": 0.9}, "Omicron": {"0-100": 0.9}},
        ]

        vaccine = Vaccine(
            "Pfizer",
            days_administered_to_effective=[5, 5, 5],
            days_effective_to_waning=[2, 2, 2],
            days_waning=[10, 10, 10],
            sterilisation_efficacies=effectiveness,
            symptomatic_efficacies=effectiveness,
            waning_factor=0.5,
        )

        days_to_next_dose = [0, 59]
        dose_numbers = [0, 1]
        # 2020-03-01
        vc = VaccinationCampaign(
            vaccine=vaccine,
            days_to_next_dose=[days_to_next_dose[dose_number] for dose_number in dose_numbers],
            dose_numbers=dose_numbers,
            start_time="2020-03-01",
            end_time="2020-03-11",
            group_by="age",
            group_type="0-100",
            group_coverage=1.0,
        )

        vaccination_campaigns = (VaccinationCampaigns([vc]),)

    epidemiology = Epidemiology(
        infection_selectors=selectors,
        infection_seeds=infection_seeds,
        immunity_setter=multiplier_setter,
        vaccination_campaigns=vaccination_campaigns,
    )

    return epidemiology
