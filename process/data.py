from os import makedirs
from os.path import exists, join

from pandas import read_csv

from process import NORTH_SOUTH_ISLAND_CODES


def write_geography_hierarchy_definition(workdir: str, geography_hierarchy_definition_cfg: dict):
    """Write geography_hierarchy_definition

    Args:
        workdir (str): Working directory
        geography_hierarchy_definition_cfg (dict): geography_hierarchy_definition configuration
    """

    def map_codes(code: str) -> list:
        """Create a mapping function

        Args:
            code (str): Regional code to be mapped

        Returns:
            list: The list contains north and south island
        """
        for key, values in NORTH_SOUTH_ISLAND_CODES.items():
            if code in values:
                return key
        return None

    if not geography_hierarchy_definition_cfg["run"]:
        return

    data = read_csv(geography_hierarchy_definition_cfg["path"])

    data = data[["REGC2023_code", "SA12023_code"]]

    data["region"] = data["REGC2023_code"].map(map_codes)

    data = data.rename(columns={"REGC2023_code": "super_area", "SA12023_code": "area"})

    output_dir = join(workdir, "geography")

    if not exists(output_dir):
        makedirs(output_dir)

    output_path = join(output_dir, "geography_hierarchy_definition.csv")

    data.to_csv(output_path, index=False)
