from june.groups.travel import Travel
from os.path import join
from june.world import World as World_class
from logging import getLogger
from process.diags import world2df 

logger = getLogger()

def create_commute_wrapper(world: World_class, base_dir: str, commute_cfg: dict, workdir: str):
    """Creating the commuting object

    Args:
        world (World_class): A world object
        commute_cfg (str): Commute configuration
        base_dir (RootLogger): Base directory
        workdir (str): Working directory

    Returns:
        _type_: _description_
    """
    logger.info("Creating a commute ...")

    commute = create_commute(
        world, 
        base_dir, 
        commute_cfg)
    
    world2df(world, write_csv = True, workdir=workdir, tag="after_commute")

    return commute


def create_commute(world, base_dir: str, commute_cfg: dict):

    travel = Travel(
        city_super_areas_filename = join(
            base_dir, commute_cfg["data"]["super_area_name"]),
        city_stations_filename = join(
            base_dir, commute_cfg["cfg"]["stations"]),
        commute_config_filename = join(
            base_dir, commute_cfg["cfg"]["passage_seats_ratio"]),
        travel_mode_filename = join(
            base_dir, commute_cfg["data"]["transport_mode"]),
        public_or_private_transport = join(
            base_dir, commute_cfg["cfg"]["public_or_private_transport"]),
    )

    travel.initialise_commute(world)

    return travel

