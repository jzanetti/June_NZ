from os import rename
from os.path import join

from pandas import read_csv as pandas_read_csv
from yaml import safe_load


def tuning_wrapper(data_cfg: dict, tuning_cfg_path: str or None):
    """Model tuning wrapper

    Args:
        data_cfg (dict): Data configuration
        tuning_cfg_path (str or None): Model tuning configuration path
    """

    if tuning_cfg_path is None:
        return

    with open(tuning_cfg_path, "r") as fid:
        tuning_cfg = safe_load(fid)

    if "infection_outcome" in tuning_cfg:
        update_infection_outcome(
            tuning_cfg["infection_outcome"],
            join(data_cfg["base_dir"], data_cfg["disease"]["infection_outcome"]),
        )


def update_infection_outcome(infection_outcome_cfg: dict, infection_outcome_path: str):
    """Update infection outcome

    Args:
        infection_outcome_cfg (dict): Infection outcome tuning configuration
        infection_outcome_path (str): Infection outcome data path
    """
    data = pandas_read_csv(infection_outcome_path)

    for age_range in list(data.iloc[:, 0]):
        df = data[data.iloc[:, 0] == age_range]
        age_min, age_max = map(int, age_range.strip("[]").split(", "))

        for proc_age_key in infection_outcome_cfg["adjust_factor"]:
            proc_age_key_min, proc_age_key_max = map(int, proc_age_key.split("-"))

            if age_min < proc_age_key_min or age_max > proc_age_key_max:
                continue

            for proc_pop_key in infection_outcome_cfg["adjust_factor"][proc_age_key]:
                for proc_sex_key in infection_outcome_cfg["adjust_factor"][proc_age_key][
                    proc_pop_key
                ]:
                    for proc_symptom_key in infection_outcome_cfg["adjust_factor"][proc_age_key][
                        proc_pop_key
                    ][proc_sex_key]:
                        proc_key = f"{proc_pop_key}_{proc_symptom_key}_{proc_sex_key}"

                        proc_factor = infection_outcome_cfg["adjust_factor"][proc_age_key][
                            proc_pop_key
                        ][proc_sex_key][proc_symptom_key]

                        df[proc_key] = df[proc_key] * proc_factor

                    proc_df = df.filter(regex=rf"^{proc_pop_key}.*_{proc_sex_key}$")

                    updated_df = proc_df / proc_df.sum().sum()

                    data.loc[data.iloc[:, 0] == age_range, list(updated_df.columns)] = updated_df

    rename(infection_outcome_path, infection_outcome_path + ".backup")

    data.to_csv(infection_outcome_path, index=False)
