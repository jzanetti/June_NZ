from june.geography import Geography
from june.geography.geography import Geography as Geography_class
import pandas
from os.path import join
from pandas import DataFrame

def create_geography(base_input: str, geography_cfg: dict) -> dict:
    """Create geography object

    Args:
        base_input (str): base input as directory
        geography_cfg (dict): geography configuration

    Returns:
        dict: the dict contains the geography object
    """
    geography = Geography.from_file(
        hierarchy_filename=join(base_input, geography_cfg["geography_hierarchy"]),
        super_area_coordinates_filename=join(base_input, geography_cfg["super_area_location"]),
        area_coordinates_filename=join(base_input, geography_cfg["area_location"]),
        area_socioeconomic_index_filename=join(base_input, geography_cfg["area_socialeconomic_index"])
    )

    geography_df = geography2df(geography)

    return {
        "data": geography,
        "df": geography_df
    }


def geography2df(geography: Geography_class) -> DataFrame:
    """Convert geography to DataFrame

    Args:
        geography (Geography_class): calculated geography

    Returns:
        DataFrame: geography Dataframe
    """


    all_regions = geography.regions

    geography_info = {
        "region_name": [],
        "super_area_name": [],
        "area_name": [],
        "socialeconomic_index": [],
        "super_area_coords": [],
        "area_coords": []
    }

    for proc_region in all_regions.members:

        proc_region_name = proc_region.name

        all_super_areas = proc_region.super_areas

        for proc_super_area in all_super_areas:

            proc_super_area_coords = proc_super_area.coordinates

            proc_super_area_name = proc_super_area.name

            all_areas = proc_super_area.areas

            for proc_area in all_areas:

                proc_area_socialeconomic_index = proc_area.socioeconomic_index
                proc_area_coordinates = proc_area.coordinates
                proc_area_name = proc_area.name

                geography_info["region_name"].append(proc_region_name)
                geography_info["super_area_name"].append(proc_super_area_name)
                geography_info["area_name"].append(proc_area_name)
                geography_info["socialeconomic_index"].append(proc_area_socialeconomic_index)
                geography_info["super_area_coords"].append(proc_super_area_coords)
                geography_info["area_coords"].append(proc_area_coordinates)
    

    return DataFrame.from_dict(geography_info)