from pickle import load as pickle_load

from pandas import DataFrame, read_csv

from process import REGION_NAMES_CONVERSIONS
from process.utils import download_file


def get_area_name(area_type: str, proc_area_code: int, geotable: DataFrame or None = None) -> str:
    """Obtain area name, e.g., Auckland

    Args:
        area_type (str): Area type, super_area or area
        proc_area_code (int): area code to be processed
        geotable (DataFrameorNone, optional): Table to convert SA2 code to its name. Defaults to None.

    Returns:
        str: area name
    """
    if area_type == "super_area":
        try:
            area_name = REGION_NAMES_CONVERSIONS[proc_area_code]
        except KeyError:
            area_name = proc_area_code

    elif area_type == "area":
        if geotable is not None:
            area_name = geotable[geotable["SA22018_code"] == proc_area_code]["SA22018_name"].values
            if len(area_name) > 0:
                area_name = area_name[0]
            else:
                area_name = "unknown"
        else:
            area_name = "unknown"

    return area_name


def load_june_output(june_output_path: str) -> DataFrame:
    """Load JUNE-NZ output in pickle

    Args:
        june_output_path (str): June output data path

    Returns:
        DataFrame: June-NZ output
    """

    return pickle_load(open(june_output_path, "rb"))


def get_geo_table(geo_table_path: str, workdir: str) -> DataFrame:
    """Get geography table, e.g., code and name

    Args:
        geo_table_path (str): geotable data path starts from https
        workdir (str): Working directory
    """
    downloaded_path = download_file(geo_table_path, workdir=workdir)

    df = read_csv(downloaded_path)

    return df[["SA22018_code", "SA22018_name", "REGC2023_name"]]
