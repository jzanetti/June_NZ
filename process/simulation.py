from june.records import Record
from june.simulator import Simulator
from june.world import World as World_class
from os.path import join

def start_simulation(
    world: World_class,
    disease_obj = None,
    interaction_obj = None,
    travel_obj = None,
    policy_obj = None,
    tracker_obj = None,
    simulation_cfg: dict = None,
    disease_cfg: dict = None,
    base_dir: str = None,
    workdir: str = None
    ):
    """Start running the simulation

    Args:
        world (World_class): The world object
        disease_obj (_type_, optional): Disease/epidemiology object. Defaults to None.
        interaction_obj (_type_, optional): Interaction object. Defaults to None.
        travel_obj (_type_, optional): Travel/commute object. Defaults to None.
        policy_obj (_type_, optional): Policy object. Defaults to None.
        tracker_obj (_type_, optional): Track object. Defaults to None.
        simulation_cfg (dict, optional): Simulation configuration. Defaults to None.
        disease_cfg (dict, optional): Disease configuration. Defaults to None.
        base_dir (str): Base directory
        workdir (str, optional): Working directory. Defaults to None.
    """

    simulator = Simulator.from_file(
        world=world,
        epidemiology=disease_obj,
        interaction=interaction_obj, 
        config_filename = join(base_dir, simulation_cfg),
        trajectory_filename = join(base_dir, disease_cfg["cfg"]["sympton_trajectories"]),
        travel = travel_obj,
        record = Record(    
            record_path = join(workdir, "output"),    
            record_static_data=True,
        ) ,
        policies = policy_obj,
        tracker=tracker_obj,
    )

    simulator.run()