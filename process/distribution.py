from os.path import join
from june.world import World as World_class
from june.distributors import (
    HouseholdDistributor,
    WorkerDistributor
)


def work_and_home_distribution(
        world: World_class,
        base_dir: str, 
        distribution_cfg: dict,
        group_and_interaction_cfg: dict, 
        population_cfg: dict):
    """Distribute people to different areas using their work and home areas

    Args:
        world (World_class): A world object
        base_dir (str): The base configuration directory
        distribution_cfg (dict): Distribution configuration
        group_and_interaction_cfg (dict): Group and interaction configuration
        population_cfg (dict): Population configuration
    """
    worker_distr = WorkerDistributor.for_super_areas(
        area_names=[super_area.name for super_area in world.super_areas],
        workflow_file = join(base_dir, distribution_cfg["work_and_home"]["data"]),
        sex_per_sector_file = join(base_dir, group_and_interaction_cfg["company"]["data"]["sectors_employee_genders"]),
        config_file = join(base_dir, distribution_cfg["work_and_home"]["cfg"]),
        policy_config_file = join(base_dir, group_and_interaction_cfg["company"]["cfg"]["company_closure"]),
        areas_map_path = join(base_dir, population_cfg["geography"]["geography_hierarchy"])
        )
        
    worker_distr.distribute(
        areas=world.areas, 
        super_areas=world.super_areas, 
        population=world.people
    )


def household_distribution(world: World_class, base_dir: str, distribution_cfg: dict):
    """Distribute individuals to household

    Args:
        world (World_class): A world object
        distribution_cfg (dict): Distribution configuration
    """
    household_distributor = HouseholdDistributor.from_file(
        husband_wife_filename = join(
            base_dir, distribution_cfg["household"]["data"]["age_difference_couple"]),
        parent_child_filename = join(
            base_dir, distribution_cfg["household"]["data"]["age_difference_parent_child"]),
        config_filename = join(
            base_dir, distribution_cfg["household"]["cfg"]["household_structure"]),
        number_of_random_numbers=int(1e3)
    )

    world.households = (
        household_distributor.distribute_people_and_households_to_areas(
            world.areas,
            number_households_per_composition_filename = join(
                base_dir, distribution_cfg["household"]["data"]["household_number"]),
            n_students_filename = join(
                base_dir, distribution_cfg["household"]["data"]["household_student"]),
            n_people_in_communal_filename = join(
                base_dir, distribution_cfg["household"]["data"]["household_commual"])
        )
        )