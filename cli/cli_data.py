"""
Usage: cli_data --workdir /tmp/june_nz --cfg june.cfg
Author: Sijin Zhang
Description: 
    This is a wrapper to obtain data for runnig JUNE
"""
import argparse
from os import makedirs
from os.path import exists

from process.data.demography import (
    write_age_profile,
    write_commorbidity,
    write_ethnicity_profile,
    write_gender_profile_female_ratio,
)
from process.data.geography import (
    write_area_location,
    write_area_socialeconomic_index,
    write_geography_hierarchy_definition,
    write_super_area_location,
)
from process.data.group import (
    write_employees_by_super_area,
    write_household_age_difference,
    write_household_number,
    write_sectors_by_super_area,
    write_sectors_employee_genders,
    write_super_area_name,
    write_transport_mode,
    write_workplace_and_home,
)
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

    # -----------------------------
    # Get demography data
    # -----------------------------
    logger.info("Processing gender_profile_female_ratio ...")
    write_gender_profile_female_ratio(
        args.workdir, cfg["demography"]["gender_profile_female_ratio"]
    )

    logger.info("Processing ethnicity profile ...")
    write_ethnicity_profile(args.workdir, cfg["demography"]["ethnicity_profile"])

    logger.info("Processing age profile ...")
    write_age_profile(args.workdir, cfg["demography"]["age_profile"])

    logger.info("Processing age profile ...")
    write_commorbidity(args.workdir)

    # -----------------------------
    # Get geography data
    # -----------------------------
    logger.info("Processing geography_hierarchy_definition ...")
    write_geography_hierarchy_definition(
        args.workdir, cfg["geography"]["geography_hierarchy_definition"]
    )

    logger.info("Processing super area location ...")
    write_super_area_location(args.workdir, cfg["geography"]["super_area_location"])

    logger.info("Processing area location ... ")
    write_area_location(args.workdir, cfg["geography"]["area_location"])

    logger.info("Processing area socialeconomic index")
    write_area_socialeconomic_index(args.workdir, cfg["geography"]["area_socialeconomic_index"])

    # -----------------------------
    # Get group data
    # -----------------------------
    logger.info("Processing sectors_employee_genders and employees_by_super_area")
    write_sectors_employee_genders(
        args.workdir, cfg["group"]["company"]["sectors_employee_genders"]
    )

    logger.info("Processing employees_by_super_area")
    write_employees_by_super_area(args.workdir, cfg["group"]["company"]["employees_by_super_area"])

    logger.info("Processing sectors_by_super_area")
    write_sectors_by_super_area(args.workdir, cfg["group"]["company"]["sectors_by_super_area"])

    # -----------------------------
    # Get commute data
    # -----------------------------
    write_transport_mode(args.workdir, cfg["group"]["commute"]["transport_mode"])
    write_super_area_name(args.workdir, cfg["group"]["commute"]["super_area_name"])

    # -----------------------------
    # Get group data
    # -----------------------------
    logger.info("Processing household age difference ...")
    write_household_age_difference(args.workdir)

    logger.info("Processing household_number ...")
    write_household_number(args.workdir, cfg["group"]["household"]["household_number"])

    logger.info("Processing workplace_and_home ...")
    write_workplace_and_home(args.workdir, cfg["group"]["others"]["workplace_and_home"])

    logger.info("Job done ...")


if __name__ == "__main__":
    main()
