import base64
import io
import pandas as pd
from dash import html
import numpy as np
from hktaruma import hk98


def parse_upload_data(content, filename, filedate):
    _, content_string = content.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if filename.endswith(".csv"):
            dataframe = pd.read_csv(
                io.StringIO(decoded.decode("utf-8")), index_col=0, parse_dates=True
            )
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            return (
                html.Div(
                    [
                        "Fitur pembacaan berkas excel masih dalam tahap pengembangan.",
                        " Template yang akan digunakan adalah hidrokit excel template.",
                    ],
                    className="text-center bg-danger text-white fs-4",
                ),
                None,
            )
        else:
            return (
                html.Div(
                    ["Hanya dapat membaca format .csv (tiap kolom merupakan stasiun)"],
                    className="text-center bg-danger text-white fs-4",
                ),
                None,
            )
    except Exception as e:
        print(e)
        return html.Div([f"There was an error processing this file. {e}"]), None

    return html.Div(["File Diterima"]), dataframe


def generate_summary_single(dataframe, n_days="1MS"):
    def days(vector):
        return len(vector)

    def sum(vector):
        return vector.sum().round(3)

    def n_rain(vector):
        return (vector > 0).sum()

    def n_dry(vector):
        return np.logical_or(vector.isna(), vector == 0).sum()

    def max_date(vector):
        if vector.any():
            return vector.idxmax().date()
        else:
            return np.nan

    def max(vector):
        return vector.max()

    ufunc = [days, max, sum, n_rain, n_dry, max_date]
    ufunc_col = ["days", "max", "sum", "n_rain", "n_dry", "max_date"]

    summary = hk98.summary_all(
        dataframe, ufunc=ufunc, ufunc_col=ufunc_col, n_days=n_days
    )

    return summary


def generate_summary_all(dataframe, n_days: list = None):
    n_days = ["16D", "1MS", "1YS"] if n_days is None else n_days

    summary_all = []
    for n_day in n_days:
        summary_all.append(generate_summary_single(dataframe, n_days=n_day))

    return summary_all


def transform_to_dataframe(
    table_data, table_columns, multiindex: bool = False, apply_numeric: bool = True
):

    dataframe = pd.DataFrame(table_data)
    if multiindex is True:
        dataframe.columns = pd.MultiIndex.from_tuples(
            [item["name"] for item in table_columns]
        )
    else:
        dataframe.columns = [item["name"] for item in table_columns]

    dataframe["DATE"] = pd.to_datetime(dataframe.DATE)
    dataframe = dataframe.set_index("DATE").sort_index()

    if apply_numeric is True:
        dataframe = dataframe.apply(pd.to_numeric, errors="coerce")
    else:
        dataframe = dataframe.infer_objects()

    return dataframe
