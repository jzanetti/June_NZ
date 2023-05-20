from logging import getLogger
from os import makedirs
from os.path import exists, join

from process.utils import download_file

logger = getLogger()


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
