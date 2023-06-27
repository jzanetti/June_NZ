from datetime import datetime
from logging import getLogger
from os import listdir, makedirs
from os.path import exists, join

import imageio
import pandas as pd
from dask import compute as dask_compute
from dask import delayed as dask_delayed
from dask.diagnostics import ProgressBar
from dask.distributed import Client
from geopandas import GeoDataFrame
from matplotlib.pyplot import close, savefig, subplots, tight_layout, title
from pandas import DataFrame

logger = getLogger()


def create_gif(png_workdir: str, filename: str or None = None, duration_sec: float = 1.0):
    # Get the list of PNG files in the directory
    png_files = [f for f in listdir(png_workdir) if f.endswith(".png")]

    # Sort the PNG files in ascending order
    png_files.sort()

    # List to store image frames
    frames = []

    # Read each PNG file and add it to the frames list
    for png_file in png_files:
        image_path = join(png_workdir, png_file)
        image = imageio.imread(image_path)
        frames.append(image)

    # Output animation file path
    if filename is not None:
        output_path = join(png_workdir, f"{filename}")
    else:
        output_path = join(png_workdir, "output.gif")

    # Save the frames as an animated GIF
    imageio.mimsave(output_path, frames, duration=duration_sec)


def plot_infected_map(
    workdir: str,
    gdf: DataFrame,
    infected_counts: DataFrame,
    geotable: DataFrame,
    regions: list or None,
):
    """Plot infected map timeseries

    Args:
        workdir (str): Working directory
        gdf (DataFrame): Base geodataframe to be used
        infected_counts (DataFrame): Infecteddata
    """

    def _plot_infected_map_time(
        proc_data: GeoDataFrame, proc_time: datetime, region: str, infected_map_dir: str
    ):
        """Plot infected map at time proc_time

        Args:
            df (GeoDataFrame): Geo dataframe to be plotted
            proc_time (datetime): time to be plotted
            region (str): region to be plotted
            infected_map_dir (str): where to store the output
        """
        total_infected_num = proc_data["infected"].sum()

        _, ax = subplots(figsize=(8, 6))

        proc_data.plot(ax=ax, column="infected", cmap="jet", legend=True, vmin=0, vmax=100)

        ax.axis("off")

        tight_layout()
        title(f'{region}, {proc_time.strftime("%Y%m%d%H")} \n Total cases: {total_infected_num}')
        savefig(
            join(
                infected_map_dir,
                f"infected_{region}_{proc_time.strftime('%Y%m%d%H')}.png",
            ),
            bbox_inches="tight",
        )
        close()

    infected_counts["super_area_name"] = infected_counts["super_area_name"].astype(str)
    geotable["SA32023_code"] = geotable["SA32023_code"].astype(str)

    merged_all = gdf.merge(infected_counts, left_on="SA32023_V1", right_on="super_area_name")

    merged_all = merged_all.merge(geotable, left_on="SA32023_V1", right_on="SA32023_code")

    if regions is None:
        regions = ["NZ"]

    # client = Client(n_workers=8)

    for region in regions:
        if region == "NZ":
            df = merged_all
        else:
            df = merged_all[merged_all["REGC2023_name"] == f"{region} Region"]

        unique_times = list(df["time"].unique())

        infected_map_dir = join(workdir, "infected_map")

        if not exists(infected_map_dir):
            makedirs(infected_map_dir)

        delayed_results = []
        for proc_time in unique_times:
            proc_data = df[df["time"] == proc_time]
            delayed_results.append(
                dask_delayed(_plot_infected_map_time)(
                    proc_data, proc_time, region, infected_map_dir
                )
            )
        ProgressBar().register()
        dask_compute(*delayed_results, scheduler="processes", num_workers=8)

        # _plot_infected_map_time(df, proc_time, region, infected_map_dir)

        logger.info("Creating GIF ...")
        create_gif(infected_map_dir, filename=f"infected_{region}.gif")
