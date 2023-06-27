from os import makedirs
from os.path import exists, join

from yaml import dump as yaml_dump

from process import FIXED_DATA


def write_interaction(
    workdir: str,
    leisure_types: list = [
        "cinema",
        "commute",
        "company",
        "grocery",
        "gym",
        "hospital",
        "household",
        "household_visit",
        "pub",
        "school",
    ],
):
    """Write interaction data

    Args:
        workdir (str): Working directory
        leisure_types (list, optional): Leisure activities.
            Defaults to [ "cinema", "commute", "company", "grocery", "gym", "hospital", "household", "pub", "school", ].
    """

    output_dir = join(workdir, "interaction")

    if not exists(output_dir):
        makedirs(output_dir)

    for proc_file_key in leisure_types:
        if proc_file_key == "household_visit":
            continue

        output_path = join(output_dir, f"{proc_file_key}.yaml")

        with open(output_path, "w") as fid:
            yaml_dump(
                {"contact_matrices": FIXED_DATA["interaction"]["contact_matrices"][proc_file_key]},
                fid,
                default_flow_style=False,
            )

    output_path = join(output_dir, "general.yaml")

    with open(output_path, "w") as fid:
        yaml_dump(
            FIXED_DATA["interaction"]["general"],
            fid,
            default_flow_style=False,
        )
