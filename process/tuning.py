from os import rename
from os.path import exists, join

from pandas import DataFrame
from pandas import read_csv as pandas_read_csv
from yaml import dump as yaml_dump
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

    if tuning_cfg["infection_outcome"]["enable"]:
        update_infection_outcome(
            tuning_cfg["infection_outcome"],
            join(data_cfg["base_dir"], data_cfg["disease"]["infection_outcome"]),
        )

    if tuning_cfg["contact_frequency_beta"]["enable"]:
        update_contact_frequency_beta(
            tuning_cfg["contact_frequency_beta"],
            join(
                data_cfg["base_dir"],
                data_cfg["group_and_interaction"]["others"]["general_interaction"],
            ),
        )

    if tuning_cfg["pobability_of_infection"]["enable"]:
        update_pobability_of_infection(
            tuning_cfg["pobability_of_infection"],
            join(data_cfg["base_dir"], data_cfg["disease"]["transmission_profile"]),
        )

    if tuning_cfg["symptom_trajectory"]["enable"]:
        update_symptom_trajectory(
            tuning_cfg["symptom_trajectory"],
            join(data_cfg["base_dir"], data_cfg["disease"]["sympton_trajectories"]),
        )


def update_symptom_trajectory(symptom_trajectory_cfg, symptom_trajectory_path: str):
    """Updatesymptom trajectory

    Args:
        symptom_trajectory_cfg (_type_): Tuning configuration
        symptom_trajectory_path (str): Origina lsymptom_trajectory path
    """

    def _get_symptom_info(symptom_trajectory_cfg: dict) -> dict:
        """Get symptom information

        Args:
            symptom_trajectory_cfg (dict): Symptom trajectory information

        Returns:
            dict: Tuning information
        """
        output = {}
        for proc_traj in symptom_trajectory_cfg["adjust_factor"]:
            if proc_traj == "general":
                continue

            proc_traj_name = sorted(
                [
                    elem.replace(" ", "")
                    for elem in symptom_trajectory_cfg["adjust_factor"][proc_traj]["name"].split(
                        "=>"
                    )
                ]
            )

            proc_traj_cfg = symptom_trajectory_cfg["adjust_factor"][proc_traj]["paras"]

            output[",".join(proc_traj_name)] = proc_traj_cfg

        return output

    if exists(symptom_trajectory_path + ".backup"):
        with open(symptom_trajectory_path + ".backup", "r") as fid:
            data = safe_load(fid)
        read_from_backup = True
    else:
        with open(symptom_trajectory_path, "r") as fid:
            data = safe_load(fid)
        read_from_backup = False

    # Update general:
    for i, proc_traj in enumerate(data["trajectories"]):
        for j, proc_stage in enumerate(proc_traj["stages"]):
            proc_func = proc_stage["completion_time"]
            proc_func_type = proc_func["type"]

            if proc_func_type in symptom_trajectory_cfg["adjust_factor"]["general"]:
                if symptom_trajectory_cfg["adjust_factor"]["general"][proc_func_type]["enable"]:
                    for ele in symptom_trajectory_cfg["adjust_factor"]["general"][proc_func_type]:
                        if ele == "enable":
                            continue
                        data["trajectories"][i]["stages"][j]["completion_time"][
                            ele
                        ] *= symptom_trajectory_cfg["adjust_factor"]["general"][proc_func_type][
                            ele
                        ]

    # Update a specific trajectory
    symptom_to_tune_info = _get_symptom_info(symptom_trajectory_cfg)
    for i, proc_traj in enumerate(data["trajectories"]):
        all_symptoms = []
        for j, proc_stage in enumerate(proc_traj["stages"]):
            all_symptoms.append(proc_traj["stages"][j]["symptom_tag"])
        all_symptoms = ",".join(sorted(all_symptoms))
        # dict_keys(['exposed,intensive_care,mild,recovered'])
        if all_symptoms in symptom_to_tune_info:
            for proc_info in symptom_to_tune_info[all_symptoms]:
                proc_tag = proc_info["symptom_tag"]

                for j, proc_stage in enumerate(proc_traj["stages"]):
                    if proc_tag == proc_traj["stages"][j]["symptom_tag"]:
                        data["trajectories"][i]["stages"][j]["completion_time"] = proc_info[
                            "completion_time"
                        ]

    if not read_from_backup:
        rename(symptom_trajectory_path, symptom_trajectory_path + ".backup")

    with open(symptom_trajectory_path, "w") as fid:
        yaml_dump(data, fid, default_flow_style=False)


def update_pobability_of_infection(
    pobability_of_infection_cfg: dict, pobability_of_infection_path: str
):
    """Update probability of infection

    Args:
        pobability_of_infection_cfg (dict): Tuning configuration
        pobability_of_infection_path (str): Original pobability_of_infection path
    """
    if exists(pobability_of_infection_path + ".backup"):
        with open(pobability_of_infection_path + ".backup", "r") as fid:
            data = safe_load(fid)
        read_from_backup = True
    else:
        with open(pobability_of_infection_path, "r") as fid:
            data = safe_load(fid)
        read_from_backup = False

    for proc_factor in pobability_of_infection_cfg["adjust_factor"]:
        data[proc_factor] = pobability_of_infection_cfg["adjust_factor"][proc_factor]

    if not read_from_backup:
        rename(pobability_of_infection_path, pobability_of_infection_path + ".backup")

    with open(pobability_of_infection_path, "w") as fid:
        yaml_dump(data, fid, default_flow_style=False)


def update_contact_frequency_beta(
    contact_frequency_beta_cfg: dict, contact_frequency_beta_path: str
):
    """Update contact frequency beta

    Args:
        contact_frequency_beta_cfg (dict): Tuning configuration
        contact_frequency_beta_path (str): Original freuqncy beta path
    """
    if exists(contact_frequency_beta_path + ".backup"):
        with open(contact_frequency_beta_path + ".backup", "r") as fid:
            data = safe_load(fid)
        read_from_backup = True
    else:
        with open(contact_frequency_beta_path, "r") as fid:
            data = safe_load(fid)
        read_from_backup = False

    for group in data["betas"]:
        if group in contact_frequency_beta_cfg["adjust_factor"]:
            proc_factor = contact_frequency_beta_cfg["adjust_factor"][group]

        data["betas"][group] *= proc_factor

    if not read_from_backup:
        rename(contact_frequency_beta_path, contact_frequency_beta_path + ".backup")

    with open(contact_frequency_beta_path, "w") as fid:
        yaml_dump(data, fid, default_flow_style=False)


def update_infection_outcome(infection_outcome_cfg: dict, infection_outcome_path: str):
    """Update infection outcome

    Args:
        infection_outcome_cfg (dict): Infection outcome tuning configuration
        infection_outcome_path (str): Infection outcome data path
    """

    def _check_infection_outcome(
        df: DataFrame, proc_age_key: str, proc_pop_key: str, proc_sex_key: str
    ):
        """Check infection outcome:
            - Hospital ratio > ICU ratio
            - Hospital ratio > Hospital IFR ratio
            - ICU ratio > ICU IFR ratio

        Args:
            df (DataFrame): Dataframe to be checked
            proc_age_key (str): Age key, e.g, 30-50
            proc_pop_key (str): Population key, e.g., gp
            proc_sex_key (str): Sex key, e.g., female and male

        Raises:
            Exception: Failure message
        """
        if (
            df[f"{proc_pop_key}_hospital_{proc_sex_key}"]
            < df[f"{proc_pop_key}_icu_{proc_sex_key}"]
        ).values[0]:
            raise Exception(
                f"Hospital ratio < ICU ratio for {proc_age_key} ({proc_pop_key}, {proc_sex_key})"
            )

        if (
            df[f"{proc_pop_key}_hospital_{proc_sex_key}"]
            < df[f"{proc_pop_key}_hospital_ifr_{proc_sex_key}"]
        ).values[0]:
            raise Exception(
                f"Hospital ratio < Hospital IFR ratio for {proc_age_key} ({proc_pop_key}, {proc_sex_key})"
            )

        if (
            df[f"{proc_pop_key}_icu_{proc_sex_key}"] < df[f"{proc_pop_key}_icu_ifr_{proc_sex_key}"]
        ).values[0]:
            raise Exception(
                f"ICU ratio < ICU IFR ratio for {proc_age_key} ({proc_pop_key}, {proc_sex_key})"
            )

    if exists(infection_outcome_path + ".backup"):
        data = pandas_read_csv(infection_outcome_path + ".backup")
        read_from_backup = True
    else:
        data = pandas_read_csv(infection_outcome_path)
        read_from_backup = False

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

                    _check_infection_outcome(updated_df, age_range, proc_pop_key, proc_sex_key)

                    data.loc[data.iloc[:, 0] == age_range, list(updated_df.columns)] = updated_df

    if not read_from_backup:
        rename(infection_outcome_path, infection_outcome_path + ".backup")

    data.to_csv(infection_outcome_path, index=False)
