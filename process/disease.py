from june.epidemiology.infection import InfectionSelector, InfectionSelectors
from june.epidemiology.infection_seed import InfectionSeed, InfectionSeeds
from june.world import World as World_class
from june.epidemiology.epidemiology import Epidemiology
from os.path import join
from process.utils import read_simulation_info

def create_disease_wrapper(world: World_class, base_dir: str, disease_cfg: dict, simulation_path: str):
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
        transmission_config_path = join(base_dir, disease_cfg["transmission_profile"]),
        rates_file = join(base_dir, disease_cfg["infection_outcome"])
    )

    simulation_info = read_simulation_info(simulation_path)

    selectors = InfectionSelectors([selector])
    # selector2df(selectors)
    infection_seed = InfectionSeed.from_uniform_cases(
        world=world, infection_selector=selector, 
        cases_per_capita=simulation_info["seed_cases_per_capita"],
        date=simulation_info["initial_day"], 
        seed_past_infections=False,
    )
    infection_seeds = InfectionSeeds([infection_seed])
    epidemiology = Epidemiology(infection_selectors=selectors, infection_seeds=infection_seeds)

    return epidemiology