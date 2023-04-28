from process import JUNE_MODEL, MODEL_PATH
from git import Repo
from os.path import exists, join
from os import makedirs
from shutil import rmtree, move
from subprocess import call
from sys import path as sys_path

def download_june_data(june_model_dir, enable: bool = False):
    """Download the required JUNE data directory

    Args:
        june_model_dir (str): JUNE model directory
        empty_data (bool): if only create an empty data directory
    """
    if enable:
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

        if exists(june_model_dir):
            rmtree(june_model_dir)
        Repo.clone_from(JUNE_MODEL["link"], june_model_dir,  branch=JUNE_MODEL["branch"])
        download_june_data(june_model_dir)

    sys_path.append(june_model_dir)

    return june_model_dir


def create_pseudo_data_folder():
    """Create pseudo data folder is requred for 
    importing or running any JUNE model modules
    """
    pseudo_data_path = join(MODEL_PATH, "data")
    if not exists(pseudo_data_path):
        makedirs(pseudo_data_path)
