from os import makedirs, system
from os.path import exists, join


def copy_simulation_file(workdir: str, simulation_path: str):
    """Copy simulation to work directory

    Args:
        workdir (str): Working directory
        simulation_path (str): Simulation path
    """
    dest_dir = join(workdir, "simulation")

    if not exists(dest_dir):
        makedirs(dest_dir)

    cmd = f"cp -rf {simulation_path} {dest_dir}/simulation_cfg.yaml"

    system(cmd)
