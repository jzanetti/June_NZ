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
from june.epidemiology.vaccines.vaccination_campaign import (
    VaccinationCampaign,
    VaccinationCampaigns,
)
from june.epidemiology.vaccines.vaccines import Vaccine
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


def get_vaccine_info(vaccine_cfg_path: str):
    """Get vaccine information

    Args:
        vaccine_cfg_path (str): Vaccine configuration path
    """

    with open(vaccine_cfg_path, "r") as fid:
        vaccine_cfg = yaml_safe_load(fid)

    vc = []
    for vaccine_campaign_name in vaccine_cfg:
        vaccine_features = {
            "days_administered_to_effective": [],
            "days_effective_to_waning": [],
            "days_waning": [],
            "sterilisation_efficacies": [],
            "symptomatic_efficacies": [],
        }

        proc_vaccine_cfg = vaccine_cfg[vaccine_campaign_name]["vaccine"]
        proc_campaign_cfg = vaccine_cfg[vaccine_campaign_name]["campaign"]
        total_doeses = proc_campaign_cfg["total_doeses"]
        for proc_vaccine_feature in vaccine_features:
            if proc_vaccine_feature in ["sterilisation_efficacies", "symptomatic_efficacies"]:
                for i in range(total_doeses):
                    feature_values = {}
                    for age_group in proc_vaccine_cfg["efficacies"]:
                        proc_features = proc_vaccine_cfg["efficacies"][age_group][
                            proc_vaccine_feature
                        ][i]
                        for proc_features_key in proc_features:
                            if proc_features_key not in feature_values:
                                feature_values[proc_features_key] = {}
                            feature_values[proc_features_key][age_group] = proc_features[
                                proc_features_key
                            ]

                    vaccine_features[proc_vaccine_feature].append(feature_values)

            else:
                for i in range(total_doeses):
                    vaccine_features[proc_vaccine_feature].append(
                        proc_vaccine_cfg[proc_vaccine_feature][i]
                    )

        vaccine = Vaccine(
            proc_vaccine_cfg["name"],
            days_administered_to_effective=vaccine_features["days_administered_to_effective"],
            days_effective_to_waning=vaccine_features["days_effective_to_waning"],
            days_waning=vaccine_features["days_waning"],
            sterilisation_efficacies=vaccine_features["sterilisation_efficacies"],
            symptomatic_efficacies=vaccine_features["sterilisation_efficacies"],
            waning_factor=proc_vaccine_cfg["waning_factor"],
        )

        days_to_next_dose = proc_campaign_cfg["days_to_next_dose"]  # [0, 59]
        dose_numbers = list(range(total_doeses))  # [0, 1]

        vc.append(
            VaccinationCampaign(
                vaccine=vaccine,
                days_to_next_dose=[days_to_next_dose[dose_number] for dose_number in dose_numbers],
                dose_numbers=dose_numbers,
                start_time=proc_campaign_cfg["start_time"],  # "2020-03-01 9:00"
                end_time=proc_campaign_cfg["end_time"],
                group_by=proc_campaign_cfg["group_by"],
                group_type=proc_campaign_cfg["group_type"],
                group_coverage=proc_campaign_cfg["group_coverage"],
            )
        )

    return VaccinationCampaigns(vc)


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
        vaccination_campaigns = get_vaccine_info(join(base_dir, disease_cfg["vaccine"]))

        # effectiveness = [
        #    {"Delta": {"0-100": 0.3}, "Omicron": {"0-100": 0.3}},
        #    {"Delta": {"0-100": 0.9}, "Omicron": {"0-100": 0.9}},
        # ]
        """
        effectiveness = [{"Covid19": {"0-100": 0.9}}]

        vaccine = Vaccine(
            "Pfizer",
            days_administered_to_effective=[1, 1, 1],
            days_effective_to_waning=[2, 2, 2],
            # days_waning=[10, 10, 10],
            days_waning=[5, 5, 5],
            sterilisation_efficacies=effectiveness,
            symptomatic_efficacies=effectiveness,
            waning_factor=0.8,
        )

        days_to_next_dose = [0]  # [0, 59]
        dose_numbers = [0]  # [0, 1]
        # 2020-03-01
        vc = VaccinationCampaign(
            vaccine=vaccine,
            days_to_next_dose=[days_to_next_dose[dose_number] for dose_number in dose_numbers],
            dose_numbers=dose_numbers,
            start_time="2020-02-25",  # "2020-03-01 9:00"
            end_time="2020-03-02",
            group_by="age",
            group_type="0-100",
            group_coverage=1.0,
        )

        vaccination_campaigns = VaccinationCampaigns([vc])
        """
    epidemiology = Epidemiology(
        infection_selectors=selectors,
        infection_seeds=infection_seeds,
        immunity_setter=multiplier_setter,
        vaccination_campaigns=vaccination_campaigns,
    )

    return epidemiology
