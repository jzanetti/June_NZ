

JUNE_MODEL = {
    "link": "https://github.com/IDAS-Durham/JUNE.git",
    "model_name": "JUNE_v1.2.0",
    "code_replacement": {
        "june/paths.py": [
                {
                    # Running JUNE requires the working directory is in the repository,
                    # if we put the repository under lib/JUNE_v1.2.0, we need to change the
                    # working directory of JUNE to there (otherwise it will be the working
                    # directory for our wrapper JUNE_NZ)
                    "id": "adjust_workding_dir",
                    "src": "working_directory = Path(os.getcwd())",
                    "dest": "working_directory = Path('lib/JUNE_v1.2.0')"
                }
            ]
    }
}
