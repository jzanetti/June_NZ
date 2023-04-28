from os.path import join
from june.groups import Hospitals, Companies


def init_interaction(base_dir: str, group_and_interaction: dict):
    """Interaction initiation for different groups

    Args:
        base_dir (list): base directory
        group_and_interaction (dict): Interaction (for different groups) configuration

    Raises:
        Exception: If the group is not implemented
    """
    for group_name in group_and_interaction:
        if group_name == "hospital":
            Hospitals.get_interaction(
                join(
                    base_dir,
                    group_and_interaction["hospital"]["interaction"])
                )

        elif group_name == "company":
            Companies.get_interaction(
                join(
                    base_dir,
                    group_and_interaction["company"]["interaction"])
                )
        
        else:
            raise Exception(f"{group_name} has not been implemented in init_interaction ...")