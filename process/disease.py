from june.epidemiology.infection import InfectionSelector, InfectionSelectors
from june.epidemiology.infection_seed import InfectionSeed, InfectionSeeds
from june.world import World as World_class
from june.epidemiology.epidemiology import Epidemiology
from os.path import join

def create_disease_wrapper(world: World_class, base_dir: str, disease_cfg: dict):
    
    selector = InfectionSelector.from_file(
        transmission_config_path = join(base_dir, disease_cfg["cfg"]["transmission_profile"]),
        rates_file = join(base_dir, disease_cfg["data"]["infection_outcome"])
    )

    selectors = InfectionSelectors([selector])
    # selector2df(selectors)
    infection_seed = InfectionSeed.from_uniform_cases(
        world=world, infection_selector=selector, 
        cases_per_capita=0.5,
        date="2020-03-01 9:00", 
        seed_past_infections=False,
    )
    infection_seeds = InfectionSeeds([infection_seed])
    epidemiology = Epidemiology(infection_selectors=selectors, infection_seeds=infection_seeds)

    return epidemiology