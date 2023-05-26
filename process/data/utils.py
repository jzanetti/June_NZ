from logging import getLogger
from os import listdir, makedirs, remove
from os.path import exists, isfile, join

from numpy import unique

from process import AREAS_CONSISTENCY_CHECK
from process.utils import download_file

logger = getLogger()


def postproc(data_list: list):
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

    # get all super_areas/areas:
    all_geo = {"super_area": [], "area": []}
    for data_name in data_list:
        if AREAS_CONSISTENCY_CHECK[data_name] is None:
            continue

        proc_data = data_list[data_name]["data"]

        for area_key in all_geo:
            if area_key in AREAS_CONSISTENCY_CHECK[data_name]:
                all_geo[area_key].append(
                    [
                        int(item)
                        for item in list(
                            unique(proc_data[AREAS_CONSISTENCY_CHECK[data_name][area_key]].values)
                        )
                    ]
                )

    for area_key in all_geo:
        all_geo[area_key] = _find_common_values(all_geo[area_key])

    # extract data with overlapped areas
    for data_name in data_list:
        if AREAS_CONSISTENCY_CHECK[data_name] is None:
            continue

        proc_data = data_list[data_name]["data"]

        for area_key in ["super_area", "area"]:
            if area_key in AREAS_CONSISTENCY_CHECK[data_name]:
                proc_data[AREAS_CONSISTENCY_CHECK[data_name][area_key]] = proc_data[
                    AREAS_CONSISTENCY_CHECK[data_name][area_key]
                ].astype(int)

                proc_data = proc_data[
                    proc_data[AREAS_CONSISTENCY_CHECK[data_name][area_key]].isin(all_geo[area_key])
                ]

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
