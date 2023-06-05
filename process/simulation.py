from copy import deepcopy
from os.path import join

from june.epidemiology.epidemiology import Epidemiology as Epidemiology_class
from june.groups.travel.travel import Travel as Travel_class
from june.interaction.interaction import Interaction as Interaction_class
from june.policy.policy import Policies as Policies_class
from june.records import Record
from june.simulator import Simulator
from june.tracker.tracker import Tracker as Tracker_class
from june.world import World as World_class


def start_simulation(
    world: World_class,
    disease_obj: Epidemiology_class = None,
    interaction_obj: Interaction_class = None,
    travel_obj: Travel_class = None,
    policy_obj: Policies_class = None,
    tracker_obj: Tracker_class = None,
    simulation_cfg: dict = None,
    disease_cfg: dict = None,
    base_dir: str = None,
    workdir: str = None,
    save_timestep: bool = False,
):
    """Start running the simulation

    Args:
        world (World_class): The world object
        disease_obj (Epidemiology_class, optional): Disease/epidemiology object. Defaults to None.
        interaction_obj (Interaction_class, optional): Interaction object. Defaults to None.
        travel_obj (Travel_class, optional): Travel/commute object. Defaults to None.
        policy_obj (Policies_class, optional): Policy object. Defaults to None.
        tracker_obj (Tracker_class, optional): Track object. Defaults to None.
        simulation_cfg (dict, optional): Simulation configuration. Defaults to None.
        disease_cfg (dict, optional): Disease configuration. Defaults to None.
        base_dir (str): Base directory
        workdir (str, optional): Working directory. Defaults to None.
    """
    simulator = Simulator.from_file(
        world=world,
        epidemiology=disease_obj,
        interaction=interaction_obj,
        config_filename=simulation_cfg,
        trajectory_filename=join(base_dir, disease_cfg["sympton_trajectories"]),
        travel=travel_obj,
        record=Record(
            record_path=join(workdir, "output"),
            record_static_data=True,
        ),
        policies=policy_obj,
        tracker=tracker_obj,
    )

    return simulator.run(save_timestep=save_timestep)
