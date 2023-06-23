from datetime import datetime
from logging import getLogger

from pandas import DataFrame

from process.diags.activities import plot_activities
from process.diags.demography import plot_demography
from process.diags.equity import plot_equity_again_symptoms
from process.diags.timeseries import plot_timeseries
from process.diags.utils import get_geo_table

logger = getLogger()


def diags_wrapper(workdir: str, df_people: DataFrame, diags_cfg: dict):
    """Creating diags data

    Args:
        workdir (str): Working directory
        june_output_path (str): June-NZ output path
        diags_cfg (dict): Diags configuration
    """
    logger.info("Loading June-NZ outputs ...")

    logger.info("Loading Geo table ...")
    geotable = get_geo_table(diags_cfg["geo_table"], workdir)

    min_time = min(df_people["time"])

    if diags_cfg["activity"]:
        plot_activities(workdir, df_people, max_plot_days=3)

    for area_type in ["super_area", "area"]:
        if area_type == "area":
            areas_or_super_areas = list(df_people.area_name.unique())
        elif area_type == "super_area":
            areas_or_super_areas = list(df_people.super_area_name.unique())

        if diags_cfg["equity"][area_type]:
            plot_equity_again_symptoms(
                workdir,
                df_people,
                areas_or_super_areas,
                area_type,
                geotable=geotable,
            )

        if diags_cfg["demography"][area_type]:
            plot_demography(
                workdir,
                df_people,
                min_time,
                areas_or_super_areas,
                area_type,
                geotable=geotable,
            )

        if diags_cfg["infection"]["timeseries"][area_type]:
            plot_timeseries(
                workdir,
                df_people,
                min_time,
                areas_or_super_areas,
                area_type,
                geotable=geotable,
                add_no_infected=diags_cfg["infection"]["add_no_infected"],
            )
