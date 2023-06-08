from datetime import datetime
from logging import getLogger
from os import makedirs
from os.path import exists, join

import matplotlib.gridspec as gridspec
from matplotlib.pyplot import close, figure, savefig, suptitle, tight_layout
from pandas import DataFrame
from pandas import cut as pandas_cut

from process import REGION_NAMES_CONVERSIONS
from process.diags.utils import get_area_name

logger = getLogger()


def plot_demography(
    workdir: str,
    df_people: DataFrame,
    min_time: datetime,
    areas_or_super_areas: list,
    area_type: str,  # super_area or area
    geotable: DataFrame or None = None,
):
    """Plot demography at either the SA2 or regional level

    Args:
        workdir (str): Working directory
        df_people (DataFrame): JUNE output at the people level
        min_time (datetime): The simulation start time
        all_areas (list): All areas to be plotted
        area_type (list): Either area or super area
        geotable (DataFrame or None): Geo table to be used
    """

    fig_dir = join(workdir, "demography", area_type)

    if not exists(fig_dir):
        makedirs(fig_dir)

    for i, proc_area in enumerate(areas_or_super_areas):
        logger.info(
            f"Creating vis (demography): {proc_area} ... ({round(100.0 * (float(i)/float(len(areas_or_super_areas))), 2)}%)"
        )
        proc_area_data = df_people.loc[df_people[f"{area_type}_name"] == proc_area][
            [
                "sex",
                "age",
                "ethnicity",
                "comorbidity",
                "work_sector",
                "work_super_area",
                "home_super_area",
                "time",
            ]
        ]
        proc_area_data = proc_area_data[proc_area_data["time"] == min_time]
        proc_area_data["work_super_area"] = proc_area_data["work_super_area"].map(
            REGION_NAMES_CONVERSIONS
        )
        proc_area_data["home_super_area"] = proc_area_data["home_super_area"].map(
            REGION_NAMES_CONVERSIONS
        )
        proc_area_data.fillna("", inplace=True)

        proc_area_data["work_to_home"] = proc_area_data[
            ["work_super_area", "home_super_area"]
        ].agg("-".join, axis=1)

        proc_area_data["work_to_home"] = proc_area_data["work_to_home"].apply(
            lambda x: "others/unemployed" if str(x).startswith("-") else x
        )

        proc_area_data = proc_area_data.drop(
            columns=["work_super_area", "home_super_area", "time"]
        )

        proc_area_data["work_sector"] = proc_area_data["work_sector"].replace(
            "", "others/unemployed"
        )

        age_bins = [0, 6, 18, 65, 100]  # Define the bin edges
        age_labels = [6, 18, 65, 100]  # Define the labels for each bin

        proc_area_data["age"] = pandas_cut(
            proc_area_data["age"], bins=age_bins, labels=age_labels, right=False
        )

        data = proc_area_data.apply(proc_area_data.value_counts)

        fig = figure(figsize=(9, 15))
        gs = gridspec.GridSpec(4, 2, figure=fig)

        # Plot the first 4 subplots with a layout of (2, 2)
        plot_layout = {
            "sex": gs[0, 0],
            "age": gs[0, 1],
            "ethnicity": gs[1, 0],
            "comorbidity": gs[1, 1],
            "work_sector": gs[2, :],
            "work_to_home": gs[3, :],
        }

        for plot_name in plot_layout:
            ax = fig.add_subplot(plot_layout[plot_name])
            data.plot(y=plot_name, subplots=True, ax=ax, kind="pie", legend=False, ylabel="")
            ax.set_title(plot_name)

        area_name = get_area_name(area_type, proc_area, geotable=geotable)

        suptitle(f"Demography for {proc_area} ({area_name})) \n {len(proc_area_data)} individuals")
        tight_layout()
        savefig(join(fig_dir, f"{proc_area}_demography.png"), bbox_inches="tight")
        close()
