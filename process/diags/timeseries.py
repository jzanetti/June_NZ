from datetime import datetime
from logging import getLogger
from os import makedirs
from os.path import exists, join

from matplotlib.pyplot import close, savefig, subplots, suptitle, tight_layout, ylim
from pandas import DataFrame

from process.diags.utils import get_area_name

logger = getLogger()


def plot_timeseries(
    workdir: str,
    df_people: DataFrame,
    min_time: datetime,
    areas_or_super_areas: list,
    area_type: str,  # super_area or area
    ts_features: dict,
    geotable: DataFrame or None = None,
    if_plot_log: bool = False,
):
    fig_dir = join(workdir, "infection", area_type)

    if not exists(fig_dir):
        makedirs(fig_dir)

    for i, proc_area in enumerate(areas_or_super_areas):
        logger.info(
            f"Creating vis (infection): {proc_area} ... ({round(100.0 * (float(i)/float(len(areas_or_super_areas))), 2)}%)"
        )
        proc_area_data = df_people.loc[df_people[f"{area_type}_name"] == proc_area][
            ["time", "infection", "dead"]
        ]

        proc_area_data_first = proc_area_data[proc_area_data["time"] == min_time]

        total_people = len(proc_area_data_first)

        proc_area_data["infection"].fillna("Recovered/Not infected", inplace=True)
        proc_area_data.loc[proc_area_data["dead"] == True, "infection"] = "dead"
        proc_area_data = proc_area_data.drop(columns=["dead"])
        grouped = proc_area_data.groupby(["time", "infection"]).size().reset_index(name="count")
        pivoted = grouped.pivot(index="time", columns="infection", values="count")
        probabilities = pivoted.div(pivoted.sum(axis=1), axis=0)

        probabilities = probabilities.applymap(lambda x: round(x * 100.0, 2))

        probabilities.fillna(0.0, inplace=True)

        area_name = get_area_name(area_type, proc_area, geotable=geotable)

        if if_plot_log:
            _, axes = subplots(nrows=2, ncols=1, figsize=(12, 12))
        else:
            _, axe = subplots(nrows=1, ncols=1, figsize=(12, 10))
            axes = [axe]

        for feature_key in ts_features:
            if not ts_features[feature_key]:
                probabilities = probabilities.drop(feature_key, axis=1)

        # if not add_no_infected:
        #    probabilities = probabilities.drop("Recovered/Not infected", axis=1)

        try:
            ax = probabilities.plot(
                ax=axes[0],
                kind="line",
                # figsize=(14, 7),
                title=False,
                # title=f"Area: {proc_area} ({area_name}) \n {total_people} individuals",
                ylabel="Probability of symptom stages",
                xlabel="Simulation time",
                logy=False,
            )
            ax.set_ylim(0, probabilities.values.max() * 1.5)

            if if_plot_log:
                probabilities.plot(
                    ax=axes[1],
                    kind="line",
                    # figsize=(14, 7),
                    title=False,
                    # title=f"Area: {proc_area} ({area_name}) \n {total_people} individuals",
                    ylabel="Probability of symptom stages (log)",
                    xlabel="Simulation time",
                    logy=True,
                )
        except TypeError:
            logger.info("No infection at all for this area")

        suptitle(f"Area: {proc_area} ({area_name}) \n {total_people} individuals")
        tight_layout()
        savefig(join(fig_dir, f"{proc_area}_infection.png"), bbox_inches="tight")
        close()
