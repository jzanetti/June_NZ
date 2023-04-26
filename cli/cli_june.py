"""
Usage: cli_train --workdir /tmp/rfm --cfg train.cfg
Author: Sijin Zhang
Description: 
    This is a wrapper to get trained model for road_fatalities_model


export PYTHONPATH=/Users/sijinzhang/Github/June_NZ

"""

import argparse
from os.path import exists
from os import makedirs
from process.utils import setup_logging
from process.june_model import check_availability_for_june_model

def get_example_usage():
    example_text = """example:
        * cli_june --workdir /tmp/june_nz
                    --cfg train.cfg
        """
    return example_text


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Run JUNE model for NZ",
        epilog=get_example_usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--workdir", required=True, help="working directory")
    parser.add_argument("--cfg", required=True, help="configuration path")

    return parser.parse_args(
        [
            "--workdir", "/tmp/june_nz",
            "--cfg", "etc/june.yml"
        ]
    )


def get_data():
    args = setup_parser()

    if not exists(args.workdir):
        makedirs(args.workdir)

    logger = setup_logging(args.workdir)

    logger.info("checkout the JUNE model ...")
    june_model_dir = check_availability_for_june_model(checkout_repo = False)

    from june import world
    print("done")


if __name__ == "__main__":
    get_data()