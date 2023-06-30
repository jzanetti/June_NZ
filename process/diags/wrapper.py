from datetime import datetime
from logging import getLogger

from pandas import DataFrame

from process.diags.activities import plot_activities
from process.diags.demography import plot_demography
from process.diags.equity import plot_equity_again_symptoms
from process.diags.map import plot_infected_map
from process.diags.timeseries import plot_timeseries
from process.diags.utils import contains_true, get_geo_table, get_shp

logger = getLogger()


def diags_wrapper(workdir: str, df_people: DataFrame, diags_cfg: dict):
    """Creating diags data

    Args:
        workdir (str): Working directory
        june_output_path (str): June-NZ output path
        diags_cfg (dict): Diags configuration
    """
    logger.info("Loading June-NZ outputs ...")

    logger.info("Loading SA3 shapefile ...")

    geotable = get_geo_table(diags_cfg["geo_table"], workdir)

    if contains_true(diags_cfg["map"]):
        logger.info("Loading map shapefile ...")
        gdf = get_shp(diags_cfg["sa3_shp"], workdir)

    if diags_cfg["activity"]:
        plot_activities(workdir, df_people, max_plot_days=3)

    for area_type in ["super_area", "area"]:
        if area_type == "area":
            if diags_cfg["domains"]["area"] is None:
                areas_or_super_areas = list(df_people.area_name.unique())
            else:
                areas_or_super_areas = diags_cfg["domains"]["area"]

        elif area_type == "super_area":
            if diags_cfg["domains"]["super_area"] is None:
                areas_or_super_areas = list(df_people.super_area_name.unique())
            else:
                areas_or_super_areas = diags_cfg["domains"]["super_area"]

        min_time = df_people["time"].min()

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
                diags_cfg["infection"]["features"],
                geotable=geotable,
            )

    if diags_cfg["map"]["infected"]:
        infected_map = df_people[["time", "super_area_name", "infected"]]
        infected_counts = (
            infected_map.groupby(["super_area_name", "time"])["infected"].sum().reset_index()
        )
        logger.info("Plot infected counts ...")
        plot_infected_map(workdir, gdf, infected_counts, geotable, diags_cfg["domains"]["region"])
