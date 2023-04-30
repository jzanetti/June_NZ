from os.path import join
from june.groups import Hospitals, Companies
from june.groups.group.make_subgroups import SubgroupParams
from june.groups.travel.transport import Transport
from june.groups import Household
from yaml import dump as yaml_dump
from yaml import safe_load as yaml_load
from june.interaction import Interaction
from june.groups.group.group import InteractiveGroup

def create_interaction_wrapper(base_dir: str, interaction_cfg: dict, workdir: str):
    """Create interaction object

    Args:
        base_dir (str): Base directory
        interaction_cfg (dict): Interaction configuration
        workdir (str): Working directory

    Returns
        _type_: _description_
    """
    combined_interaction_cfg_path = combine_interaction_cfg(
        workdir, base_dir, interaction_cfg)

    interaction = Interaction.from_file(
        config_filename=combined_interaction_cfg_path
    )

    return {"data": interaction, "path": combined_interaction_cfg_path}




def combine_interaction_cfg(workdir: str, base_dir: str, interaction_cfg: dict) -> str:
    """Combine interaction configurations together

    Args:
        workdir (str): Workding directory
        base_dir (str): Base directory
        interaction_cfg (dict): Interaction configuration
    """
    all_cfg = []

    for proc_group in interaction_cfg:

        if proc_group == "general":
            continue

        proc_cfg = join(base_dir, interaction_cfg[proc_group]["interaction"])

        with open(proc_cfg, "r") as fid:
            cfg = yaml_load(fid)

        all_cfg.append(cfg["contact_matrices"])

    with open(join(base_dir, interaction_cfg["general"]), "r") as fid:
        general_cfg = yaml_load(fid)

    general_cfg["contact_matrices"] = {}

    for proc_key in all_cfg:
        general_cfg["contact_matrices"].update(proc_key)

    combined_interaction_cfg_path = join(workdir, "combined_interaction_cfg.yml")

    with open(combined_interaction_cfg_path, "w") as fid:
        yaml_dump(general_cfg, fid)

    return combined_interaction_cfg_path


def initiate_interaction(base_dir: str, interaction_cfg: dict):
    """Interaction initiation for different groups

    Args:
        base_dir (list): base directory
        interaction (dict): Interaction (for different groups) configuration

    Raises:
        Exception: If the group is not implemented
    """
    for group_name in interaction_cfg:

        if group_name == "general":
            continue
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
            InteractiveGroup.interaction_path= join(
                    base_dir,
                    interaction_cfg["general"])

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
