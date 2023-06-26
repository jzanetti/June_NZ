from os.path import join

from june.distributors import (
    CompanyDistributor,
    HospitalDistributor,
    HouseholdDistributor,
    SchoolDistributor,
    WorkerDistributor,
)
from june.geography.geography import Geography as Geography_class
from june.groups.leisure import generate_leisure_for_config
from june.world import World as World_class


def leisure_distribution(
    world: World_class, simulation_cfg_path: str, base_dir: str, group_and_interaction_cfg: dict
):
    """Distribute leisure activities

    Args:
        world (World_class): A world object
        simulation_cfg_path (str): Simulation path,
            e.g., etc/data/singleobs_v2.0/simulation/simulation_cfg.yml
    """
    world.leisure = generate_leisure_for_config(
        world,
        config_filename=simulation_cfg_path,
        pub_config_filename=join(
            base_dir, group_and_interaction_cfg["pubs"]["defination"]["configs"]
        ),
        gym_config_filename=join(
            base_dir, group_and_interaction_cfg["gyms"]["defination"]["configs"]
        ),
        cinema_config_filename=join(
            base_dir, group_and_interaction_cfg["cinemas"]["defination"]["configs"]
        ),
        grocery_config_filename=join(
            base_dir, group_and_interaction_cfg["groceries"]["defination"]["configs"]
        ),
    )
    world.leisure.distribute_social_venues_to_areas(
        areas=world.areas, super_areas=world.super_areas
    )

    x = 3


def work_and_home_distribution(
    world: World_class, base_dir: str, group_and_interaction_cfg: dict, geography_cfg: dict
):
    """Distribute people to different areas using their work and home areas

    Args:
        world (World_class): A world object
        base_dir (str): The base configuration directory
        distribution_cfg (dict): Distribution configuration
        group_and_interaction_cfg (dict): Group and interaction configuration
        geography_cfg (dict): Geography configuration
    """
    worker_distr = WorkerDistributor.for_super_areas(
        area_names=[super_area.name for super_area in world.super_areas],
        workflow_file=join(
            base_dir, group_and_interaction_cfg["commute"]["defination"]["workplace_and_home"]
        ),
        sex_per_sector_file=join(
            base_dir,
            group_and_interaction_cfg["company"]["defination"]["sectors_employee_genders"],
        ),
        config_file=join(
            base_dir, group_and_interaction_cfg["company"]["defination"]["subsector_cfg"]
        ),
        policy_config_file=join(
            base_dir, group_and_interaction_cfg["company"]["defination"]["company_closure"]
        ),
        areas_map_path=join(base_dir, geography_cfg["geography_hierarchy"]),
    )

    worker_distr.non_geographical_work_location = []

    worker_distr.distribute(
        areas=world.areas, super_areas=world.super_areas, population=world.people
    )


def household_distribution(world: World_class, base_dir: str, distribution_household_cfg: dict):
    """Distribute individuals to household

    Args:
        world (World_class): A world object
        distribution_cfg (dict): Distribution configuration (household)
    """
    household_distributor = HouseholdDistributor.from_file(
        husband_wife_filename=join(
            base_dir, distribution_household_cfg["defination"]["age_difference_couple"]
        ),
        parent_child_filename=join(
            base_dir, distribution_household_cfg["defination"]["age_difference_parent_child"]
        ),
        config_filename=join(
            base_dir, distribution_household_cfg["defination"]["household_structure"]
        ),
        number_of_random_numbers=int(1e3),
    )

    household_distributor.household_interaction_filename = join(
        base_dir, distribution_household_cfg["interaction"]
    )

    world.households = household_distributor.distribute_people_and_households_to_areas(
        world.areas,
        number_households_per_composition_filename=join(
            base_dir, distribution_household_cfg["defination"]["household_number"]
        ),
        n_students_filename=join(
            base_dir, distribution_household_cfg["defination"]["household_student"]
        ),
        n_people_in_communal_filename=join(
            base_dir, distribution_household_cfg["defination"]["household_commual"]
        ),
    )


def hospital_distribution(world: World_class, base_dir: str, distribution_hospital_cfg: dict):
    """ "Distribute individuals to hospitals

    Args:
        world (World_class): A world object
        base_dir (str): Base directory
        distribution_hospital_cfg (dict): Distribution configuration (hospitals)
    """

    hospital_distributor = HospitalDistributor.from_file(
        world.hospitals,
        config_filename=join(base_dir, distribution_hospital_cfg["defination"]["configs"]),
    )
    hospital_distributor.distribute_medics_to_super_areas(world.super_areas)
    hospital_distributor.assign_closest_hospitals_to_super_areas(world.super_areas)


def school_distribution(world: World_class):
    school_distributor = SchoolDistributor(world.schools)
    school_distributor.distribute_kids_to_school(world.areas)
    school_distributor.limit_classroom_sizes()
    school_distributor.distribute_teachers_to_schools_in_super_areas(world.super_areas)


def company_distribution(
    world: World_class,
):
    company_distributor = CompanyDistributor()
    company_distributor.distribute_adults_to_companies_in_super_areas(world.super_areas)
