import matplotlib.pyplot as plt
from pandas import read_csv, to_datetime

measles_esr = read_csv("etc/data/measles/measles_esr.csv")
measles_google = read_csv("etc/data/measles/measles_google_trend.csv", header=None, skiprows=1)


measles_esr = measles_esr[measles_esr["Disease"] == "Measles"][["Report Year", "Case Count"]]

measles_google_column_names = measles_google.iloc[0]
measles_google.columns = measles_google_column_names
measles_google = measles_google.reindex(measles_google.index.drop(0)).reset_index(drop=True)
measles_google.columns = ["Time", "Case Count"]
measles_google["Time"] = to_datetime(measles_google["Time"])
measles_google["Year"] = measles_google["Time"].dt.year
measles_google["Case Count"] = measles_google["Case Count"].replace("<1", "0")
measles_google["Case Count"] = measles_google["Case Count"].astype(int)
measles_google = measles_google.groupby("Year")["Case Count"].sum().reset_index()


measles_esr = measles_esr.rename(columns={"Report Year": "year", "Case Count": "case"})
measles_google = measles_google.rename(columns={"Year": "year", "Case Count": "case"})

measles_esr = measles_esr[(measles_esr["year"] >= 2006) & (measles_esr["year"] <= 2021)]
measles_google = measles_google[
    (measles_google["year"] >= 2006) & (measles_google["year"] <= 2021)
]

measles_esr_mean = measles_esr["case"].quantile(0.8)
measles_google_mean = measles_google["case"].quantile(0.8)

scaling_factor = measles_esr_mean / measles_google_mean

measles_google["case"] = measles_google["case"] * scaling_factor

plt.plot(measles_esr["year"], measles_esr["case"], label="ESR reported cases")
plt.plot(measles_google["year"], measles_google["case"], label="Scaled Google search")
plt.legend()
plt.xlabel("Year")
plt.ylabel("Cases")
plt.savefig("test.png")
plt.close()
