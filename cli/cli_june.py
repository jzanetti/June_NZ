"""
Usage: cli_june --workdir /tmp/june_nz --cfg june.cfg
Author: Sijin Zhang
Contact: sijin.zhang@esr.cri.nz

Description: 
    This is a wrapper to run the JUNE model
"""
from process.june_model import (
    check_availability_for_june_model,
    create_pseudo_data_folder,
)

check_availability_for_june_model(checkout_repo=False)
create_pseudo_data_folder()

import argparse
import sys
from os import makedirs
from os.path import exists

from process.commute import create_commute_wrapper
from process.disease import create_disease_wrapper
from process.geography import create_geography_wrapper
from process.interaction import create_interaction_wrapper, initiate_interaction
from process.policy import create_policy_wrapper
from process.simulation import start_simulation
from process.tracker import create_tracker_wrapper
from process.tuning import tuning_wrapper
from process.utils import check_data_availability, read_cfg, setup_logging
from process.world import create_world_wrapper

sys.setrecursionlimit(999999)


def get_example_usage():
    example_text = """example:
        * cli_june --workdir /tmp/june_nz
                    --cfg june.cfg
        """
    return example_text


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Run JUNE model for New Zealand",
        epilog=get_example_usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--workdir", required=True, help="Working directory, e.g., where the output will be stored"
    )
    parser.add_argument(
        "--cfg", required=True, help="Configuration path for the model, e.g., june.cfg"
    )

    parser.add_argument(
        "--tuning_cfg",
        required=False,
        default=None,
        help="Model tuning configuration, e.g., june_tune.cfg",
    )

    return parser.parse_args(
        [
            "--workdir",
            "/tmp/june_realworld_auckland_exp3",
            "--cfg",
            "etc/cfg/run/june_auckland_exp3.yml",
            "--tuning_cfg",
            "etc/cfg/tuning/tuning.yml",
        ]
        # [
        #    "--workdir", "/tmp/june_realworld_2023_0615_6", "--cfg", "etc/cfg/run/june_nz2.yml"
        # ]
        # [
        #    "--workdir",
        #    "/tmp/june_singleobs_tuning_test",
        #    "--cfg",
        #    "etc/cfg/run/june_singleobs_v2.0_tuning.yml",
        #    "--tuning_cfg",
        #    "etc/cfg/tuning/tuning.yml",
        # ]
    )


def main():
    """Run June model for New Zealand"""
    args = setup_parser()

    if not exists(args.workdir):
        makedirs(args.workdir)

    logger = setup_logging(args.workdir)

    logger.info("Reading configuration ...")
    cfg = read_cfg(args.cfg)

    logger.info("Checking data availability ...")
    check_data_availability(cfg["data"])

    logger.info("Tuning the model ...")
    tuning_wrapper(cfg["data"], args.tuning_cfg)

    logger.info("Creating geography object ...")
    geography_object = create_geography_wrapper(
        cfg["data"]["base_dir"], cfg["data"]["geography"], save_df=cfg["save"]["geography"]
    )

    logger.info("Initiating the interaction ...")
    initiate_interaction(cfg["data"]["base_dir"], cfg["data"]["group_and_interaction"])

    logger.info("Creating the world object ...")

    world = create_world_wrapper(
        geography_object,
        cfg["data"]["base_dir"],
        cfg["data"]["demography"],
        cfg["data"]["geography"],
        cfg["data"]["group_and_interaction"],
        cfg["data"]["disease"],
        cfg["simulation_cfg"],
        args.workdir,
        save_df=True,
    )

    logger.info("Creating commuting object ...")
    commute = create_commute_wrapper(
        world["data"],
        cfg["data"]["base_dir"],
        cfg["data"]["group_and_interaction"]["commute"],
        cfg["data"]["geography"]["super_area_name"],
        args.workdir,
        save_df=cfg["save"]["world"],
    )

    logger.info("Creating disease object ...")
    disease = create_disease_wrapper(
        world["data"],
        cfg["data"]["base_dir"],
        cfg["data"]["disease"],
        cfg["simulation_cfg"],
        apply_vaccine=False,
    )

    logger.info("Creating interaction object ...")
    interaction = create_interaction_wrapper(
        cfg["data"]["base_dir"], cfg["data"]["group_and_interaction"], args.workdir
    )

    logger.info("Creating policy object ...")
    policy = create_policy_wrapper(cfg["data"]["base_dir"], cfg["data"]["policy"])

    logger.info("Creating tracker ...")
    tracker = create_tracker_wrapper(
        args.workdir,
        world["data"],
        list(cfg["data"]["group_and_interaction"].keys()),
        interaction["path"],
    )

    logger.info("Starting simulation ...")

    start_simulation(
        world["data"],
        disease_obj=disease,
        interaction_obj=interaction["data"],
        travel_obj=commute,
        policy_obj=policy,
        tracker_obj=tracker,
        simulation_cfg=cfg["simulation_cfg"],
        disease_cfg=cfg["data"]["disease"],
        base_dir=cfg["data"]["base_dir"],
        workdir=args.workdir,
        save_debug=True,
    )

    logger.info("Job done ...")


if __name__ == "__main__":
    main()
