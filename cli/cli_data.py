"""
Usage: cli_data --workdir /tmp/june_nz --cfg june.cfg
Author: Sijin Zhang
Description: 
    This is a wrapper to obtain data for runnig JUNE
"""
import argparse
from os import makedirs
from os.path import exists

from process.data import write_geography_hierarchy_definition, write_super_area_location
from process.utils import read_cfg, setup_logging


def get_example_usage():
    example_text = """example:
        * cli_june --workdir /tmp/june_nz
                    --cfg june.cfg
        """
    return example_text


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Creating data for JUNE model for NZ",
        epilog=get_example_usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--workdir", required=True, help="working directory")
    parser.add_argument("--cfg", required=True, help="configuration path, e.g., data.cfg")

    return parser.parse_args(["--workdir", "etc/data/realworld", "--cfg", "etc/june_data.yml"])


def main():
    """Getting data for running JUNE"""
    args = setup_parser()

    if not exists(args.workdir):
        makedirs(args.workdir)

    logger = setup_logging(args.workdir)

    logger.info("Reading configuration ...")
    cfg = read_cfg(args.cfg)

    logger.info("Processing geography_hierarchy_definition ...")
    write_geography_hierarchy_definition(
        args.workdir, cfg["geography"]["geography_hierarchy_definition"]
    )

    logger.info("Processing super area location ...")
    write_super_area_location(args.workdir, cfg["geography"]["super_area_location"])

    logger.info("Job done ...")


if __name__ == "__main__":
    main()
