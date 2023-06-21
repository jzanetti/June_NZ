from datetime import datetime
from logging import getLogger
from os import makedirs
from os.path import exists, join

from matplotlib.pyplot import (
    close,
    savefig,
    subplots,
    suptitle,
    tight_layout,
    title,
    ylim,
)
from pandas import DataFrame

from process.diags.utils import get_area_name

logger = getLogger()


def plot_equity_again_symptoms(
    workdir: str,
    df_people: DataFrame,
    areas_or_super_areas: list,
    area_type: str,  # super_area or area
    geotable: DataFrame or None = None,
    symptoms: list = [["hospitalised"], ["hospitalised", "dead_hospital"]],
    equity_elements: list = ["sex", "age", "ethnicity"],
):
    fig_dir = join(workdir, "equity")

    if not exists(fig_dir):
        makedirs(fig_dir)

    for i, proc_area in enumerate(areas_or_super_areas):
        logger.info(
            f"Creating vis (equity): {proc_area} ... ({round(100.0 * (float(i)/float(len(areas_or_super_areas))), 2)}%)"
        )

        proc_area_data = df_people.loc[df_people[f"{area_type}_name"] == proc_area]

        area_name = get_area_name(area_type, proc_area, geotable=geotable)

        for proc_symptom in symptoms:
            proc_df = proc_area_data[proc_area_data["symptoms"].isin(proc_symptom)]

            for proc_equity_element in equity_elements:
                proc_df2 = proc_df[["id", proc_equity_element]]

                proc_df2_no_duplicates = proc_df2.drop_duplicates()

                proc_df2_no_duplicates[proc_equity_element].value_counts().plot(
                    y=proc_equity_element, kind="pie", legend=False, ylabel=""
                )

                title(f"{proc_equity_element}, {area_name}\n{', '.join(proc_symptom)}")

                tight_layout()

                savefig(
                    join(
                        fig_dir,
                        f"{proc_area}_equity_{'-'.join(proc_symptom)}_{proc_equity_element}.png",
                    ),
                    bbox_inches="tight",
                )
                close()
