from logging import getLogger
from os import remove
from os.path import join

from pandas import DataFrame, merge, read_csv

from process import EXCLUDED_AREAS, REGION_CODES, REGION_NAMES_CONVERSIONS
from process.data.utils import check_list, get_raw_data

logger = getLogger()


def write_area_socialeconomic_index(
    workdir: str,
    area_socialeconomic_index_cfg: dict,
    geography_hierarchy_definition: DataFrame or None = None,
):
    """Write area area_socialeconomic_index data

    Args:
        workdir (str): Working directory
        area_socialeconomic_index_cfg (dict): Area_socialeconomic_index configuration
        geography_hierarchy_definition (DataFrame or None): Geography hierarchy definition
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
    geog_hierarchy = geography_hierarchy_definition[["super_area", "area"]]

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


def write_super_area_location(
    workdir: str,
    use_sa3_as_super_area: bool,
    geograph_cfg: dict,
    geography_hierarchy_definition: DataFrame or None,
):
    """Write super_area_location data

    Args:
        workdir (str): Working directory
        use_sa3_as_super_area (bool): Use SA3 as super area, otherwise use regions
        super_area_location_cfg (dict): Super area location configuration
        geography_hierarchy_definition (DataFrame or None): Geography hierarchy definition
    """
    if use_sa3_as_super_area:
        data_path = get_raw_data(
            workdir, geograph_cfg["area_location"], "area_location", "geography", force=True
        )
    else:
        data_path = get_raw_data(
            workdir,
            geograph_cfg["super_area_location"],
            "super_area_location",
            "geography",
            force=True,
        )

    if data_path is None:
        return

    data = read_csv(data_path["raw"])

    if use_sa3_as_super_area:
        data = data[["SA22018_V1_00", "LATITUDE", "LONGITUDE"]]

        data = data.rename(
            columns={"SA22018_V1_00": "area", "LATITUDE": "latitude", "LONGITUDE": "longitude"}
        )

        if geography_hierarchy_definition is None:
            raise Exception(
                "use_sa3_as_super_area is enabled, however geography_hierarchy_definition is not set ..."
            )

        data = merge(data, geography_hierarchy_definition, on="area", how="inner")

        data = data.groupby("super_area")[["latitude", "longitude"]].mean().reset_index()

    else:
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
    workdir: str, use_sa3_as_super_area: bool, geography_hierarchy_definition_cfg: dict
) -> dict:
    """Write geography_hierarchy_definition

    Args:
        workdir (str): Working directory
        use_sa3_as_super_area (bool): Use SA3 as super area, otherwise we will use regions
        geography_hierarchy_definition_cfg (dict): geography_hierarchy_definition configuration
    """

    def _map_codes1(code: str) -> list:
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

    def _map_codes2(code: str) -> list:
        """Create a mapping function

        Args:
            code (str): Regional code to be mapped

        Returns:
            list: The list contains north and south island
        """
        for key, values in REGION_NAMES_CONVERSIONS.items():
            if code == key:
                return values
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

    if use_sa3_as_super_area:
        data = data[["REGC2023_code", "SA32023_code", "SA32023_name", "SA22023_code"]]

        data = data[~data["REGC2023_code"].isin(REGION_CODES["Others"])]

        data["REGC2023_name"] = data["REGC2023_code"].map(_map_codes2)

        data = data.rename(
            columns={
                "REGC2023_name": "region",
                "SA32023_code": "super_area",
                "SA22023_code": "area",
                "SA32023_name": "super_area_name",
            }
        ).drop_duplicates()

        data = data[["region", "super_area", "area", "super_area_name"]]

    else:
        data = data[["REGC2023_code", "SA22018_code"]]

        data = data[~data["REGC2023_code"].isin(REGION_CODES["Others"])]

        data["region"] = data["REGC2023_code"].map(_map_codes1)

        data = data.rename(
            columns={"REGC2023_code": "super_area", "SA22018_code": "area"}
        ).drop_duplicates()

    data.to_csv(data_path["output"], index=False)

    logger.info("Geography_hierarchy_definition is created ...")

    return {"data": data, "output": data_path["output"]}


def write_super_area_name(
    workdir: str,
    use_sa3_as_super_area: bool,
    geography_hierarchy_definition_cfg: dict or None = None,
) -> dict:
    """Write super area names

    Args:
        workdir (str): Working directory
        use_sa3_as_super_area (bool): Use SA3 as super area, otherwise we will use regions
        geography_hierarchy_definition_cfg (dict or None): Geography hierarchy definition configuration
    """

    data = {"super_area": [], "city": []}

    if use_sa3_as_super_area:
        if geography_hierarchy_definition_cfg is None:
            raise Exception(
                "use_sa3_as_super_area is enabled, but geography_hierarchy_definition_cfg is None ..."
            )

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
        data = data[["SA32023_code", "SA32023_name"]]
        df = data.rename(columns={"SA32023_code": "super_area", "SA32023_name": "city"})
        df = df.drop_duplicates()

    else:
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
