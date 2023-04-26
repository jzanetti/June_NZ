"""
Usage: cli_june --workdir /tmp/june_nz --cfg june.cfg
Author: Sijin Zhang
Description: 
    This is a wrapper to run the JUNE model


export PYTHONPATH=/Users/sijinzhang/Github/June_NZ

"""

import argparse
from os.path import exists
from os import makedirs
from process.utils import setup_logging, read_cfg
from process.june_model import check_availability_for_june_model
from process.geography import create_geography


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


def run_june():
    args = setup_parser()

    if not exists(args.workdir):
        makedirs(args.workdir)

    logger = setup_logging(args.workdir)

    logger.info("Checking out the JUNE model ...")
    check_availability_for_june_model(checkout_repo = False)

    logger.info("Reading configuration ...")
    cfg = read_cfg(args.cfg)

    logger.info("Creating geography object ...")
    geography_object = create_geography(
        cfg["input"]["base_input"], 
        cfg["input"]["population"]["geography"])


if __name__ == "__main__":
    run_june()