from os import makedirs, system
from os.path import exists, join


def copy_vaccine_file(workdir: str, vaccine_path: str):
    """Copy vaccine configuration to work directory

    Args:
        workdir (str): Working directory
        simulation_path (str): Vaccine path
    """
    dest_dir = join(workdir, "vaccine")

    if not exists(dest_dir):
        makedirs(dest_dir)

    cmd = f"cp -rf {vaccine_path} {dest_dir}/vaccine.yaml"

    system(cmd)
