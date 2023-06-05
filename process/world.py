from logging import getLogger

from june.demography.demography import Demography as Demography_class
from june.geography.geography import Geography as Geography_class
from june.world import World as World_class
from june.world import generate_world_from_geography

from process.demography import create_person
from process.diags import world2df
from process.distribution import (
    company_distribution,
    hospital_distribution,
    household_distribution,
    school_distribution,
    work_and_home_distribution,
)
from process.groups import create_group_locations

logger = getLogger()


def create_world_wrapper(
    geography_object,
    base_input: str,
    demography_cfg: dict,
    geography_cfg: dict,
    group_and_interaction_cfg: dict,
    disease_cfg: dict,
    workdir: str,
    save_df: bool = False,
) -> World_class:
    """Initialiate a world object

    Args:
        geography_object: Geography object
        workdir (str): working directory
        demography_cfg (dict): Demography configuration

    Returns:
        World: a World object
    """
    # -----------------------------
    # 1. Create Geography dependant groups
    # (e.g., venues such as companies, hospitals ...)
    # -----------------------------
    logger.info("Creating groups (companies, hospitals etc.)...")
    group_object = create_group_locations(
        geography_object["data"], base_input, group_and_interaction_cfg
    )
    geography_object["data"] = group_object["data"]

    logger.info("Creating demography ...")
    person = create_person(
        geography_object["data"], base_input, demography_cfg, disease_cfg["comorbidity"]
    )

    logger.info("Creating the world ...")
    world = create_world(geography_object["data"], person["data"])

    # -----------------------------
    # 2. Assign people with work/work places
    # -----------------------------
    logger.info("Distributing individuals to work/home areas...")
    work_and_home_distribution(world, base_input, group_and_interaction_cfg, geography_cfg)

    # -----------------------------
    # 3. Assign people to fixed interaction objects
    # -----------------------------
    for interaction_obj in group_and_interaction_cfg:
        if interaction_obj in ["others", "commute"]:
            continue

        logger.info(f"Distributing individuals to {interaction_obj} ...")

        if interaction_obj == "household":
            household_distribution(world, base_input, group_and_interaction_cfg["household"])
        elif interaction_obj == "hospital":
            hospital_distribution(world, base_input, group_and_interaction_cfg["hospital"])
        elif interaction_obj == "company":
            company_distribution(world)
        elif interaction_obj == "school":
            school_distribution(world)

    if save_df:
        df = world2df(world, write_csv=True, workdir=workdir, tag="after_init")
    else:
        df = None
    return {"data": world, "df": df}


def create_world(geography: Geography_class, person: Demography_class) -> World_class:
    """Create the World class

    Args:
        geography (Geography_class): Geography class
        demography (Demography_class): Demography class

    Returns:
        World_class: _description_
    """
    return generate_world_from_geography(geography, demography=person)
