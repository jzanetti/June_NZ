from os.path import join

from june.geography import Geography

from process.diags import geography2df


def create_geography_wrapper(base_input: str, geography_cfg: dict, save_df: bool = False) -> dict:
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
        area_socioeconomic_index_filename=join(
            base_input, geography_cfg["area_socialeconomic_index"]
        ),
    )

    if save_df:
        geography_df = geography2df(geography)
    else:
        geography_df = None

    return {"data": geography, "df": geography_df}
