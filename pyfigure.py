from dash import dcc
from plotly.subplots import make_subplots
from pyconfig import appConfig
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pytemplate
from collections import defaultdict

THRESHOLD_SUMMARY = (367 * 8) // 2
THRESHOLD_GRAPH_RAINFALL = 365 * 8


def _generate_dict_watermark(n: int = 1, source=appConfig.TEMPLATE.WATERMARK_SOURCE):
    n = "" if n == 1 else n
    return dict(
        source=source,
        xref=f"x{n} domain",
        yref=f"y{n} domain",
        x=0.5,
        y=0.5,
        sizex=0.5,
        sizey=0.5,
        xanchor="center",
        yanchor="middle",
        name="watermark-hidrokit",
        layer="below",
        opacity=0.2,
    )


def figure_test_scatter():
    data = [{"x": np.arange(1, 11), "y": np.random.randint(0, 10, 10)}]
    layout = go.Layout()
    return go.Figure(data, layout)


def figure_test_heatmap():
    data = [[1, np.nan, 30, 50, 1], [20, 1, np.nan, 80, 30], [30, 60, np.nan, 5, 20]]
    fig = px.imshow(
        data,
        labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
        x=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        y=["Morning", "Afternoon", "Evening"],
        aspect="auto",
    )
    return fig


def figure_test_heatmap2():
    data = go.Heatmap(z=[[1, 20, 30], [20, np.nan, 60], [30, 60, 1]])
    layout = go.Layout()
    return go.Figure(data, layout)


LABEL_GRAPH_RAINFALL = dict(
    title="<b>Rainfall Each Stations</b>",
    yaxis={"title": "<b>Rainfall (mm)</b>"},
    xaxis={"title": "<b>Date</b>"},
    legend={"title": "Stations"},
)


def figure_scatter(dataframe):

    data = [
        go.Scatter(x=dataframe.index, y=dataframe[col], mode="lines", name=col)
        for col in dataframe.columns
    ]
    layout = go.Layout(hovermode="closest", **LABEL_GRAPH_RAINFALL)

    fig = go.Figure(data, layout)

    return fig


def figure_bar(dataframe, barmode="stack"):

    if barmode == "stack":
        col_df = dataframe.columns[::-1]
        bargap = 0
    else:
        col_df = dataframe.columns
        bargap = 0.2

    data = [
        go.Bar(
            x=dataframe.index,
            y=dataframe[col],
            name=col,
        )
        for col in col_df
    ]
    layout = go.Layout(
        hovermode="x unified", barmode=barmode, bargap=bargap, **LABEL_GRAPH_RAINFALL
    )

    fig = go.Figure(data, layout)

    return fig


def figure_empty():
    data = [{"x": [], "y": []}]
    layout = go.Layout(
        title={"text": "", "x": 0.5},
        xaxis={
            "title": "",
            "showgrid": False,
            "showticklabels": False,
            "zeroline": False,
        },
        yaxis={
            "title": "",
            "showgrid": False,
            "showticklabels": False,
            "zeroline": False,
        },
        margin=dict(t=55, l=55, r=55, b=55),
    )

    return go.Figure(data, layout)


def figure_summary_maxsum(
    summary,
    ufunc_cols: list[str] = None,
    rows: int = 2,
    cols: int = 1,
    subplot_titles: list[str] = None,
    title: str = "Summary Rainfall",
    period: str = None,
) -> dcc.Graph:

    ufunc_cols = ["max", "sum"] if ufunc_cols is None else ufunc_cols
    subplot_titles = ufunc_cols if subplot_titles is None else subplot_titles

    if summary.size > THRESHOLD_SUMMARY:
        return dcc.Graph(figure=figure_empty(), config={"staticPlot": True})

    fig = make_subplots(
        rows=rows,
        cols=cols,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=subplot_titles,
    )

    fig.layout.images = [_generate_dict_watermark(n) for n in range(2, rows + 1)]

    data_dict = defaultdict(list)

    for station in summary.columns.levels[0]:
        for ufcol, series in summary[station].items():
            if ufcol in ufunc_cols:
                _bar = go.Bar(
                    x=np.arange(series.index.size),
                    y=series,
                    name=f"{station} ({ufcol})",
                    legendgroup=station,
                    legendgrouptitle_text=station,
                )
                data_dict[ufcol].append(_bar)

    for counter, (ufcol, data) in enumerate(data_dict.items(), 1):
        fig.add_traces(data, rows=counter, cols=cols)

    fig.update_layout(
        title={"text": title, "pad": {"b": 20}},
        barmode="group",
        hovermode="x",
        height=800,
        xaxis2={"title": "<b>Date</b>"},
        bargap=0.2,
        dragmode="zoom",
        legend={"title": "<b>Stations</b>"},
    )

    ticktext = series.index.strftime("%d %b %Y")

    if period.lower() in ["monthly", "yearly"]:
        if period.lower() == "monthly":
            ticktext = series.index.strftime("%B %Y")
        if period.lower() == "yearly":
            ticktext = series.index.strftime("%Y")

    UPDATE_XAXES = {
        "ticktext": ticktext,
        "tickvals": np.arange(series.index.size),
        "gridcolor": pytemplate._FONT_COLOR_RGB_ALPHA,
        "gridwidth": 2,
    }

    UPDATE_YAXES = {
        "gridcolor": pytemplate._FONT_COLOR_RGB_ALPHA,
        "gridwidth": 2,
        "fixedrange": True,
        "title": "<b>Rainfall (mm)</b>",
    }

    def update_axis(fig, update, n, axis: str = "x"):
        n = "" if n == 1 else n
        fig.update(layout={f"{axis}axis{n}": update})

    for n_row in range(1, rows + 1):
        for axis, update in zip(["x", "y"], [UPDATE_XAXES, UPDATE_YAXES]):
            update_axis(fig, update, n_row, axis)

    # ref: https://stackoverflow.com/questions/39863250
    from itertools import cycle, islice

    n_data = len(fig.data)
    n_split = n_data // 2

    if n_split < len(pytemplate.hktemplate.layout.colorway):
        colors = list(pytemplate.hktemplate.layout.colorway[:n_split])
    else:
        colorway_list = pytemplate.hktemplate.layout.colorway
        colors = list(islice(cycle(colorway_list), n_split))

    for data, color in zip(fig.data, colors * 2):
        data.marker.color = color

    return dcc.Graph(figure=fig)


def figure_summary_raindry(
    summary,
    ufunc_cols: list[str] = None,
    rows: int = None,
    cols: int = 1,
    subplot_titles: list[str] = None,
    title: str = "Summary Rainfall",
    period: str = None,
) -> dcc.Graph:

    rows = summary.columns.levels[0].size if rows is None else rows

    ufunc_cols = ["n_rain", "n_dry"] if ufunc_cols is None else ufunc_cols
    subplot_titles = (
        summary.columns.levels[0] if subplot_titles is None else subplot_titles
    )

    if summary.size > THRESHOLD_SUMMARY:
        return dcc.Graph(figure=figure_empty(), config={"staticPlot": True})

    fig = make_subplots(
        rows=rows,
        cols=cols,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=subplot_titles,
    )

    fig.layout.images = [_generate_dict_watermark(n) for n in range(2, rows + 1)]

    data_dict = defaultdict(list)

    for station in summary.columns.levels[0]:
        for ufcol, series in summary[station].items():
            if ufcol in ufunc_cols:
                _bar = go.Bar(
                    x=np.arange(series.index.size),
                    y=series,
                    name=f"{station} ({ufcol})",
                    legendgroup=station,
                    legendgrouptitle_text=station,
                )
                data_dict[station].append(_bar)

    for counter, (ufcol, data) in enumerate(data_dict.items(), 1):
        fig.add_traces(data, rows=counter, cols=cols)

    fig.update_layout(
        title={"text": title, "pad": {"b": 20}},
        barmode="stack",
        hovermode="x",
        height=max([800, 250 * rows]),
        bargap=0,
        dragmode="zoom",
        legend={"title": "<b>Stations</b>"},
    )

    ticktext = series.index.strftime("%d %b %Y")

    if period.lower() in ["monthly", "yearly"]:
        if period.lower() == "monthly":
            ticktext = series.index.strftime("%B %Y")
        if period.lower() == "yearly":
            ticktext = series.index.strftime("%Y")

    UPDATE_XAXES = {
        "ticktext": ticktext,
        "tickvals": np.arange(series.index.size),
        "gridcolor": pytemplate._FONT_COLOR_RGB_ALPHA,
        "gridwidth": 2,
    }

    UPDATE_YAXES = {
        "gridcolor": pytemplate._FONT_COLOR_RGB_ALPHA,
        "gridwidth": 2,
        "fixedrange": True,
        "title": "<b>Days</b>",
    }

    def update_axis(fig, update, n, axis: str = "x"):
        n = "" if n == 1 else n
        fig.update(layout={f"{axis}axis{n}": update})

    fig.update(layout={f"xaxis{rows}": {"title": "<b>Date</b>"}})

    for n_row in range(1, rows + 1):
        for axis, update in zip(["x", "y"], [UPDATE_XAXES, UPDATE_YAXES]):
            update_axis(fig, update, n_row, axis)

    color_list = pytemplate.hktemplate.layout.colorway[:2]

    for data, color in zip(fig.data, color_list * rows):
        data.marker.color = color

    return dcc.Graph(figure=fig)
