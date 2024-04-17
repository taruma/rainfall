"""
This module contains functions for parsing and processing uploaded data, 
    generating summary statistics for rainfall data, 
    transforming table data into a pandas DataFrame, 
    and calculating the cumulative sum of a DataFrame.
"""

import base64
import io
import pandas as pd
from dash import html
import numpy as np
from hidrokit.contrib.taruma import statistic_summary


def parse_upload_data(content, filename, filedate):
    """
    Parse and process uploaded data.

    Args:
        content (str): The content of the uploaded file.
        filename (str): The name of the uploaded file.
        filedate (str): The date of the uploaded file.

    Returns:
        tuple: A tuple containing the processed data and an HTML element.
            The processed data is a pandas DataFrame if the file is in CSV format.
            If the file is in XLSX or XLS format, an HTML element with a warning message
                is returned.
            If the file is in any other format, an HTML element with an error message
                is returned.
    """

    _ = filedate  # unused variable
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
    except UnicodeDecodeError as e:
        print(e)
        return html.Div([f"File is not valid UTF-8. {e}"]), None
    except pd.errors.ParserError as e:
        print(e)
        return html.Div([f"CSV file is not well-formed. {e}"]), None
    except ValueError as e:
        print(e)
        return html.Div([f"Content string is not valid base64. {e}"]), None

    return html.Div(["File Diterima"]), dataframe


def generate_summary_single(dataframe, n_days="1MS"):
    """
    Generate a summary of rainfall data for a single location.

    Args:
        dataframe (pandas.DataFrame): The input dataframe containing rainfall data.
        n_days (str, optional): The number of days to consider for the summary.
            Defaults to "1MS".

    Returns:
        pandas.DataFrame: The summary dataframe containing various statistics of
            the rainfall data.
    """

    def days(vector):
        return len(vector)

    def vector_sum(vector):
        return vector.sum().round(3)

    def n_rain(vector):
        return (vector > 0).sum()

    def n_dry(vector):
        return np.logical_or(vector.isna(), vector == 0).sum()

    def max_date(vector):
        if vector.any():
            return vector.idxmax().date()
        return pd.NaT

    def vector_max(vector):
        return vector.max()

    ufunc = [days, vector_max, vector_sum, n_rain, n_dry, max_date]
    ufunc_col = ["days", "max", "sum", "n_rain", "n_dry", "max_date"]

    summary = statistic_summary.summary_all(
        dataframe, ufunc=ufunc, ufunc_col=ufunc_col, n_days=n_days
    )

    return summary.infer_objects()


def generate_summary_all(dataframe, n_days: list = None):
    """
    Generate summary statistics for multiple time periods.

    Args:
        dataframe (pandas.DataFrame): The input dataframe containing the data.
        n_days (list, optional): A list of time periods to calculate
            the summary statistics for.
            If not provided, the default time periods ["16D", "1MS", "1YS"] will be used.

    Returns:
        list: A list of summary statistics for each time period.

    """
    n_days = ["16D", "1MS", "1YS"] if n_days is None else n_days

    summary_all = []
    for n_day in n_days:
        summary_all.append(generate_summary_single(dataframe, n_days=n_day))

    return summary_all


def transform_to_dataframe(
    table_data,
    table_columns,
    multiindex: bool = False,
    apply_numeric: bool = True,
    parse_dates: list = None,
):
    """
    Transform table data into a pandas DataFrame.

    Args:
        table_data (list): The data to be transformed into a DataFrame.
        table_columns (list): The column names of the table data.
        multiindex (bool, optional): Whether to create a multi-index DataFrame.
            Defaults to False.
        apply_numeric (bool, optional): Whether to apply numeric conversion to the DataFrame.
            Defaults to True.
        parse_dates (list, optional): The column names to parse as dates.
            Defaults to None.

    Returns:
        pandas.DataFrame: The transformed DataFrame.
    """

    if multiindex is True:
        dataframe = pd.DataFrame(table_data)
        dataframe.columns = pd.MultiIndex.from_tuples(
            [item["name"] for item in table_columns]
        )
    else:
        columns = pd.Index([item["name"] for item in table_columns])
        dataframe = pd.DataFrame(table_data, columns=columns)

    dataframe["DATE"] = pd.to_datetime(dataframe.DATE)
    dataframe = dataframe.set_index("DATE").sort_index()

    if multiindex is True:
        # removing date (index.name) from top level multiindex
        dataframe.columns = pd.MultiIndex.from_tuples(dataframe.columns.to_flat_index())

    if apply_numeric is True:
        dataframe = dataframe.apply(pd.to_numeric, errors="coerce")
    else:
        dataframe = dataframe.infer_objects()

    if parse_dates is not None:
        if multiindex:
            for col_dates in parse_dates:
                col_parsing = [
                    col_tuple
                    for col_tuple in dataframe.columns
                    if col_dates in col_tuple
                ]
                for col_dates in col_parsing:
                    dataframe[col_dates] = pd.to_datetime(
                        dataframe[col_dates], errors="coerce"
                    )
        else:
            for col_dates in parse_dates:
                dataframe[col_dates] = pd.to_datetime(
                    dataframe[col_dates], errors="coerce"
                )

    return dataframe


def calculate_cumulative_sum(dataframe):
    """
    Calculate the cumulative sum of a DataFrame by resampling it on a yearly basis.

    Parameters:
    dataframe (pandas.DataFrame): The input DataFrame containing the data.

    Returns:
    pandas.DataFrame: The DataFrame with the cumulative sum rounded to the nearest integer.
    """
    consistency = dataframe.resample("YS").sum().cumsum()

    return consistency.round()
