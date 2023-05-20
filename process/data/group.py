from copy import deepcopy
from re import match as re_match

from numpy import nan as numpy_nan
from pandas import DataFrame, pivot_table, read_csv, read_excel

from process import REGION_NAMES_CONVERSIONS
from process.data.utils import get_raw_data


def read_leed(leed_path: str, anzsic_code: DataFrame, if_rate: bool = False) -> DataFrame:
    """Read NZ stats LEED data

    Args:
        leed_path (str): leed path to be processed
        anzsic_code (Dataframe): ANZSIC codes
        if_rate (bool): if return male and female rate

    Returns:
        DataFrame: Leed dataset
    """
    df = read_excel(leed_path)
    industrial_row = df.iloc[0].fillna(method="ffill")

    if anzsic_code is not None:
        for i, row in enumerate(industrial_row):
            row = row.strip()

            if row in ["Industry", "Total people"]:
                continue

            code = anzsic_code[anzsic_code["Description"] == row]["Anzsic06"].values[0]
            industrial_row[i] = code

    # x = anzsic_code.set_index("Description")
    sec_row = df.iloc[1].fillna(method="ffill")
    titles = industrial_row + "," + sec_row
    titles[
        "Number of Employees by Industry, Age Group, Sex, and Region (derived from 2018 Census)"
    ] = "Area"
    titles["Unnamed: 1"] = "Age"
    titles["Unnamed: 2"] = "tmp"

    df = df.iloc[3:]
    df = df.drop(df.index[-1:])
    df = df.rename(columns=titles)
    df = df.drop("tmp", axis=1)
    df["Area"] = df["Area"].fillna(method="ffill")
    # return df.rename(columns=lambda x: x.strip())

    df["Area"] = df["Area"].replace("Manawatu-Wanganui Region", "Manawatu-Whanganui Region")

    if anzsic_code is not None:
        character_indices = set(
            [
                col.split(",")[0][0]
                for col in df.columns
                if col not in ["Area", "Age", "Total people,Male", "Total people, Female"]
            ]
        )

        # Iterate over the unique character indices to sum the corresponding columns
        for char_index in character_indices:
            subset_cols_male = [
                col
                for col in df.columns
                if col.startswith(char_index)
                and col.endswith("Male")
                and col not in ["Area", "Age", "Total people,Male", "Total people,Female"]
            ]
            subset_cols_female = [
                col
                for col in df.columns
                if col.startswith(char_index)
                and col.endswith("Female")
                and col not in ["Area", "Age", "Total people,Male", "Total people,Female"]
            ]
            summed_col_male = f"{char_index},Male"
            summed_col_female = f"{char_index},Female"
            df[summed_col_male] = df[subset_cols_male].sum(axis=1)
            df[summed_col_female] = df[subset_cols_female].sum(axis=1)
            df = df.drop(subset_cols_male + subset_cols_female, axis=1)

    df["Area"] = df["Area"].str.replace(" Region", "")

    if not if_rate:
        return df

    industrial_columns = [
        x
        for x in list(df.columns)
        if x not in ["Area", "Age", "Total people,Male", "Total people,Female"]
    ]

    df = df.groupby("Area")[industrial_columns].sum()

    df_rate = deepcopy(df)

    # Calculate percentages
    for column in df.columns:
        group = column.split(",")[0]
        total = df[[f"{group},Male", f"{group},Female"]].sum(
            axis=1
        )  # Calculate the total for the group

        total.replace(0, numpy_nan, inplace=True)
        df_rate[column] = df[column] / total

    return df_rate


def read_anzsic_code(anzsic06_code_path: str) -> DataFrame:
    """Read ANZSIC code

    Args:
        anzsic06_code_path (str): ANZSIC data path

    Returns:
        DataFrame: code in a dataframe
    """
    anzsic_code = read_csv(anzsic06_code_path)

    for _, row in anzsic_code.iterrows():
        row["Description"] = " ".join(row["Description"].split()[1:])

    return anzsic_code


def write_sectors_by_super_area(workdir: str, sectors_by_super_area_cfg: dict):
    """Write number of employers by sectors for super area

    Args:
        workdir (str): _description_
        sectors_by_super_area_cfg (dict): Configuration
    """
    data_path = get_raw_data(
        workdir,
        sectors_by_super_area_cfg,
        "sectors_by_super_area",
        "group/company",
        force=True,
    )

    data = read_csv(data_path["raw"])[["Area", "ANZSIC06", "Value"]]

    data["Area"] = data["Area"].str.replace(" Region", "")
    data["Area"] = data["Area"].replace("Manawatu-Wanganui", "Manawatu-Whanganui")
    data["Area"] = data["Area"].map({v: k for k, v in REGION_NAMES_CONVERSIONS.items()})

    data["ANZSIC06"] = data["ANZSIC06"].str[0]

    df_pivot = (
        pivot_table(data, values="Value", index="Area", columns="ANZSIC06").dropna().astype(int)
    ).reset_index()

    df_pivot = df_pivot.rename(columns={"Area": "MSOA"})
    df_pivot.to_csv(data_path["output"], index=False)


def write_employees_by_super_area(workdir: str, employees_by_super_area_cfg: dict):
    """Write number of employees by age for super area

    Args:
        workdir (str): _description_
        employees_by_super_area_cfg (dict): _description_
    """
    data_path = get_raw_data(
        workdir,
        employees_by_super_area_cfg,
        "employees_by_super_area",
        "group/company",
        force=True,
    )

    data = read_csv(data_path["raw"])[
        ["Area", "Measure", "Enterprise employee count size group", "Value"]
    ]
    data["Area"] = data["Area"].str.replace(" Region", "")

    data = data.drop(data[data["Enterprise employee count size group"] == "Total"].index)
    data = data[data["Measure"] == "Geographic Units"]

    data = data[["Area", "Enterprise employee count size group", "Value"]]

    data["Area"] = data["Area"].replace("Manawatu-Wanganui", "Manawatu-Whanganui")

    data["Area"] = data["Area"].map({v: k for k, v in REGION_NAMES_CONVERSIONS.items()})

    data["Enterprise employee count size group"] = (
        data["Enterprise employee count size group"]
        .replace("1 to 19", "1-19")
        .replace("20 to 49", "20-49")
        .replace("50+", "50-xxx")
    )

    df_pivot = pivot_table(
        data, values="Value", index="Area", columns="Enterprise employee count size group"
    ).reset_index()
    df_pivot = df_pivot[["Area", "1-19", "20-49", "50-xxx"]]

    df_pivot = df_pivot.rename(columns={"Area": "MSOA"})

    df_pivot.to_csv(data_path["output"], index=False)


def write_sectors_employee_genders(workdir: str, sectors_employee_genders_cfg: dict):
    """Write the number of employees by gender for different area

    Args:
        workdir (str): Working directory
        sectors_employee_genders_cfg (dict): Configuration
    """

    def _rename_column(column_name):
        # Define a regular expression pattern to match the column names
        pattern = r"([a-zA-Z]+) ([a-zA-Z]+)"
        matches = re_match(pattern, column_name)
        if matches:
            gender = matches.group(1)[0].lower()
            category = matches.group(2)
            return f"{gender} {category}"
        return column_name

    data_path = get_raw_data(
        workdir,
        sectors_employee_genders_cfg,
        "sectors_employee_genders",
        "group/company",
        force=True,
    )

    # Read Leed rate for region
    data_leed_rate = read_leed(
        data_path["deps"]["leed"],
        read_anzsic_code(data_path["deps"]["anzsic06_code"]),
        if_rate=True,
    )

    # Read employees for different SA2
    data = read_csv(data_path["raw"])[["anzsic06", "Area", "ec_count"]]

    data = data[
        data["anzsic06"].isin(list(set([col.split(",")[0] for col in data_leed_rate.columns])))
    ]

    data_sa2 = data[data["Area"].str.startswith("A")]

    data_sa2 = data_sa2.rename(columns={"Area": "area"})

    data_sa2["area"] = data_sa2["area"].str[1:].astype(int)

    # Read geography hierarchy
    geography_hierarchy_definition = read_csv(data_path["deps"]["geography_hierarchy_definition"])

    data_sa2 = data_sa2.merge(
        geography_hierarchy_definition[["area", "super_area"]], on="area", how="left"
    )

    data_sa2 = data_sa2.dropna()

    data_sa2["super_area"] = data_sa2["super_area"].astype(int)

    data_leed_rate = data_leed_rate.reset_index()

    data_leed_rate["super_area"] = data_leed_rate["Area"].map(
        {v: k for k, v in REGION_NAMES_CONVERSIONS.items()}
    )

    data_sa2 = data_sa2.merge(data_leed_rate, on="super_area", how="left")

    industrial_codes = []
    industrial_codes_with_genders = []
    for proc_item in list(data_sa2.columns):
        if proc_item.endswith("Male"):
            proc_code = proc_item.split(",")[0]
            industrial_codes.append(proc_code)
            industrial_codes_with_genders.extend([f"{proc_code},Male", f"{proc_code},Female"])

    # Create new columns 'male' and 'female' based on 'anzsic06' prefix
    for category in industrial_codes:
        male_col = f"{category},Male"
        female_col = f"{category},Female"
        data_sa2.loc[data_sa2["anzsic06"] == category, "Male"] = (
            data_sa2[male_col] * data_sa2["ec_count"]
        )
        data_sa2.loc[data_sa2["anzsic06"] == category, "Female"] = (
            data_sa2[female_col] * data_sa2["ec_count"]
        )

    df = data_sa2.drop(columns=industrial_codes_with_genders)

    df["Male"] = df["Male"].astype("int")
    df["Female"] = df["Female"].astype("int")

    df_pivot = pivot_table(df, index="area", columns="anzsic06", values=["Male", "Female"])

    df_pivot.columns = [f"{col[0]} {col[1]}" for col in df_pivot.columns]

    df_pivot = df_pivot.fillna(0.0)
    df_pivot = df_pivot.astype(int)

    df_pivot = (
        df_pivot.rename(columns=_rename_column).reset_index().rename(columns={"area": "oareas"})
    )

    df_pivot.to_csv(data_path["output"], index=False)


def write_company_info(
    workdir: str,
    comnpany_cfg: dict,
):
    """Write sector/company related data using the stats sent over by NZ Stats, which includes:
        - At super area level:
         * employees_by_super_area.csv: the number of employees by each age category
         * sectors_by_super_area.csv: number of companies in each sector
        - At area level:
         * sectors_employee_genders.csv: number of employees by each industrials + by gender

    Args:
        workdir (str): working directory
        comnpany_cfg (dict): Company data configuration
    """
    if comnpany_cfg["path"].startswith("https"):
        raw_data_path = download_file(comnpany_cfg["path"], workdir=workdir)

    from pandas import read_excel

    df = read_excel(raw_data_path, header=1)
