from pandas import concat
from process.diags import world_person2df
from os.path import join, exists
from pandas import DataFrame
from os import makedirs
import matplotlib.pyplot as plt

def output2csv(workdir: str, simulation_output: list) -> DataFrame:
    """Write output (world object) to a csv

    Args:
        workdir (str): Working directory
        simulation_output (list): A list of simulation outputs
    """
    output = []
    for proc_simulation in simulation_output:
        proc_simulation_time = list(proc_simulation.keys())[0]
        output.append(
            world_person2df(
                proc_simulation[proc_simulation_time], 
                time=proc_simulation_time)
            )

    df = concat(output)
    
    df.to_csv(join(
        workdir,
        "output.csv"
    ))

    return df



def output2figure(workdir: str, df: DataFrame):
    """Convert output dataframe to figures

    Args:
        workdir (str): Working directory
        df (DataFrame): Dataframe output
    """
    fig_dir = join(workdir, "fig")
    if not exists(fig_dir):
        makedirs(fig_dir)

    # plot demography
    for proc_area in df.area_name.unique():
        proc_area_data = df.loc[df["area_name"] == proc_area][
            ["sex", "age", "ethnicity", "comorbidity", "work_sector", "work_super_area", "home_super_area"]]
        proc_area_data.fillna("",inplace=True)
        proc_area_data['work_to_home'] = proc_area_data[['work_super_area', 'home_super_area']].agg('-'.join, axis=1)
        proc_area_data = proc_area_data.drop(columns=["work_super_area", "home_super_area"])
        data = proc_area_data.apply(proc_area_data.value_counts)
        data.plot(kind="pie", subplots=True, layout=(2,3),figsize=(15, 9), title=f"Area: {proc_area}")
        plt.savefig(join(fig_dir, f"{proc_area}_demography.png"), bbox_inches = "tight")
        plt.close()

    # plot infection
    for proc_area in df.area_name.unique():
        proc_area_data = df.loc[df["area_name"] == proc_area][
            ["time", "infection", "dead"]]
        proc_area_data["infection"].fillna("Not infected",inplace=True)
        proc_area_data.loc[proc_area_data['dead'] == True, "infection"] = "dead"
        proc_area_data = proc_area_data.drop(columns=["dead"])
        grouped = proc_area_data.groupby(["time", "infection"]).size().reset_index(name="count")
        pivoted = grouped.pivot(index="time", columns="infection", values="count")
        probabilities = pivoted.div(pivoted.sum(axis=1), axis=0)
        probabilities.fillna(0.0,inplace=True)
        probabilities.plot(kind="line",figsize=(14, 7), title=f"Area: {proc_area}")
        plt.savefig(join(fig_dir, f"{proc_area}_infection.png"), bbox_inches = "tight")
        plt.close()



