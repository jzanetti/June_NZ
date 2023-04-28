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
from process.geography import create_geography
from process.interaction import init_interaction
from process.demography import create_person
from process.groups import create_groups
from process.world import create_world
from process.distribution import init_worker_distribution
from logging import RootLogger
from june.world import World as World_class

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


def world_init(logger: RootLogger, cfg: dict) -> World_class:
    """Initialiate a world object

    Args:
        logger (RootLogger): logger object
        cfg (dict): configuration

    Returns:
        World: a World object
    """
    logger.info("Creating geography object ...")
    geography_object = create_geography(
        cfg["input"]["base_input"], 
        cfg["input"]["population"]["geography"])
    
    logger.info("Initiating the interaction ...")
    init_interaction(
        cfg["input"]["base_input"], 
        cfg["input"]["group_and_interaction"])

    logger.info("Creating groups (companies, hospitals etc.)...")
    group_object = create_groups(
        geography_object["data"], 
        cfg["input"]["base_input"], 
        cfg["input"]["group_and_interaction"])
    geography_object["data"] = group_object["data"]

    logger.info("Creating demography ...")
    person = create_person(
        geography_object["data"],
        cfg["input"]["base_input"], 
        cfg["input"]["population"]["demography"]["individual"])
    
    logger.info("Creating the world ...")
    return create_world(geography_object["data"], person["data"])


def world_distribution(world, logger: RootLogger, cfg: dict):
    """Population distribution, e.g., distribute people to 
          - Workplace and home
          - Household

    Args:
        world (World): World object
        logger (RootLogger): Logger object
        cfg (dict): Configuration
    """
    logger.info("Initiating workplace and home distribution ...")
    init_worker_distribution(
        world, 
        cfg["input"]["base_input"], 
        cfg["input"]["distribution"], 
        cfg["input"]["group_and_interaction"], 
        cfg["input"]["population"])




def main():
    """Run June model
    """
    args = setup_parser()

    if not exists(args.workdir):
        makedirs(args.workdir)

    logger = setup_logging(args.workdir)

    logger.info("Checking out the JUNE model ...")

    logger.info("Reading configuration ...")
    cfg = read_cfg(args.cfg)

    logger.info("Initiating the world object ...")
    world = world_init(logger, cfg)

    logger.info("Population distribution ...")
    world_distribution(world, logger, cfg)

    logger.info("Job done ...")


if __name__ == "__main__":
    main()