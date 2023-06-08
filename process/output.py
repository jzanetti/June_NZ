from logging import getLogger

# from os import makedirs
from os.path import exists, join
from pickle import dump as pickle_dump

# import matplotlib.pyplot as plt
from pandas import DataFrame, concat

from process.june2df import get_people_for_groups_df, world_person2df

# from pandas import cut as pandas_cut


logger = getLogger()


def output_postprocess(
    workdir: str,
    simulation_output: dict,
    simulation_output_timestep: dict = {},
    write_csv: bool = True,
) -> DataFrame:
    """Write output (world object) to a csv

    Args:
        workdir (str): Working directory
        simulation_output (list): A list of simulation outputs
        write_csv (bool): Write output to a CSV
    """
    output_people = []
    output_groups = []

    write_timestep = False
    if len(simulation_output_timestep) > 0:
        write_timestep = True

    for proc_simulation_time in simulation_output:
        # proc_simulation_time = list(proc_simulation.keys())[0]

        logger.info(f"Output_postprocess: processing {proc_simulation_time} ...")

        output_people.append(
            world_person2df(simulation_output[proc_simulation_time], time=proc_simulation_time)
        )

        if write_timestep:
            output_groups.append(
                get_people_for_groups_df(
                    simulation_output_timestep[proc_simulation_time], time=proc_simulation_time
                )
            )

    logger.info(f"Output_postprocess: concat output_people ...")
    output_people = concat(output_people)

    if write_timestep:
        logger.info(f"Output_postprocess: concat output_groups ...")
        output_groups = concat(output_groups)
    else:
        output_groups = None

    if write_csv:
        output_people.to_csv(join(workdir, "output_people.csv"))
        if write_timestep:
            output_groups.to_csv(join(workdir, "output_groups.csv"))

    output = {"output_people": output_people, "output_groups": output_groups}

    pickle_dump(output, open(join(workdir, "output.pickle"), "wb"))

    return output


"""
def output_to_figure(workdir: str, output: dict, output_cfg: dict):

    fig_dir = join(workdir, "fig")
    if not exists(fig_dir):
        makedirs(fig_dir)

    df_people = output["output_people"]
    df_group = output["output_groups"]

    df_people["home_super_area"] = df_people["home_super_area"].astype(str)
    df_people["work_super_area"] = df_people["work_super_area"].astype(str)

    if output_cfg["demography"] is not None:
        min_time = min(df_people["time"])
        all_areas = df_people.area_name.unique()
        all_super_areas = df_people.super_area_name.unique()

        if output_cfg["demography"]["area"]:
            for i, proc_area in enumerate(df_people.area_name.unique()):
                logger.info(
                    f"Creating vis (demography): {proc_area} ... ({round(100.0 * (float(i)/float(len(all_areas))), 2)}%)"
                )
                proc_area_data = df_people.loc[df_people["area_name"] == proc_area][
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

                proc_area_data.fillna("", inplace=True)
                proc_area_data["work_to_home"] = proc_area_data[
                    ["work_super_area", "home_super_area"]
                ].agg("-".join, axis=1)
                proc_area_data = proc_area_data.drop(
                    columns=["work_super_area", "home_super_area", "time"]
                )

                age_bins = [0, 6, 18, 65, 100]  # Define the bin edges
                age_labels = [6, 18, 65, 100]  # Define the labels for each bin

                proc_area_data["age"] = pandas_cut(
                    proc_area_data["age"], bins=age_bins, labels=age_labels, right=False
                )

                data = proc_area_data.apply(proc_area_data.value_counts)
                data.plot(
                    kind="pie",
                    subplots=True,
                    legend=False,
                    layout=(2, 3),
                    figsize=(15, 9),
                    title=f"Area: {proc_area}, Total people {len(data)}",
                )
                plt.savefig(join(fig_dir, f"{proc_area}_demography.png"), bbox_inches="tight")
                plt.close()

    if output_cfg["timeseries"]["total_people"]:
        if df_group is not None:
            logger.info(f"Creating vis (timeseries) ...")
            result = df_group.groupby(["area", "time"])["people"].sum()
            result_df = result.unstack(level="area")
            result_df["total"] = result_df.sum(axis=1)
            result_df.plot.line(legend=False)
            plt.xlabel("Time")
            plt.ylabel("Total People")
            plt.title("Total people for different areas")
            plt.savefig(join(fig_dir, f"total_people.png"), bbox_inches="tight")
            plt.close()

    if output_cfg["timeseries"]["infection"]:
        total_areas = len(df_people.area_name.unique())
        for i, proc_area in enumerate(df_people.area_name.unique()):
            logger.info(
                f"Creating vis (infection): {proc_area} ... ({round(100.0 * (float(i)/float(total_areas)), 2)}%)"
            )
            proc_area_data = df_people.loc[df_people["area_name"] == proc_area][
                ["time", "infection", "dead"]
            ]
            proc_area_data["infection"].fillna("Not infected", inplace=True)
            proc_area_data.loc[proc_area_data["dead"] == True, "infection"] = "dead"
            proc_area_data = proc_area_data.drop(columns=["dead"])
            grouped = (
                proc_area_data.groupby(["time", "infection"]).size().reset_index(name="count")
            )
            pivoted = grouped.pivot(index="time", columns="infection", values="count")
            probabilities = pivoted.div(pivoted.sum(axis=1), axis=0)
            probabilities.fillna(0.0, inplace=True)
            probabilities.plot(kind="line", figsize=(14, 7), title=f"Area: {proc_area}")
            plt.savefig(join(fig_dir, f"{proc_area}_infection.png"), bbox_inches="tight")
            plt.close()
"""
