from june.groups.travel import Travel
from os.path import join

def create_commute(world, base_dir: str, commute_cfg: dict):

    travel = Travel(
        city_super_areas_filename = join(
            base_dir, commute_cfg["data"]["super_area_name"]),
        city_stations_filename = join(
            base_dir, commute_cfg["cfg"]["stations"]),
        commute_config_filename = join(
            base_dir, commute_cfg["cfg"]["passage_seats_ratio"]),
        travel_mode_filename = join(
            base_dir, commute_cfg["data"]["transport_mode"])
    )

    travel.initialise_commute(world)

    return travel

