from process import JUNE_MODEL
from git import Repo
from os.path import exists, join
from shutil import copyfile, rmtree, move
from copy import deepcopy
from subprocess import call
import sys

def update_codes_in_june():
    """Update codes in the JUNE model

    Raises:
        Exception: Obtained more than one line with the same target to be replaced
    """
    for src_file in JUNE_MODEL["code_replacement"]:
        
        all_codes_to_be_processed = JUNE_MODEL["code_replacement"][src_file]

        src_file_template = deepcopy(src_file)

        for proc_code in all_codes_to_be_processed:

            id = proc_code["id"]

            src_file_template = src_file_template + f".{id}"

            src_file_path = join("lib", JUNE_MODEL["model_name"], src_file)

            src_file_template_path = join("lib", JUNE_MODEL["model_name"], src_file_template)

            copyfile(src_file_path, src_file_template_path)

            replaced = False
            with open(src_file_template_path, "rt") as fin:

                with open(src_file_path, "wt") as fout:
                    for line in fin:

                        if proc_code["src"] in line:

                            if replaced:
                                raise Exception(f"Got two lines with the same input: {proc_code['src']} ...")

                            fout.write(line.replace(proc_code["src"], proc_code["dest"]))
                            replaced = True
                        else:
                            fout.write(line)


def download_june_data(june_model_dir):
    """Download the required JUNE data directory

    Args:
        june_model_dir (str): JUNE model directory
    """
    script_path = join(june_model_dir, "scripts", "get_june_data.sh")
    with open(script_path, "rb") as file:
        script = file.read()
    call(script, shell=True)
    move("data", join(june_model_dir, "data"))


def check_availability_for_june_model(checkout_repo: bool = False) -> str:
    """Check the availability of the JUNE model

    Arguments:
        workdir(str): working directory

    Returns:
        str: Downloaded JUNE model directory
    """
    june_model_dir = f"lib/{JUNE_MODEL['model_name']}"

    if checkout_repo or (not exists(june_model_dir)):

        rmtree(june_model_dir)
        Repo.clone_from(JUNE_MODEL["link"], june_model_dir)
        update_codes_in_june()
        download_june_data(june_model_dir)

    sys.path.append(june_model_dir)

    return june_model_dir