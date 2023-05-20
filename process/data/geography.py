from logging import getLogger
from os import remove
from os.path import join

from pandas import merge, read_csv

from process import REGION_CODES, REGION_NAMES_CONVERSIONS
from process.data.utils import get_raw_data

logger = getLogger()


def write_area_socialeconomic_index(workdir: str, area_socialeconomic_index_cfg: dict):
    """Write area area_socialeconomic_index data

    Args:
        workdir (str): Working directory
        area_socialeconomic_index_cfg (dict): Area_socialeconomic_index configuration
    """
    data_path = get_raw_data(
        workdir,
        area_socialeconomic_index_cfg,
        "area_socialeconomic_index",
        "geography",
        force=True,
    )
    if data_path is None:
        return
    data = read_csv(data_path["raw"])[["SA22018_code", "SA2_average_NZDep2018"]]

    data = data.rename(
        columns={
            "SA22018_code": "area",
            "SA2_average_NZDep2018": "socioeconomic_centile",
        }
    )

    # get hierarchy defination data
    geog_hierarchy = read_csv(
        join(
            workdir,
            area_socialeconomic_index_cfg["deps"]["geography_hierarchy_definition"] + ".csv",
        )
    )[["super_area", "area"]]

    merged_df = merge(data, geog_hierarchy, on="area")

    merged_df.to_csv(data_path["output"], index=False)

    remove(data_path["raw"])

    logger.info("area_socialeconomic_index is created ...")


def write_area_location(workdir: str, area_location_cfg: dict):
    """Write area location data

    Args:
        workdir (str): Working directory
        area_location_cfg (dict): Area location configuration
    """
    data_path = get_raw_data(workdir, area_location_cfg, "area_location", "geography", force=True)
    if data_path is None:
        return

    data = read_csv(data_path["raw"])

    data = data[["SA22018_V1_00", "LATITUDE", "LONGITUDE"]]

    data = data.rename(
        columns={"SA22018_V1_00": "area", "LATITUDE": "latitude", "LONGITUDE": "longitude"}
    )

    data.to_csv(data_path["output"], index=False)

    remove(data_path["raw"])

    logger.info("area_location is created ...")


def write_super_area_location(workdir: str, super_area_location_cfg: dict):
    """Write super_area_location data

    Args:
        workdir (str): Working directory
        super_area_location_cfg (dict): Super area location configuration
    """
    data_path = get_raw_data(
        workdir, super_area_location_cfg, "super_area_location", "geography", force=True
    )

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
        workdir,
        geography_hierarchy_definition_cfg,
        "geography_hierarchy_definition",
        "geography",
        force=True,
    )

    if data_path is None:
        return

    data = read_csv(data_path["raw"])

    data = data[["REGC2023_code", "SA22018_code"]]

    data = data[~data["REGC2023_code"].isin(REGION_CODES["Others"])]

    data["region"] = data["REGC2023_code"].map(map_codes)

    data = data.rename(
        columns={"REGC2023_code": "super_area", "SA22018_code": "area"}
    ).drop_duplicates()

    data.to_csv(data_path["output"], index=False)

    remove(data_path["raw"])

    logger.info("Geography_hierarchy_definition is created ...")
