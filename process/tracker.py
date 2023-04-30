from june.world import World as World_class
from june.tracker.tracker import Tracker
from os.path import join

def create_tracker_groups(world: World_class, interaction_keys: list) -> list:
    """Create tracker groups

    Args:
        world (World_class): The World object
        interaction_keys (dict): interaction configuration keys (e.g., hospital)

    Returns:
        list: The list of groups
    """
    group_types = []
    for interaction_key in interaction_keys:

        if interaction_key == "hospital":
            group_types.append(world.hospitals)
        elif interaction_key == "company":
            group_types.append(world.companies)
        elif interaction_key == "household":
            group_types.append(world.households)
        elif interaction_key == "commute":
            group_types.append(world.city_transports)
            group_types.append(world.inter_city_transports)
    
    return group_types

def create_tracker_wrapper(
        workdir: str,
        world: World_class, 
        interaction_keys: list, 
        combined_interaction_path: str, 
        contact_sexes: list = ["unisex", "male", "female"]):
    """Create tracker

    Args:
        workdir (str): Working directory
        world (World_class): World object
        interaction_keys (dict): Interaction configuration keys
        combined_interaction_path (str): Combined interaction path
        contact_sexes (list, optional): Sex to be applied. Defaults to ["unisex", "male", "female"].

    Returns:
        _type_: _description_
    """

    return Tracker(
        world=world,
        record_path=join(workdir, "output"),
        group_types=create_tracker_groups(world, interaction_keys),
        load_interactions_path=combined_interaction_path,
        contact_sexes=contact_sexes,
        MaxVenueTrackingSize = 500
    )