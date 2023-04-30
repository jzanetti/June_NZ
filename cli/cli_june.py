"""
Usage: cli_june --workdir /tmp/june_nz --cfg june.cfg
Author: Sijin Zhang
Description: 
    This is a wrapper to run the JUNE model


export PYTHONPATH=/Users/sijinzhang/Github/June_NZ

"""
from process.june_model import (check_availability_for_june_model, 
                                create_pseudo_data_folder)
check_availability_for_june_model(checkout_repo = False)
create_pseudo_data_folder()

import argparse
from os.path import exists
from os import makedirs
from process.utils import setup_logging, read_cfg
from process.geography import create_geography_wrapper
from process.interaction import initiate_interaction, create_interaction_wrapper
from process.world import create_world_wrapper
from process.commute import create_commute_wrapper
from process.disease import create_disease_wrapper
from process.tracker import create_tracker_wrapper
from process.policy import create_policy_wrapper
from process.simulation import start_simulation
from process.output import output2csv, output2figure

def get_example_usage():
    example_text = """example:
        * cli_june --workdir /tmp/june_nz
                    --cfg june.cfg
        """
    return example_text


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Run JUNE model for NZ",
        epilog=get_example_usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--workdir", required=True, help="working directory")
    parser.add_argument("--cfg", required=True, help="configuration path, e.g., june.cfg")

    return parser.parse_args(
        [
            "--workdir", "/tmp/june_nz",
            "--cfg", "etc/june_singleobs.yml"
        ]
    )


def main():
    """Run June model
    """
    args = setup_parser()

    if not exists(args.workdir):
        makedirs(args.workdir)

    logger = setup_logging(args.workdir)

    logger.info("Reading configuration ...")
    cfg = read_cfg(args.cfg)

    logger.info("Creating geography object ...")
    geography_object = create_geography_wrapper(
        cfg["input"]["base_input"], 
        cfg["input"]["population"]["geography"])

    logger.info("Initiating the interaction ...")
    initiate_interaction(
        cfg["input"]["base_input"], 
        cfg["input"]["interaction"])

    logger.info("Creating the world object ...")
    world = create_world_wrapper(
        geography_object, 
        cfg["input"]["base_input"],
        cfg["input"]["population"],
        cfg["input"]["distribution"],
        cfg["input"]["interaction"],
        args.workdir)

    logger.info("Creating commuting object ...")
    commute = create_commute_wrapper(
        world["data"],
        cfg["input"]["base_input"], 
        cfg["input"]["interaction"]["commute"], 
        args.workdir)

    logger.info("Creating disease object ...")
    disease = create_disease_wrapper(
        world["data"], 
        cfg["input"]["base_input"], 
        cfg["input"]["disease"])

    logger.info("Creating interaction object ...")
    interaction = create_interaction_wrapper(
        cfg["input"]["base_input"], 
        cfg["input"]["interaction"], 
        args.workdir)

    logger.info("Creating policy object ...")
    policy = create_policy_wrapper(cfg["input"]["base_input"], cfg["input"]["policy"],)

    logger.info("Creating tracker ...")
    tracker = create_tracker_wrapper(
        args.workdir,
        world["data"], 
        list(cfg["input"]["interaction"].keys()),
        interaction["path"]
    )

    logger.info("Starting simulation ...")
    output = start_simulation(
        world["data"],
        disease_obj = disease,
        interaction_obj = interaction["data"],
        travel_obj = commute,
        policy_obj = policy,
        tracker_obj = tracker,
        simulation_cfg = cfg["input"]["simulation"],
        disease_cfg = cfg["input"]["disease"],
        base_dir = cfg["input"]["base_input"],
        workdir = args.workdir
    )

    df = output2csv(args.workdir, output)

    output2figure(args.workdir, df)

    logger.info("Job done ...")


if __name__ == "__main__":
    main()