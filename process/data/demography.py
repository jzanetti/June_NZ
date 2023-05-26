from math import ceil as math_ceil
from os.path import join

from pandas import DataFrame, melt, merge, read_excel

from process import FIXED_DATA
from process.data.utils import get_raw_data


def write_gender_profile_female_ratio(workdir: str, gender_profile_female_ratio_cfg: dict):
    """Write gender_profile_female_ratio

    Args:
        workdir (str): Working directory
        gender_profile_female_ratio_cfg (dict): gender_profile_female_ratio configuration
    """
    data_path = get_raw_data(
        workdir,
        gender_profile_female_ratio_cfg,
        "gender_profile_female_ratio",
        "demography",
        force=True,
    )

    df = read_excel(data_path["raw"], header=3)

    df = df.rename(
        columns={
            "Male": "Male (15)",
            "Female": "Female (15)",
            "Male.1": "Male (40)",
            "Female.1": "Female (40)",
            "Male.2": "Male (65)",
            "Female.2": "Female (65)",
            "Male.3": "Male (100)",
            "Female.3": "Female (100)",
            "Sex": "output_area",
        }
    )

    df = df.drop("Unnamed: 1", axis=1)

    df = df.drop([0, 1, 2]).drop(df.tail(3).index).astype(int)

    df = df[df["output_area"] > 10000]

    for age in ["15", "40", "65", "100"]:
        df[age] = df[f"Female ({age})"] / (df[f"Male ({age})"] + df[f"Female ({age})"])

    df = df[["output_area", "15", "40", "65", "100"]]

    df.to_csv(data_path["output"], index=False)

    return {"data": df, "output": data_path["output"]}


def write_ethnicity_profile(workdir: str, ethnicity_cfg: dict):
    """Write ethnicity profile

    Args:
        workdir (str): Working directory
        ethnicity_cfg (dict): Ethnicity configuration
    """

    def _get_all_paths(data_path: dict) -> dict:
        """Get all paths to be read

        Args:
            data_path (dict): data path to be checked

        Returns:
            dict: data path to be read
        """
        all_paths = {
            "15": data_path["raw"],
            "30": data_path["deps"][1529],
            "65": data_path["deps"][3064],
            "100": data_path["deps"][65100],
        }
        return all_paths

    data_path = get_raw_data(
        workdir,
        ethnicity_cfg,
        "ethnicity_profile",
        "demography",
        force=True,
    )

    input_data = _get_all_paths(data_path)

    dfs = []

    for proc_age_key in input_data:
        df = read_excel(input_data[proc_age_key], header=4)
        df = df.drop([0, 1]).drop(df.tail(3).index)
        df = df.drop("Unnamed: 1", axis=1)
        df.columns = df.columns.str.strip()

        df = df.rename(
            columns={
                "Ethnic group": "output_area",
                "Pacific Peoples": "Pacific",
                "Middle Eastern/Latin American/African": "MELAA",
            }
        )

        dfs.append(
            melt(
                df,
                id_vars=["output_area"],
                value_vars=[
                    "European",
                    "Maori",
                    "Pacific",
                    "Asian",
                    "MELAA",
                ],
                var_name="ethnicity",
                value_name=proc_age_key,
            )
        )

    # Assuming 'dataframes' is a list containing your DataFrames
    combined_df = merge(dfs[0], dfs[1], on=["output_area", "ethnicity"])
    for i in range(2, len(dfs)):
        combined_df = merge(combined_df, dfs[i], on=["output_area", "ethnicity"])

    combined_df.to_csv(data_path["output"], index=False)

    return {"data": combined_df, "output": data_path["output"]}


def write_commorbidity(workdir: str):
    """Convert the fixed commorbidity data

    Args:
        workdir (str): Working directory
    """
    for proc_file_key in FIXED_DATA["demography"]:
        proc_data = FIXED_DATA["demography"][proc_file_key]
        data = DataFrame.from_dict(proc_data)
        data.to_csv(join(workdir, "demography", f"{proc_file_key}.csv"), index=False)


def write_age_profile(workdir: str, age_profile_cfg: dict):
    """Write age profile

    Args:
        workdir (str): Working directory
        age_profile_cfg (dict): Age profile configuration
    """

    def _find_range(number, ranges):
        for age_range in ranges:
            start, end = map(int, age_range.split("-"))
            if start <= number <= end:
                return age_range
        return None

    data_path = get_raw_data(
        workdir,
        age_profile_cfg,
        "age_profile",
        "demography",
        force=True,
    )

    df = read_excel(data_path["raw"], header=2)

    df.columns = df.columns.str.strip()

    df = df[
        [
            "Region and Age",
            "0-4 Years",
            "5-9 Years",
            "10-14 Years",
            "15-19 Years",
            "20-24 Years",
            "25-29 Years",
            "30-34 Years",
            "35-39 Years",
            "40-44 Years",
            "45-49 Years",
            "50-54 Years",
            "55-59 Years",
            "60-64 Years",
            "65-69 Years",
            "70-74 Years",
            "75-79 Years",
            "80-84 Years",
            "85-89 Years",
            "90 Years and over",
        ]
    ]

    df = df.drop(df.index[-1])

    df["Region and Age"] = df["Region and Age"].str.strip()

    df = df[~df["Region and Age"].isin(["NZRC", "NIRC", "SIRC"])]

    df["Region and Age"] = df["Region and Age"].astype(int)

    df = df[df["Region and Age"] > 10000]

    df = df.set_index("Region and Age")

    df.columns = [str(name).replace(" Years", "") for name in df]
    df = df.rename(columns={"90 and over": "90-100"})

    new_df = DataFrame(columns=["Region"] + list(range(0, 101)))

    for cur_age in list(new_df.columns):
        if cur_age == "Region":
            new_df["Region"] = df.index
        else:
            age_range = _find_range(cur_age, list(df.columns))
            age_split = age_range.split("-")
            start_age = int(age_split[0])
            end_age = int(age_split[1])
            age_length = end_age - start_age + 1
            new_df[cur_age] = (df[age_range] / age_length).values

    new_df = new_df.applymap(math_ceil)

    new_df = new_df.rename(columns={"Region": "output_area"})

    new_df.to_csv(data_path["output"], index=False)

    return {"data": new_df, "output": data_path["output"]}
