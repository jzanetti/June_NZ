
from os.path import join, exists
from logging import INFO, Formatter, StreamHandler, basicConfig, getLogger
from datetime import datetime
from yaml import safe_load as yaml_load

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
        "seed_cases_per_capita": cfg["seed"]["cases_per_capita"]
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


