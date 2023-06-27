from datetime import datetime
from logging import INFO, Formatter, StreamHandler, basicConfig, getLogger
from os.path import basename, exists, join
from subprocess import PIPE, Popen

from yaml import safe_load as yaml_load


def move_item_to_end(item: str, my_list: list) -> list:
    """Move an item to the end of list, e.g.,
        it is useful when we need to move "leisure" behind "household" when we
        process interaction, since "leisure" contains "household visit"

    Args:
        item (str): item to be moved
        my_list (list): original list
    """
    if item in my_list:
        my_list.remove(item)  # Remove the item from its current position
        my_list.append(item)  # Append the item to the end

    return my_list


def download_file(url: str, workdir: str = "/tmp") -> str:
    """Download a file from URL to local

    Args:
        url (str): URL to be downloaded
        workdir (str, optional): Working directory. Defaults to "/tmp".

    Returns:
        str: Downloaded path
    """
    local_path = join(workdir, basename(url))

    command = ["wget", url, "-O", local_path]

    process = Popen(command, stdout=PIPE, stderr=PIPE)
    _, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error message when download {url}: {stderr.decode()}")

    return local_path


def setup_logging(workdir: str = "/tmp", start_utc: datetime = datetime.utcnow()):
    """set up logging system for tasks

    Returns:
        object: a logging object
    """
    formatter = Formatter("%(asctime)s - %(name)s.%(lineno)d - %(levelname)s - %(message)s")
    ch = StreamHandler()
    ch.setLevel(INFO)
    ch.setFormatter(formatter)
    logger_path = join(workdir, f"june_nz.{start_utc.strftime('%Y%m%d')}")
    basicConfig(filename=logger_path),
    logger = getLogger()
    logger.setLevel(INFO)
    logger.addHandler(ch)

    return logger


def read_cfg(cfg_path: str) -> dict:
    """Read configuration file

    Args:
        cfg_path (str): configuration path

    Returns:
        dict: configuration
    """
    with open(cfg_path, "r") as fid:
        cfg = yaml_load(fid)

    return cfg


def read_simulation_info(simulation_path: str) -> dict:
    """Read simulation information

    Args:
        simulation_path (str): Simulation configuration path

    Returns:
        dict: simulation info
    """
    cfg = read_cfg(simulation_path)

    return {
        "initial_day": cfg["time"]["initial_day"],
        "seed_cases_per_capita": cfg["seed"]["cases_per_capita"],
    }


def check_data_availability(data_cfg: dict):
    """Get the availablity of the input data

    Args:
        data_cfg (dict): Data configuration
    """

    def _extract_values(d):
        """
        A recursive function to extract all
        the values from a nested dictionary.
        """
        values = []
        for k, v in d.items():
            if k == "base_dir":
                continue

            if isinstance(v, dict):
                values.extend(_extract_values(v))
            else:
                values.append(v)
        return values

    paths = _extract_values(data_cfg)

    for proc_path in paths:
        proc_path = join(data_cfg["base_dir"], proc_path)
        if not exists(proc_path):
            raise Exception(f"{proc_path} does not exist ....")
