from logging import getLogger
from os import remove
from os.path import join

from pandas import DataFrame, merge, read_csv

from process import EXCLUDED_AREAS, REGION_CODES, REGION_NAMES_CONVERSIONS
from process.data.utils import check_list, get_raw_data

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

    return {"data": merged_df, "output": data_path["output"]}


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

    logger.info("area_location is created ...")

    return {"data": data, "output": data_path["output"]}


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

    logger.info("Super_area_location is created ...")

    return {"data": data, "output": data_path["output"]}


def write_geography_hierarchy_definition(
    workdir: str, geography_hierarchy_definition_cfg: dict
) -> dict:
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

    logger.info("Geography_hierarchy_definition is created ...")

    return {"data": data, "output": data_path["output"]}


def write_super_area_name(workdir: str) -> dict:
    """Write super area names

    Args:
        workdir (str): Working directory
    """

    data = {"super_area": [], "city": []}

    for super_area_code in REGION_NAMES_CONVERSIONS:
        if super_area_code == 99:
            continue

        data["super_area"].append(super_area_code)
        data["city"].append(REGION_NAMES_CONVERSIONS[super_area_code])

    df = DataFrame(data)

    output_path = join(workdir, "geography", "super_area_name.csv")
    df.to_csv(output_path, index=False)

    return {"data": df, "output": output_path}

    """
    data_path = get_raw_data(
        workdir,
        super_area_name_cfg,
        "super_area_name",
        "geography",
        force=True,
    )

    data = read_csv(data_path["raw"])

    data = data[["REGC2023_code", "REGC2023_name"]]

    data["REGC2023_name"] = data["REGC2023_name"].str.replace(" Region", "")

    data = data.rename(columns={"REGC2023_code": "super_area", "REGC2023_name": "city"})

    data = data.drop_duplicates()

    data["super_area"] = data["super_area"].astype(str)

    data["city"] = data["city"].replace("Manawatū-Whanganui", "Manawatu-Whanganui")

    data.to_csv(data_path["output"], index=False)

    return {"data": data, "output": data_path["output"]}
    """
