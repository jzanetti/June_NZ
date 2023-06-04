from logging import getLogger
from os import makedirs
from os.path import exists, join
from pickle import dump as pickle_dump

import matplotlib.pyplot as plt
from pandas import DataFrame, concat

from process.diags import get_people_for_groups_df, world_person2df

logger = getLogger()


def output_postprocess(workdir: str, simulation_output: list, write_csv: bool = True) -> DataFrame:
    """Write output (world object) to a csv

    Args:
        workdir (str): Working directory
        simulation_output (list): A list of simulation outputs
        write_csv (bool): Write output to a CSV
    """
    output_people = []
    output_groups = []
    for proc_simulation in simulation_output:
        proc_simulation_time = list(proc_simulation.keys())[0]

        logger.info(f"Output_postprocess: processing {proc_simulation_time} ...")

        # print(proc_simulation[proc_simulation_time].companies.group_subgroups_size)
        output_people.append(
            world_person2df(proc_simulation[proc_simulation_time], time=proc_simulation_time)
        )

        output_groups.append(
            get_people_for_groups_df(
                proc_simulation[proc_simulation_time], time=proc_simulation_time
            )
        )

    output_people = concat(output_people)
    output_groups = concat(output_groups)

    if write_csv:
        output_people.to_csv(join(workdir, "output_people.csv"))
        output_groups.to_csv(join(workdir, "output_groups.csv"))

    output = {"output_people": output_people, "output_groups": output_groups}

    pickle_dump(output, open(join(workdir, "output.pickle"), "wb"))

    return output


def output_to_figure(workdir: str, output: dict, output_cfg: dict):
    """Convert output dataframe to figures

    Args:
        workdir (str): Working directory
        output (DataFrame): Processed output
    """
    fig_dir = join(workdir, "fig")
    if not exists(fig_dir):
        makedirs(fig_dir)

    df_people = output["output_people"]
    df_group = output["output_groups"]

    df_people["home_super_area"] = df_people["home_super_area"].astype(str)
    df_people["work_super_area"] = df_people["work_super_area"].astype(str)

    if output_cfg["demography"]:
        for proc_area in df_people.area_name.unique():
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
            proc_area_data = proc_area_data[proc_area_data["time"] == min(proc_area_data["time"])]

            proc_area_data.fillna("", inplace=True)
            proc_area_data["work_to_home"] = proc_area_data[
                ["work_super_area", "home_super_area"]
            ].agg("-".join, axis=1)
            proc_area_data = proc_area_data.drop(
                columns=["work_super_area", "home_super_area", "time"]
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
        for proc_area in df_people.area_name.unique():
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
