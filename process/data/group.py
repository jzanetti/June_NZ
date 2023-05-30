from copy import deepcopy
from os.path import join
from re import findall as re_findall
from re import match as re_match

from numpy import arctan2, argmin, cos
from numpy import nan as numpy_nan
from numpy import radians, sin, sqrt
from pandas import DataFrame, merge, pivot_table, read_csv, read_excel
from scipy.spatial.distance import cdist
from shapely.wkt import loads as wkt_loads

from process import FIXED_DATA, REGION_NAMES_CONVERSIONS
from process.data.utils import get_raw_data


def write_household_student(workdir: str, pop: DataFrame) -> DataFrame:
    """Write number of students living in student dorms

    Args:
        workdir (str): Working directory
        pop (DataFrame): Population
    """
    df = DataFrame({"area": pop["area"], "n_students": 0})

    output = join(workdir, "group", "household", "household_student.csv")

    df.to_csv(output, index=False)

    return {"data": df, "output": output}


def write_household_communal(workdir: str, pop: DataFrame):
    """Write number of people living in communal places

    Args:
        workdir (str): Working directory
        pop (DataFrame): Population
    """
    df = DataFrame({"output_area": pop["area"], "0": 0})

    output = join(workdir, "group", "household", "household_commual.csv")

    df.to_csv(output, index=False)

    return {"data": df, "output": output}


def write_hospital_locations(workdir: str, hospital_locations_cfg: dict):
    """Write hospital locations

    Args:
        workdir (str): Working directory
        hospital_locations_cfg (dict): Hospital location configuration
    """

    def _get_central_point(wkt_string: str):
        """Get central point from MultiPolygon

        Args:
            wkt (str): WKT description

        Returns:
            _type_: _description_
        """
        polygon = wkt_loads(wkt_string)
        central_point = polygon.centroid
        return central_point

    def _haversine_distance(lat1, lon1, lat2, lon2):
        """Function to calculate the Haversine distance between two points

        Args:
            lat1 (float): Latitude 1
            lon1 (float): Longitude 1
            lat2 (float): Latitude 1
            lon2 (float): Longitude 2

        Returns:
            _type_: _description_
        """
        r = 6371  # Earth's radius in kilometers
        phi1 = radians(lat1)
        phi2 = radians(lat2)
        delta_phi = radians(lat2 - lat1)
        delta_lambda = radians(lon2 - lon1)
        a = sin(delta_phi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2) ** 2
        c = 2 * arctan2(sqrt(a), sqrt(1 - a))
        distance = r * c
        return distance

    data_path = get_raw_data(
        workdir,
        hospital_locations_cfg,
        "hospital_locations",
        "group/hospital",
        force=True,
    )

    data = read_csv(data_path["raw"])

    data = data[data["use"] == "Hospital"]

    data["Central Point"] = data["WKT"].apply(_get_central_point)

    data["latitude"] = data["Central Point"].apply(lambda point: point.y)
    data["longitude"] = data["Central Point"].apply(lambda point: point.x)

    data = data[["latitude", "longitude", "estimated_occupancy", "source_facility_id"]]

    sa2_loc = read_csv(data_path["deps"]["sa2_loc"])

    sa2_loc = sa2_loc[["SA22018_V1_00", "LATITUDE", "LONGITUDE"]]

    sa2_loc = sa2_loc.rename(
        columns={"LATITUDE": "latitude", "LONGITUDE": "longitude", "SA22018_V1_00": "sa2"}
    )

    distances = cdist(
        data[["latitude", "longitude"]],
        sa2_loc[["latitude", "longitude"]],
        lambda x, y: _haversine_distance(x[0], x[1], y[0], y[1]),
    )

    # Find the nearest location in A for each point in B
    nearest_indices = argmin(distances, axis=1)
    data["sa2"] = sa2_loc["sa2"].iloc[nearest_indices].values

    geography_hierarchy_definition = read_csv(data_path["deps"]["geography_hierarchy_definition"])

    geography_hierarchy_definition = (
        geography_hierarchy_definition[["SA22018_code", "REGC2023_code"]]
        .drop_duplicates()
        .rename(columns={"SA22018_code": "sa2", "REGC2023_code": "region"})
    )

    merged_df = merge(data, geography_hierarchy_definition, on="sa2", how="left")

    merged_df = merged_df.rename(
        columns={
            "region": "super_area",
            "sa2": "area",
            "source_facility_id": "code",
            "estimated_occupancy": "beds",
        }
    )

    merged_df = merged_df.dropna(subset=["beds"], axis=0, how="any", inplace=False)

    merged_df["icu_beds"] = merged_df["beds"] * FIXED_DATA["group"]["hospital"]["icu_beds_ratio"]

    merged_df["icu_beds"] = merged_df["icu_beds"].astype(int)
    merged_df["beds"] = merged_df["beds"].astype(int)

    merged_df.to_csv(data_path["output"], index=False)

    return {"data": merged_df, "output": data_path["output"]}


def write_workplace_and_home(workdir: str, workplace_and_home_cfg: dict):
    """Write workplace and home commute file

    Args:
        workdir (str): Working directory
        workplace_and_home_cfg (dict): Workplace and home commute configuration
    """

    def _get_required_gender_data(gender_data_path: str) -> DataFrame:
        """Get requred gender data

        Args:
            gender_data_path (str): Gender data path

        Returns:
            DataFrame: Dataframe to be exported
        """
        gender_profile = read_csv(data_path["deps"]["gender_profile"])

        gender_profile = gender_profile[
            ~gender_profile["Area"].str.endswith(("region", "regions", "region/SA2"))
        ]
        gender_profile["Area"] = gender_profile["Area"].apply(
            lambda x: re_findall("\d+", str(x))[0] if re_findall("\d+", str(x)) else None
        )

        gender_profile["Percentage_Male"] = gender_profile["Male"] / (
            gender_profile["Male"] + gender_profile["Female"]
        )

        gender_profile["Percentage_Female"] = gender_profile["Female"] / (
            gender_profile["Male"] + gender_profile["Female"]
        )

        gender_profile = gender_profile[["Area", "Percentage_Male", "Percentage_Female"]]

        return gender_profile

    data_path = get_raw_data(
        workdir,
        workplace_and_home_cfg,
        "workplace_and_home",
        "group/others",
        force=True,
    )

    commute_data = read_csv(data_path["raw"])[
        ["SA2_code_usual_residence_address", "SA2_code_workplace_address", "Total"]
    ]

    gender_profile = _get_required_gender_data(data_path["deps"]["gender_profile"])
    commute_data = commute_data.rename(columns={"SA2_code_usual_residence_address": "Area"})

    gender_profile["Area"] = gender_profile["Area"].astype(str)
    commute_data["Area"] = commute_data["Area"].astype(str)

    merged_df = merge(gender_profile, commute_data, on="Area")

    # Perform the calculations and create new columns
    merged_df["Male"] = merged_df["Percentage_Male"] * merged_df["Total"]
    merged_df["Female"] = merged_df["Percentage_Female"] * merged_df["Total"]

    merged_df["Male"] = merged_df["Male"].astype(int)
    merged_df["Female"] = merged_df["Female"].astype(int)

    # "Area of residence","Area of workplace","All categories: Sex","Male","Female"
    merged_df = merged_df[["Area", "SA2_code_workplace_address", "Total", "Male", "Female"]]

    merged_df = merged_df.rename(
        {
            "Area": "Area of residence",
            "SA2_code_workplace_address": "Area of workplace",
            "Total": "All categories: Sex",
            "Male": "Male",
            "Female": "Female",
        }
    ).astype(int)

    geography_hierarchy_definition = read_csv(
        workplace_and_home_cfg["deps"]["geography_hierarchy_definition"]
    )[["SA22018_code", "REGC2023_code"]].astype(int)
    # "Area of residence","Area of workplace","All categories: Sex","Male","Female"

    mapping_dict = dict(
        zip(
            geography_hierarchy_definition["SA22018_code"],
            geography_hierarchy_definition["REGC2023_code"],
        )
    )

    merged_df["Area"] = merged_df["Area"].map(mapping_dict)
    merged_df["SA2_code_workplace_address"] = merged_df["SA2_code_workplace_address"].map(
        mapping_dict
    )
    merged_df = merged_df.groupby(["Area", "SA2_code_workplace_address"]).sum().reset_index()

    merged_df = merged_df.rename(
        columns={
            "Area": "Area of residence",
            "SA2_code_workplace_address": "Area of workplace",
            "Total": "All categories: Sex",
            "Male": "Male",
            "Female": "Female",
        }
    )

    merged_df.to_csv(data_path["output"], index=False)

    return {"data": merged_df, "output": data_path["output"]}


def write_household_age_difference(workdir: str):
    """Write household age difference for couple and parent-children

    Args:
        workdir (str): Working directory
    """
    for proc_file_key in FIXED_DATA["group"]["household"]:
        proc_data = FIXED_DATA["group"]["household"][proc_file_key]
        data = DataFrame.from_dict(proc_data)
        data.to_csv(join(workdir, "group/household", f"{proc_file_key}.csv"), index=False)


def write_household_number(workdir: str, household_number_cfg: dict):
    """Write household number

    Args:
        workdir (str): Working directory
        household_number_cfg (dict): Household number configuration
    """
    data_path = get_raw_data(
        workdir,
        household_number_cfg,
        "household_number",
        "group/household",
        force=True,
    )

    data = read_csv(data_path["raw"])

    data = data[data["Household composition"] >= 10000]

    data = data.rename(
        columns={
            "Household composition": "output_area",
            "Total households - household composition": ">=0 >=0 >=0 >=0 >=0",
        }
    )

    data.to_csv(data_path["output"], index=False)

    return {"data": data, "output": data_path["output"]}


def write_transport_mode(workdir: str, transport_mode_cfg: dict):
    """Write Transport Model file

    Args:
        workdir (str): Working directory
        transport_mode_cfg (dict): Transport model configuration
    """
    data_path = get_raw_data(
        workdir,
        transport_mode_cfg,
        "transport_mode",
        "group/commute",
        force=True,
    )

    data = read_csv(data_path["raw"])

    # work_from_home_ratio = 0.1

    data = data[
        [
            "SA2_code_usual_residence_address",
            # "SA2_code_workplace_address",
            "Drive_a_private_car_truck_or_van",
            "Drive_a_company_car_truck_or_van",
            "Passenger_in_a_car_truck_van_or_company_bus",
            "Public_bus",
            "Train",
            "Bicycle",
            "Ferry",
            "Other",
            "Total",
        ]
    ]

    data = data.replace(-999.0, 0)

    data = data.groupby("SA2_code_usual_residence_address").sum().reset_index()

    data = data.rename(columns={"SA2_code_usual_residence_address": "geography"})

    for data_key in data.columns:
        if data_key != "geography":
            data = data.rename(
                columns={data_key: f"Method of Travel to Work: {data_key}; measures: Value"}
            )

    data["date"] = 2018
    data["geography code"] = data["geography"]
    data["Rural Urban"] = "Total"

    # Remove rows that there is no travel methods
    travel_methods = [
        x
        for x in list(data.columns)
        if x
        not in [
            "geography",
            "date",
            "geography code",
            "Rural Urban",
            "Method of Travel to Work: Total; measures: Value",
        ]
    ]
    data = data.loc[~((data[travel_methods] == 0).all(axis=1))]

    # Convert all columns from string to integer, except for the Rural Urban
    for column in data.columns:
        if column != "Rural Urban":
            data[column] = data[column].astype(int)

    # data = data.drop(columns=["date", "geography code", "Rural Urban"])

    data.to_csv(data_path["output"], index=False)

    return {"data": data, "output": data_path["output"]}


def write_super_area_name(
    workdir: str, super_area_name_cfg: dict
):
    """Write Super Area name file + number of stations

    Args:
        workdir (str): Working directory
        super_area_name_cfg (dict): Super area name configuration
    """
    data_path = get_raw_data(
        workdir,
        super_area_name_cfg,
        "super_area_name",
        "group/commute",
        force=True,
    )

    data = read_csv(data_path["raw"])

    data = data[["REGC2023_code", "REGC2023_name"]]

    data["REGC2023_name"] = data["REGC2023_name"].str.replace(" Region", "")

    data = data.rename(columns={"REGC2023_code": "super_area", "REGC2023_name": "city"})

    data = data.drop_duplicates()

    data["super_area"] = data["super_area"].astype(str)

    data["city"] = data["city"].replace("Manawatū-Whanganui", "Manawatu-Whanganui")

    data.to_csv(data_path["output"], index=False)

    return {"data": data, "output": data_path["output"]}


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

    return {"data": df_pivot, "output": data_path["output"]}


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

    return {"data": df_pivot, "output": data_path["output"]}


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

    return {"data": df_pivot, "output": data_path["output"]}


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
