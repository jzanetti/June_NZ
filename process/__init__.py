

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
            ],
        "june/groups/hospital.py": [
            {
                # originally we set the hospital Dataframe index to 4, but 
                # it does not point to Area which is required 
                # (due to some changes in our hosptial data format)
                "id": "replace_hospital_id",
                "src": "hospital_df = pd.read_csv(filename, index_col=4)",
                "dest": "hospital_df = pd.read_csv(filename, index_col='area')"
            }
        ],
        "june/demography/demography.py": [
             # by default demography data like age etc. have to be read from the default path, 
             # after this changethe demography file can be read from a user defined dict
             {
                "id": "replace_age_profile_path",
                "src": 'age_structure_path = data_path / "age_structure_single_year.csv"',
                "dest": 'age_structure_path = data_path["age_profile"]'
             },
             {
                "id": "replace_gender_profile_path",
                "src": 'female_fraction_path = data_path / "female_ratios_per_age_bin.csv"',
                "dest": 'female_fraction_path = data_path["gender_profile"]'
             },
             {
                "id": "replace_ethnicity_profile_path",
                "src": 'ethnicity_structure_path = data_path / "ethnicity_structure.csv"',
                "dest": 'ethnicity_structure_path = data_path["ethnicity_profile"]'
             },
             {
                "id": "replace_male_comorbidity_path",
                "src": 'm_comorbidity_path = data_path / "uk_male_comorbidities.csv"',
                "dest": 'm_comorbidity_path = data_path["comorbidities"]["male"]'
             },
             {
                "id": "replace_female_comorbidity_path",
                "src": 'f_comorbidity_path = data_path / "uk_female_comorbidities.csv"',
                "dest": 'f_comorbidity_path = data_path["comorbidities"]["female"]'
             },
        ],
        "june/world.py": [
            # Remove houshold and cinema initialition so they 
            # can be initiated from outside the World class
            {
                "id": "remove_household",
                "src": "world.distribute_people(include_households=include_households)",
                "dest": "# world.distribute_people(include_households=include_households)"
            },
            {
                "id": "remove_cinema",
                "src": "world.cemeteries = Cemeteries()",
                "dest": "# world.cemeteries = Cemeteries()"
            }
        ]
    }
}