from logging import getLogger
from os import makedirs, remove
from os.path import exists, join

from pandas import read_csv

from process import REGION_CODES, REGION_NAMES_CONVERSIONS
from process.utils import download_file

logger = getLogger()


def get_raw_data(workdir: str, cfg: dict, name: str, force: bool = False) -> str or None:
    """Download raw data if does not exists, and return the downloaded data path

    Args:
        workdir (str): Workding directory
        cfg (dict): Configuration for the data
        name (str): Name of the data
        force (bool): if force the regeneration of data

    Returns:
        dict or None: The download data path
    """
    if not cfg["run"] and not force:
        logger.info(f"Generating {name} is skipped ...")
        return None

    output_dir = join(workdir, "geography")

    if not exists(output_dir):
        makedirs(output_dir)

    output_path = join(output_dir, f"{name}.csv")

    if exists(output_path) and not force:
        logger.info(f"{name} exists ...")
        return None

    if cfg["path"].startswith("https"):
        raw_data_path = download_file(cfg["path"], workdir=workdir)
    else:
        raw_data_path = cfg["path"]

    return {"raw": raw_data_path, "output": output_path}


def write_super_area_location(workdir: str, super_area_location_cfg: dict):
    """Write super_area_location data

    Args:
        workdir (str): Working directory
        super_area_location_cfg (dict): Super area location configuration
    """
    data_path = get_raw_data(workdir, super_area_location_cfg, "super_area_location", force=True)

    if data_path is None:
        return

    data = read_csv(data_path["raw"])

    data["Region"] = data["Region"].map(
        {value: key for key, value in REGION_NAMES_CONVERSIONS.items()}
    )

    data = data.rename(
        columns={"Region": "super_area", "Latitude": "latitude", "Longitude": "longitude"}
    )

    data.to_csv(data_path["output"], index=False)

    remove(data_path["raw"])

    logger.info("Super_area_location is created ...")


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
        for key, values in REGION_CODES.items():
            if code in values:
                return key
        return None

    data_path = get_raw_data(
        workdir, geography_hierarchy_definition_cfg, "geography_hierarchy_definition", force=True
    )

    if data_path is None:
        return

    data = read_csv(data_path["raw"])

    data = data[["REGC2023_code", "SA22018_code"]]

    data = data[~data["REGC2023_code"].isin(REGION_CODES["Others"])]

    data["region"] = data["REGC2023_code"].map(map_codes)

    data = data.rename(columns={"REGC2023_code": "super_area", "SA22018_code": "area"})

    data.to_csv(data_path["output"], index=False)

    remove(data_path["raw"])

    logger.info("Geography_hierarchy_definition is created ...")
