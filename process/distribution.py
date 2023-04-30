from os.path import join
from june.world import World as World_class
from june.distributors import (
    HouseholdDistributor,
    WorkerDistributor,
    HospitalDistributor,
    CompanyDistributor
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


def household_distribution(world: World_class, base_dir: str, distribution_household_cfg: dict):
    """Distribute individuals to household

    Args:
        world (World_class): A world object
        distribution_cfg (dict): Distribution configuration (household)
    """
    household_distributor = HouseholdDistributor.from_file(
        husband_wife_filename = join(
            base_dir, distribution_household_cfg["data"]["age_difference_couple"]),
        parent_child_filename = join(
            base_dir, distribution_household_cfg["data"]["age_difference_parent_child"]),
        config_filename = join(
            base_dir, distribution_household_cfg["cfg"]["household_structure"]),
        number_of_random_numbers=int(1e3)
    )

    household_distributor.household_interaction_filename = join(base_dir, distribution_household_cfg["interaction"])
    
    world.households = (
        household_distributor.distribute_people_and_households_to_areas(
            world.areas,
            number_households_per_composition_filename = join(
                base_dir, distribution_household_cfg["data"]["household_number"]),
            n_students_filename = join(
                base_dir, distribution_household_cfg["data"]["household_student"]),
            n_people_in_communal_filename = join(
                base_dir, distribution_household_cfg["data"]["household_commual"])
        )
    )



def hospital_distribution(world: World_class, base_dir: str, distribution_hospital_cfg: dict):
    """"Distribute individuals to hospitals

    Args:
        world (World_class): A world object
        base_dir (str): Base directory
        distribution_hospital_cfg (dict): Distribution configuration (hospitals)
    """

    hospital_distributor = HospitalDistributor.from_file(
        world.hospitals,
        config_filename=join(base_dir, distribution_hospital_cfg["cfg"]["configs"]))
    hospital_distributor.distribute_medics_to_super_areas(world.super_areas)
    hospital_distributor.assign_closest_hospitals_to_super_areas(
        world.super_areas
    )


def company_distribution(world: World_class):

    company_distributor = CompanyDistributor()
    company_distributor.distribute_adults_to_companies_in_super_areas(
        world.super_areas
    )
    
