"""
Usage: cli_diags --workdir /tmp/june_nz --cfg june_diags.cfg
Author: Sijin Zhang
Description: 
    This is a wrapper to plot the JUNE_NZ outputs
"""
import argparse
from os import makedirs
from os.path import exists

from process.diags.wrapper import diags_wrapper
from process.output import combine_outputs

# from process.output import output_to_figure
from process.utils import read_cfg, setup_logging


def get_example_usage():
    example_text = """example:
        * cli_diags --workdir /tmp/june_nz_diags
                    --output /tmp/june_nz2/output.pickle
                    --cfg june_diags.cfg
        """
    return example_text


def setup_parser():
    parser = argparse.ArgumentParser(
        description="Creating plots for JUNE model for NZ",
        epilog=get_example_usage(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--workdir", required=True, help="working directory")
    parser.add_argument("--june_data_dir", required=True, help="JUNE_NZ output data directory")
    parser.add_argument("--cfg", required=True, help="configuration path, e.g., diags.cfg")

    return parser.parse_args(
        [
            "--workdir",
            "/tmp/june_realworld_test2_diags",
            "--june_data_dir",
            "/tmp/june_realworld_test2/output",
            "--cfg",
            "etc/cfg/run/june_diags.yml",
        ]
    )


def main():
    """Getting visualization for JUNE"""
    args = setup_parser()

    if not exists(args.workdir):
        makedirs(args.workdir)

    logger = setup_logging(args.workdir)

    logger.info("Reading configuration ...")
    cfg = read_cfg(args.cfg)

    output = combine_outputs(args.june_data_dir)

    diags_wrapper(args.workdir, output, cfg)

    logger.info("Job done ...")


if __name__ == "__main__":
    main()
