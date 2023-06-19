from os import makedirs, system
from os.path import exists, join

from pandas import DataFrame
from yaml import dump as yaml_dump

from process import FIXED_DATA


def copy_policy_file(workdir: str, policy_path: str):
    """Copy policy to work directory

    Args:
        workdir (str): Working directory
        policy_path (str): Policy path
    """
    dest_dir = join(workdir, "policy")

    if not exists(dest_dir):
        makedirs(dest_dir)

    cmd = f"cp -rf {policy_path} {dest_dir}/policy.yaml"

    system(cmd)
