from os import makedirs, system
from os.path import exists, join

from pandas import DataFrame
from yaml import dump as yaml_dump

from process import FIXED_DATA


def copy_disease_cfg(workdir: str, disease_cfg_dir: str):
    """Copy disease configuration to work directory

    Args:
        workdir (str): Working directory
        disease_cfg_dir (str): Disease configuration directory, e.g.,
            etc/cfg/disease/covid-19
    """
    dest_dir = join(workdir, "disease")

    if not exists(dest_dir):
        makedirs(dest_dir)

    cmd = f"cp -rf {disease_cfg_dir}/* {dest_dir}"

    system(cmd)


def write_commorbidity(workdir: str):
    """Convert the fixed commorbidity data

    Args:
        workdir (str): Working directory
    """

    output_dir = join(workdir, "disease")
    if not exists(output_dir):
        makedirs(output_dir)

    for proc_file_key in FIXED_DATA["disease"]:
        proc_data = FIXED_DATA["disease"][proc_file_key]

        if not exists(output_dir):
            makedirs(output_dir)

        if proc_file_key == "comorbidities_intensity":
            with open(join(output_dir, f"{proc_file_key}.yaml"), "w") as fid:
                yaml_dump(proc_data, fid)
        else:
            data = DataFrame.from_dict(proc_data)
            data.to_csv(join(output_dir, f"{proc_file_key}.csv"), index=False)
