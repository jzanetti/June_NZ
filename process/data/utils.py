from copy import copy as shallow_copy
from logging import getLogger
from math import ceil as math_ceil
from os import listdir, makedirs, remove
from os.path import exists, isfile, join

from numpy import arctan2, argmin, cos, radians, sin, sqrt, unique
from pandas import read_csv
from shapely.wkt import loads as wkt_loads

from process import AREAS_CONSISTENCY_CHECK
from process.utils import download_file

logger = getLogger()


def haversine_distance(lat1, lon1, lat2, lon2):
    """Function to calculate the Haversine distance between two points

    Args:
        lat1 (float): Latitude 1
        lon1 (float): Longitude 1
        lat2 (float): Latitude 1
        lon2 (float): Longitude 2

    Returns:
        _type_: _description_
    """
    r = 6371  # Earth's radius in kilometers
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)
    a = sin(delta_phi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2) ** 2
    c = 2 * arctan2(sqrt(a), sqrt(1 - a))
    distance = r * c
    return distance


def get_central_point(wkt_string: str):
    """Get central point from MultiPolygon

    Args:
        wkt (str): WKT description

    Returns:
        _type_: _description_
    """
    polygon = wkt_loads(wkt_string)
    central_point = polygon.centroid
    return central_point


def remove_super_area(super_area_to_exclude: list, data_list: dict, all_geo: dict) -> dict:
    """Remove super areas from input

    Args:
        super_area_to_exclude (list): Super area to be excluded, e.g.,
            super_area_to_exclude = ["Tasman", "Marlborough"]
    """

    if len(super_area_to_exclude) == 0:
        return

    super_area_name_to_remove = data_list["super_area_name"]["data"]
    geography_hierarchy_definition = data_list["geography_hierarchy_definition"]["data"]
    age_profile = data_list["age_profile"]["data"]

    super_area_name_to_remove = super_area_name_to_remove[
        super_area_name_to_remove["city"].isin(super_area_to_exclude)
    ]["super_area"].to_list()

    super_area_name_to_remove = [int(item) for item in super_area_name_to_remove]

    all_geo["super_area"] = set(
        [item for item in all_geo["super_area"] if item not in super_area_name_to_remove]
    )

    return all_geo


def postproc(data_list: list, scale: float = 1.0, domains_cfg: dict or None = None):
    """Postprocessing the dataset, e.g., match the number of SA2 etc.

    Args:
        data_list (list): data to be checked
    """

    def _find_common_values(sublists):
        # Initialize with the first sublist
        common_values = set(sublists[0])

        # Iterate over the remaining sublists
        for sublist in sublists[1:]:
            common_values = common_values.intersection(sublist)

        return common_values

    # scaling the population
    age_profile = data_list["age_profile"]["data"]
    columns_to_multiply = [col for col in age_profile.columns if col not in ["output_area"]]
    age_profile[columns_to_multiply] = age_profile[columns_to_multiply] * scale

    age_profile[columns_to_multiply] = age_profile[columns_to_multiply].astype(int)
    # age_profile[columns_to_multiply] = age_profile[columns_to_multiply].applymap(math_ceil)

    total_person = age_profile[columns_to_multiply].values.sum()
    logger.info(f"A total of {total_person} person will be used ...")
    # age_profile[columns_to_multiply] = age_profile[columns_to_multiply].astype(int)

    # remove areas with no people live
    age_profile["sum"] = age_profile[columns_to_multiply].sum(axis=1)
    age_profile = age_profile[age_profile["sum"] != 0]

    # remove areas with no people > 18
    cols_to_sum = list(range(18, 101))
    age_profile["sum18"] = age_profile[cols_to_sum].sum(axis=1)
    age_profile = age_profile[age_profile["sum18"] != 0]

    data_list["age_profile"]["data"] = age_profile.drop(["sum", "sum18"], axis=1)

    """
    # remove region, super_area or area as required
    if domains_cfg is not None:
        # domains_cfg = {"region": ["Auckland"], "super_area": None, "area": None}
        geography_hierarchy_definition = shallow_copy(
            data_list["geography_hierarchy_definition"]["data"]
        )
        for domain_key in ["region", "super_area", "area"]:
            proc_domains = domains_cfg[domain_key]

            if proc_domains is not None:
                geography_hierarchy_definition = geography_hierarchy_definition[
                    geography_hierarchy_definition[domain_key].isin(proc_domains)
                ]
        age_profile = age_profile[
            age_profile["output_area"].isin(geography_hierarchy_definition["area"])
        ]

    data_list["age_profile"]["data"] = age_profile
    """

    # get all super_areas/areas:
    all_geo = {"super_area": [], "area": []}
    for data_name in data_list:
        if AREAS_CONSISTENCY_CHECK[data_name] is None:
            continue

        proc_data = data_list[data_name]["data"]

        for area_key in all_geo:
            if area_key in AREAS_CONSISTENCY_CHECK[data_name]:
                data_key = AREAS_CONSISTENCY_CHECK[data_name][area_key]

                all_geo[area_key].append(
                    [int(item) for item in list(unique(proc_data[data_key].values))]
                )

    for area_key in all_geo:
        all_geo[area_key] = _find_common_values(all_geo[area_key])

    # remove region, super_area or area as required
    if domains_cfg is not None:
        # domains_cfg = {"region": ["Auckland"], "super_area": None, "area": None}
        geography_hierarchy_definition = shallow_copy(
            data_list["geography_hierarchy_definition"]["data"]
        )
        for domain_key in ["region", "super_area", "area"]:
            proc_domains = domains_cfg[domain_key]

            if proc_domains is not None:
                geography_hierarchy_definition = geography_hierarchy_definition[
                    geography_hierarchy_definition[domain_key].isin(proc_domains)
                ]

            for area_key in all_geo:
                all_geo[area_key] = all_geo[area_key].intersection(
                    list(geography_hierarchy_definition[area_key].unique())
                )

    # all_geo = remove_super_area(exclude_super_areas, data_list, all_geo)

    # extract data with overlapped areas
    for data_name in data_list:
        if AREAS_CONSISTENCY_CHECK[data_name] is None:
            continue

        proc_data = data_list[data_name]["data"]

        for area_key in ["super_area", "area"]:
            if area_key in AREAS_CONSISTENCY_CHECK[data_name]:
                data_key = AREAS_CONSISTENCY_CHECK[data_name][area_key]

                proc_data[data_key] = proc_data[data_key].astype(int)

                if isinstance(data_key, str):
                    proc_data = proc_data[proc_data[data_key].isin(all_geo[area_key])]
                elif isinstance(data_key, list):
                    if len(data_key) == 2:
                        proc_data = proc_data[
                            proc_data[data_key[0]].isin(all_geo[area_key])
                            & proc_data[data_key[1]].isin(all_geo[area_key])
                        ]
                    else:
                        raise Exception("does not support data_key > 2 at the moment")

        data_list[data_name]["data"] = proc_data

    # write data out
    for data_name in data_list:
        if AREAS_CONSISTENCY_CHECK[data_name] is None:
            continue
        logger.info(f"Updating {data_name} ...")
        data_list[data_name]["data"].to_csv(data_list[data_name]["output"], index=False)


def check_list(list1: list, list2: list) -> list:
    """Check if two lists are identical

    Args:
        list1 (list): _description_
        list2 (list): _description_

    Returns:
        bool: _description_
    """

    return list(set(list1) - set(list2))


def housekeeping(dir_path: str, extensions_to_delete: list = [".xls", ".csv", ".xlsx"]):
    """Remove downloaded raw files

    Args:
        dir_path (str): Working directories
        extensions_to_delete (list, optional): Extensions to be deleted. Defaults to [".xls", ".csv", ".xlsx"].
    """
    for file in listdir(dir_path):
        if isfile(join(dir_path, file)) and file.endswith(tuple(extensions_to_delete)):
            file_path = join(dir_path, file)
            remove(file_path)


def get_raw_data(
    workdir: str, cfg: dict, name: str, data_group: str, force: bool = False, deps: bool = False
) -> str or None:
    """Download raw data if does not exists, and return the downloaded data path

    Args:
        workdir (str): Workding directory
        cfg (dict): Configuration for the data
        name (str): Name of the data
        data_group (str): Data group name, e.g.,geography or group/company
        force (bool): if force the regeneration of data
        deps (bool): if get the deps data

    Returns:
        dict or None: The download data path
    """
    if not cfg["run"] and not force:
        logger.info(f"Generating {name} is skipped ...")
        return None

    output_dir = join(workdir, data_group)

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

    deps = {}
    if cfg["deps"] is not None:
        for proc_data in cfg["deps"]:
            proc_deps_path = cfg["deps"][proc_data]

            if proc_deps_path.startswith("https"):
                proc_deps_raw_data_path = download_file(proc_deps_path, workdir=workdir)
            else:
                proc_deps_raw_data_path = join(workdir, proc_deps_path + ".csv")
            deps[proc_data] = proc_deps_raw_data_path

    return {"raw": raw_data_path, "output": output_path, "deps": deps}
