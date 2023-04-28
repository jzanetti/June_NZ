from os.path import join
from june.world import World as World_class

def init_worker_distribution(
    world: World_class, 
    base_dir: str, 
    distribution_cfg: dict, 
    group_and_interaction_cfg: dict, 
    population_cfg: dict):
    """Initiate the distribution between worker and homeplace

    Args:
        world (_type_): World object
        base_dir (str): Base directory
        distribution_cfg (dict): Distribution configuration
        group_and_interaction_cfg (dict): Group and interaction configuration
        population_cfg (dict): Population configuration
    """
    world.workflow_file = join(base_dir, distribution_cfg["work_and_home"]["data"])
    world.sex_per_sector_file = join(base_dir, group_and_interaction_cfg["company"]["data"]["sectors_employee_genders"])
    world.policy_config_file = join(base_dir, group_and_interaction_cfg["company"]["cfg"]["company_closure"])
    world.areas_map_path = join(base_dir, population_cfg["geography"]["geography_hierarchy"])