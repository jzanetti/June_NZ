from glob import glob
from logging import getLogger

from pandas import concat, read_parquet

logger = getLogger()


def combine_outputs(workdir: str, max_files: int or None = None) -> dict:
    """Combine outputs to a dict

    Args:
        workdir (str): Working directory

    Returns:
        dict: June-NZ output in a dict
    """

    all_files = glob(workdir + "/world*.parquet")

    logger.info(f"Reading files: {len(all_files)}")

    if max_files is not None:
        all_files = all_files[:max_files]

    all_data = []
    for i, proc_file in enumerate(all_files):
        completed_ratio = round((i / len(all_files)) * 100.0, 2)
        logger.info(f"    - completed: {completed_ratio}%")
        all_data.append(read_parquet(proc_file))

    logger.info(f"Concat files")
    all_data = concat(all_data)

    logger.info("Done reading ...")
    return all_data
