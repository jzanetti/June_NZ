from os.path import join
from june.groups import Hospitals, Companies
from june.groups.group.make_subgroups import SubgroupParams
from june.groups.travel.transport import Transport
from june.groups import Household

def create_interaction_wrapper(base_dir: str, interaction_cfg: dict):
    """Interaction initiation for different groups

    Args:
        base_dir (list): base directory
        interaction (dict): Interaction (for different groups) configuration

    Raises:
        Exception: If the group is not implemented
    """
    for group_name in interaction_cfg:
        if group_name == "hospital":
            Hospitals.get_interaction(
                join(
                    base_dir,
                    interaction_cfg["hospital"]["interaction"])
                )

        elif group_name == "company":
            Companies.get_interaction(
                join(
                    base_dir,
                    interaction_cfg["company"]["interaction"])
                )
        elif group_name == "commute":
            mytransport = Transport
            mytransport.subgroup_params = SubgroupParams.from_file(
                config_filename=join(
                    base_dir, interaction_cfg["commute"]["interaction"])
            )

        elif group_name == "household":
            my_household= Household
            my_household.subgroup_params = SubgroupParams.from_file(
                config_filename=join(
                    base_dir, interaction_cfg["household"]["interaction"])
            )
        else:
            raise Exception(f"{group_name} has not been implemented in init_interaction ...")