from june.world import generate_world_from_geography
from june.geography.geography import Geography as Geography_class
from june.demography.demography import Demography as Demography_class
from june.world import World as World_class
from process.demography import create_person
from process.groups import create_group_locations
from process.distribution import work_and_home_distribution, household_distribution, hospital_distribution, company_distribution
from process.diags import world2df

from logging import getLogger

logger = getLogger()

def create_world_wrapper(
        geography_object, 
        base_input: str,
        population_cfg: dict,
        distribution_cfg: dict,
        interaction_cfg: dict,
        workdir: str) -> World_class:
    """Initialiate a world object

    Args:
        geography_object: Geography object
        workdir (str): working directory
        cfg (dict): configuration

    Returns:
        World: a World object
    """
    # -----------------------------
    # 1. Create Geography dependant groups 
    # (e.g., venues such as companies, hospitals ...)
    # -----------------------------
    logger.info("Creating groups (companies, hospitals etc.)...")
    group_object = create_group_locations(
        geography_object["data"], 
        base_input, 
        interaction_cfg)
    geography_object["data"] = group_object["data"]

    logger.info("Creating demography ...")
    person = create_person(
        geography_object["data"],
        base_input, 
        population_cfg["demography"]["individual"])
    
    logger.info("Creating the world ...")
    world = create_world(geography_object["data"], person["data"])

    # -----------------------------
    # 2. Assign people with work/work places
    # -----------------------------
    logger.info("Distributing individuals to work/home areas...")
    work_and_home_distribution(
        world,
        base_input, 
        distribution_cfg, 
        interaction_cfg, 
        population_cfg)

    # -----------------------------
    # 3. Assign people to fixed interaction objects
    # -----------------------------
    for interaction_obj in interaction_cfg:
        
        if interaction_obj in ["genneral", "commute"]:
            continue

        logger.info(f"Distributing individuals to {interaction_obj} ...")

        if interaction_obj == "household":
            household_distribution(
                world, 
                base_input, 
                interaction_cfg["household"])
        elif interaction_obj == "hospital":
            hospital_distribution(
                world,
                base_input,
                interaction_cfg["hospital"])
        elif interaction_obj == "hospital":
            company_distribution(world)

    return {
        "data": world,
        "df": world2df(world, write_csv = True, workdir=workdir, tag="after_init")
    }


def create_world(geography: Geography_class, person: Demography_class) -> World_class:
    """Create the World class

    Args:
        geography (Geography_class): Geography class
        demography (Demography_class): Demography class

    Returns:
        World_class: _description_
    """
    return generate_world_from_geography(geography, demography=person)


