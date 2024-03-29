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
    read_population,
    write_age_profile,
    write_ethnicity_profile,
    write_gender_profile_female_ratio,
)
from process.data.disease import copy_disease_cfg
from process.data.geography import (
    write_area_location,
    write_area_socialeconomic_index,
    write_geography_hierarchy_definition,
    write_super_area_location,
    write_super_area_name,
)
from process.data.group import (
    write_company_closure,
    write_employees,
    write_employers_by_firm_size,
    write_employers_by_sector,
    write_hospital_cfg,
    write_hospitals,
    write_household_age_difference,
    write_household_communal,
    write_household_def,
    write_household_number,
    write_household_student,
    write_leisiure_def,
    write_leisures,
    write_neighbour_hospitals,
    write_number_of_inter_city_stations,
    write_passage_seats_ratio,
    write_school,
    write_subsector_cfg,
    write_transport_def,
    write_transport_mode,
    write_workplace_and_home,
)
from process.data.interaction import write_interaction
from process.data.policy import copy_policy_file
from process.data.simulation import copy_simulation_file
from process.data.utils import housekeeping, postproc
from process.data.vaccine import copy_vaccine_file
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
    parser.add_argument(
        "--scale",
        required=False,
        default=1.0,
        help="The scale of population [default = 1.0]",
        type=str,
    )

    parser.add_argument(
        "--disease_cfg_dir",
        type=str or None,
        help="Directory contains diseases configuration",
        default=None,
    )

    parser.add_argument(
        "--policy_cfg_path",
        type=str or None,
        help="Policy file to be used",
        default=None,
    )

    parser.add_argument(
        "--simulation_cfg_path",
        type=str or None,
        help="Simulation configuration",
        default=None,
    )

    parser.add_argument(
        "--vaccine_cfg_path",
        type=str or None,
        help="Vaccine configuration",
        default=None,
    )

    parser.add_argument("--use_sa3_as_super_area", action="store_true")

    return parser.parse_args(
        [
            "--workdir",
            "etc/data/realworld_auckland",
            "--use_sa3_as_super_area",
            "--cfg",
            "etc/cfg/run/june_data.yml",
            "--scale",
            "1.0",
            "--disease_cfg_dir",
            "etc/cfg/disease/covid-19",
            "--policy_cfg_path",
            "etc/cfg/policy/policy1.yaml",
            "--simulation_cfg_path",
            "etc/cfg/simulation/simulation_cfg.yml",
            "--vaccine_cfg_path",
            "etc/cfg/disease/vaccine/vaccine1.yaml",
        ]
    )


def main():
    """Getting data for running JUNE"""
    args = setup_parser()

    if not exists(args.workdir):
        makedirs(args.workdir)

    logger = setup_logging(args.workdir)

    logger.info("Reading configuration ...")
    cfg = read_cfg(args.cfg)

    logger.info("Writing total population ...")

    pop = read_population(cfg["total_population"])

    # =============================
    # Get geography data
    # =============================
    logger.info("Processing geography_hierarchy_definition ...")
    geography_hierarchy_definition = write_geography_hierarchy_definition(
        args.workdir,
        args.use_sa3_as_super_area,
        cfg["geography"]["geography_hierarchy_definition"],
    )

    logger.info("Processing super area location ...")
    super_area_location = write_super_area_location(
        args.workdir,
        args.use_sa3_as_super_area,
        cfg["geography"],
        geography_hierarchy_definition=geography_hierarchy_definition["data"],
    )

    logger.info("Processing area location ... ")
    area_location = write_area_location(args.workdir, cfg["geography"]["area_location"])

    logger.info("Processing area socialeconomic index")
    area_socialeconomic_index = write_area_socialeconomic_index(
        args.workdir,
        cfg["geography"]["area_socialeconomic_index"],
        geography_hierarchy_definition=geography_hierarchy_definition["data"],
    )
    super_area_name = write_super_area_name(
        args.workdir,
        args.use_sa3_as_super_area,
        geography_hierarchy_definition_cfg=cfg["geography"]["geography_hierarchy_definition"],
    )

    # =============================
    # Get demography data
    # =============================
    logger.info("Processing gender_profile_female_ratio ...")
    gender_profile_female_ratio = write_gender_profile_female_ratio(
        args.workdir, cfg["demography"]["gender_profile_female_ratio"]
    )

    logger.info("Processing ethnicity profile ...")
    ethnicity_profile = write_ethnicity_profile(
        args.workdir, cfg["demography"]["ethnicity_profile"], pop=pop
    )

    logger.info("Processing age profile ...")
    age_profile = write_age_profile(args.workdir, cfg["demography"]["age_profile"], pop=pop)

    # =============================
    # Get group data
    # =============================
    # ----------------
    # Company
    # ----------------
    logger.info("Processing employees")
    employees = write_employees(
        args.workdir,
        cfg["group"]["company"]["employees"],
        pop=pop,
        use_sa3_as_super_area=args.use_sa3_as_super_area,
    )  # sectors_employee_genders

    logger.info("Processing employers_by_firm_size")
    employers_by_firm_size = write_employers_by_firm_size(
        args.workdir,
        cfg["group"]["company"]["employers_by_firm_size"],
        pop=pop,
        geography_hierarchy_definition=geography_hierarchy_definition["data"],
        use_sa3_as_super_area=args.use_sa3_as_super_area,
    )  # employees_by_super_area

    logger.info("Processing employers_by_sector")
    employers_by_sector = write_employers_by_sector(
        args.workdir,
        cfg["group"]["company"]["employers_by_sector"],
        pop=pop,
        geography_hierarchy_definition=geography_hierarchy_definition["data"],
        use_sa3_as_super_area=args.use_sa3_as_super_area,
        employers_by_firm_size_data_input=employers_by_firm_size["data"],
    )  # sectors_by_super_area

    logger.info("Processing company_closure")
    write_company_closure(args.workdir)

    logger.info("Processing subsector_cfg")
    write_subsector_cfg(args.workdir)

    # -----------------------------
    # Get commute data
    # -----------------------------
    write_transport_def(args.workdir)
    write_passage_seats_ratio(
        args.workdir,
        geography_hierarchy_definition=geography_hierarchy_definition["data"],
        use_sa3_as_super_area=args.use_sa3_as_super_area,
    )
    write_number_of_inter_city_stations(
        args.workdir,
        pop=pop,
        geography_hierarchy_definition=geography_hierarchy_definition["data"],
        use_sa3_as_super_area=args.use_sa3_as_super_area,
    )
    transport_mode = write_transport_mode(args.workdir, cfg["group"]["commute"]["transport_mode"])
    workplace_and_home = write_workplace_and_home(
        args.workdir,
        cfg["group"]["commute"]["workplace_and_home"],
        geography_hierarchy_definition=geography_hierarchy_definition["data"],
        use_sa3_as_super_area=args.use_sa3_as_super_area,
    )

    # ----------------
    # Household
    # ----------------
    logger.info("Processing household age difference ...")
    write_household_age_difference(args.workdir)

    logger.info("Processing household_number ...")
    household_number = write_household_number(
        args.workdir, cfg["group"]["household"]["household_number"]
    )

    write_household_def(args.workdir)

    logger.info("Processing household_student ...")
    household_student = write_household_student(args.workdir, pop)

    logger.info("Processing household_communal ...")
    household_communal = write_household_communal(args.workdir, pop)

    # ----------------
    # Hospital
    # ----------------
    logger.info("Processing hospitals")
    hospitals = write_hospitals(
        args.workdir, cfg["group"]["hospital"]["hospitals"]
    )  # hospital_locations

    write_hospital_cfg(args.workdir)
    write_neighbour_hospitals(args.workdir)
    # ----------------
    # School
    # ----------------
    logger.info("Processing schools")
    schools = write_school(args.workdir, cfg["group"]["school"]["schools"])

    # ----------------
    # Leisure
    # ----------------
    logger.info("Processing leisure ...")
    write_leisures(args.workdir)
    write_leisiure_def(args.workdir)

    # =============================
    # Get interaction data
    # =============================
    write_interaction(args.workdir)

    # =============================
    # Get disease data
    # =============================
    if args.disease_cfg_dir is not None:
        logger.info("Processing disease ...")
        copy_disease_cfg(args.workdir, args.disease_cfg_dir)

    # =============================
    # Get policy data
    # =============================
    if args.policy_cfg_path is not None:
        logger.info("Processing policy ...")
        copy_policy_file(args.workdir, args.policy_cfg_path)

    # =============================
    # Get simulation data
    # =============================
    if args.simulation_cfg_path is not None:
        logger.info("Processing simulation configuration file ...")
        copy_simulation_file(args.workdir, args.simulation_cfg_path)

    # =============================
    # Get vaccine data
    # =============================
    if args.vaccine_cfg_path is not None:
        logger.info("Processing vaccine configuration file ...")
        copy_vaccine_file(args.workdir, args.vaccine_cfg_path)

    # -----------------------------
    # Housekeep
    # -----------------------------
    logger.info("Running postprocessing ...")
    postproc(
        {
            "geography_hierarchy_definition": geography_hierarchy_definition,
            "super_area_location": super_area_location,
            "area_location": area_location,
            "area_socialeconomic_index": area_socialeconomic_index,
            "gender_profile_female_ratio": gender_profile_female_ratio,
            "ethnicity_profile": ethnicity_profile,
            "age_profile": age_profile,
            "employees": employees,
            "employers_by_firm_size": employers_by_firm_size,
            "employers_by_sector": employers_by_sector,
            "hospitals": hospitals,
            "schools": schools,
            "transport_mode": transport_mode,
            "super_area_name": super_area_name,
            "household_number": household_number,
            "workplace_and_home": workplace_and_home,
            "household_student": household_student,
            "household_communal": household_communal,
        },
        scale=float(args.scale),
        domains_cfg=cfg["domains"],
    )

    logger.info("Processing house keeping ...")
    housekeeping(args.workdir)

    logger.info("Job done ...")


if __name__ == "__main__":
    main()
