from os.path import join

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
    for proc_file_key in leisure_types:
        output_path = join(workdir, "interaction", f"{proc_file_key}.yaml")

        with open(output_path, "w") as fid:
            yaml_dump(
                {"contact_matrices": FIXED_DATA["interaction"]["contact_matrices"][proc_file_key]},
                fid,
                default_flow_style=False,
            )

    output_path = join(workdir, "interaction", "general.yaml")

    with open(output_path, "w") as fid:
        yaml_dump(
            FIXED_DATA["interaction"]["general"],
            fid,
            default_flow_style=False,
        )
