from pandas import concat
from process.diags import world_person2df
from os.path import join

def output2csv(workdir: str, simulation_output: list):
    """Write output (world object) to a csv

    Args:
        workdir (str): Working directory
        simulation_output (list): A list of simulation outputs
    """
    output = []
    for proc_simulation in simulation_output:
        output.append(world_person2df(proc_simulation))

    concat(output).to_csv(join(
        workdir,
        "output.csv"
    ))




