from datetime import datetime
from logging import getLogger
from os import makedirs
from os.path import exists, join

from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.pyplot import (
    close,
    legend,
    savefig,
    tight_layout,
    title,
    xlabel,
    ylabel,
)
from pandas import DataFrame, DateOffset

logger = getLogger()


def plot_activities(workdir: str, df_people: DataFrame, max_plot_days: int = 7):
    """Plot daily activities

    Args:
        workdir (str): _description_
        df_people (DataFrame): _description_
    """
    fig_dir = join(workdir, "activities")

    if not exists(fig_dir):
        makedirs(fig_dir)

    activity_df = df_people[["time", "subgroup_or_activity"]]

    start_date = activity_df["time"].min()
    end_date = start_date + DateOffset(days=max_plot_days)
    activity_df = activity_df[
        (activity_df["time"] >= start_date) & (activity_df["time"] <= end_date)
    ]

    activity_counts = (
        activity_df.groupby(["time", "subgroup_or_activity"]).size().unstack(fill_value=0)
    )
    try:
        activity_counts = activity_counts.drop("", axis=1)
    except KeyError:
        pass
    activity_percentages = activity_counts.apply(lambda x: x / x.sum(), axis=1) * 100.0

    ax = activity_percentages.plot(kind="bar", stacked=True, figsize=(10, 6))
    ax.xaxis.set_major_locator(AutoDateLocator(interval_multiples=1))
    xlabel("Time")
    ylabel("Percentage")
    title("Percentage of Activities at Different Times")
    legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
    tight_layout()
    savefig(join(fig_dir, "activities.png"), bbox_inches="tight")
    close()
