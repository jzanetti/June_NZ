from os.path import join

from june.policy import Policies


def create_policy_wrapper(base_dir: str, policy_cfg: dict):
    """Creating a policy

    Args:
        base_dir (str): Base directory
        policy_cfg (dict): Policy configuration

    Returns:
        _type_: _description_
    """
    return Policies.from_file(config_file=join(base_dir, policy_cfg))
