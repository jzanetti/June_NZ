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
from process.interaction import create_interaction_wrapper
from process.demography import create_person
from process.groups import create_geography_dependant_groups
from process.world import create_world_wrapper, world2df
from process.distribution import work_and_home_distribution, household_distribution
from process.commute import create_commute_wrapper
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
    create_interaction_wrapper(
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

    logger.info("Job done ...")


if __name__ == "__main__":
    main()