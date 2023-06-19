from math import ceil as math_ceil
from os import makedirs
from os.path import exists, join

from numpy import inf, nan
from pandas import DataFrame, concat, melt, merge, read_excel, to_numeric
from yaml import dump as yaml_dump

from process import FIXED_DATA
from process.data.utils import get_raw_data


def read_population(population_path: str):
    """Read population

    Args:
        population_path (str): Population data path
    """
    data = read_excel(population_path, header=6)

    data = data.rename(columns={"Area": "area", "Unnamed: 2": "population"})

    data = data.drop("Unnamed: 1", axis=1)

    # Drop the last row
    data = data.drop(data.index[-1])

    data = data.astype(int)

    data = data[data["area"] > 10000]

    return data


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
            "Male.3": "Male (90)",
            "Female.3": "Female (90)",
            "Sex": "output_area",
        }
    )

    df = df.drop("Unnamed: 1", axis=1)

    df = df.drop([0, 1, 2]).drop(df.tail(3).index).astype(int)

    df = df[df["output_area"] > 10000]

    for age in ["15", "40", "65", "90"]:
        df[age] = df[f"Female ({age})"] / (df[f"Male ({age})"] + df[f"Female ({age})"])

    df = df[["output_area", "15", "40", "65", "90"]]

    df = df.dropna()

    df.to_csv(data_path["output"], index=False)

    return {"data": df, "output": data_path["output"]}


def write_ethnicity_profile(workdir: str, ethnicity_cfg: dict, pop: DataFrame or None = None):
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
            "0": data_path["raw"],
            "15": data_path["deps"][1529],
            "30": data_path["deps"][3064],
            "65": data_path["deps"][65100],
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

    dfs = {}

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

        df = (
            df.apply(to_numeric, errors="coerce").dropna().astype(int)
        )  # convert str ot others to NaN, and drop them and convert the rests to int

        df["total"] = df["European"] + df["Maori"] + df["Pacific"] + df["Asian"] + df["MELAA"]

        dfs[proc_age_key] = df

    if pop is not None:
        df_ratio = concat(list(dfs.values()))
        df_ratio = df_ratio.groupby("output_area").sum().reset_index()
        pop = pop.rename(columns={"area": "output_area"})
        df_ratio = df_ratio.merge(pop, on="output_area")
        df_ratio["ratio"] = df_ratio["population"] / df_ratio["total"]
        df_ratio = df_ratio.drop(
            ["European", "Maori", "Pacific", "Asian", "MELAA", "total", "population"], axis=1
        )

        dfs_after_ratio = {}
        for proc_age in dfs:
            df = dfs[proc_age]

            df = df.merge(df_ratio, on="output_area")
            for race_key in ["European", "Maori", "Pacific", "Asian", "MELAA", "total"]:
                df[race_key] = df[race_key] * df["ratio"]
            df = df.drop(["ratio", "total"], axis=1)
            # df = df.astype(int)
            # df = df.apply(math_ceil).astype(int)
            df = df.round().astype(int)
            dfs_after_ratio[proc_age] = df

        dfs = dfs_after_ratio

    dfs_output = []
    for proc_age in dfs:
        dfs_output.append(
            melt(
                dfs[proc_age],
                id_vars=["output_area"],
                value_vars=[
                    "European",
                    "Maori",
                    "Pacific",
                    "Asian",
                    "MELAA",
                ],
                var_name="ethnicity",
                value_name=proc_age,
            )
        )

    # Assuming 'dataframes' is a list containing your DataFrames
    combined_df = merge(dfs_output[0], dfs_output[1], on=["output_area", "ethnicity"])
    for i in range(2, len(dfs_output)):
        combined_df = merge(combined_df, dfs_output[i], on=["output_area", "ethnicity"])

    combined_df.to_csv(data_path["output"], index=False)

    return {"data": combined_df, "output": data_path["output"]}


def write_age_profile(workdir: str, age_profile_cfg: dict, pop: DataFrame or None = None):
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

    # match populations
    if pop is not None:
        all_ages = range(101)
        for index, row in new_df.iterrows():
            total = sum(row[col] for col in all_ages)
            new_df.at[index, "total"] = total

        pop = pop.rename(columns={"area": "output_area"})
        df_after_ratio = new_df.merge(pop, on="output_area")
        df_after_ratio["ratio"] = df_after_ratio["population"] / df_after_ratio["total"]

        for col in all_ages:
            df_after_ratio[col] = df_after_ratio[col] / df_after_ratio["ratio"]

        df_after_ratio.replace([inf, -inf], nan, inplace=True)
        df_after_ratio.dropna(inplace=True)

        df_after_ratio = df_after_ratio.round().astype(int)

        new_df = df_after_ratio.drop(["total", "population", "ratio"], axis=1)

    new_df.to_csv(data_path["output"], index=False)

    return {"data": new_df, "output": data_path["output"]}
