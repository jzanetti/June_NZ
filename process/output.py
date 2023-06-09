from glob import glob
from logging import getLogger

from pandas import concat, read_parquet

logger = getLogger()


def combine_outputs(workdir: str) -> dict:
    """Combine outputs to a dict

    Args:
        workdir (str): Working directory

    Returns:
        dict: June-NZ output in a dict
    """

    all_files = glob(workdir + "/world*.parquet")

    all_data = []
    for proc_file in all_files:
        all_data.append(read_parquet(proc_file))

    all_data = concat(all_data)

    return all_data
