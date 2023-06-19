from os import makedirs
from os.path import exists, join

from pandas import DataFrame
from yaml import dump as yaml_dump

from process import FIXED_DATA


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
