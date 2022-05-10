from dash import dcc
from plotly.subplots import make_subplots
from pyconfig import appConfig
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pytemplate
import pandas as pd
from collections import defaultdict
from itertools import cycle, islice

THRESHOLD_SUMMARY = (367 * 8) // 2
THRESHOLD_GRAPH_RAINFALL = 365 * 8
THRESHOLD_XAXES = 12 * 2 * 5
THRESHOLD_STATIONS = 8


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


def figure_empty(text: str = "", size: int = 40):
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
        annotations=[
            dict(
                name="text",
                text=f"<i>{text}</i>",
                opacity=0.3,
                font_size=size,
                xref="x domain",
                yref="y domain",
                x=0.5,
                y=0.05,
                showarrow=False,
            )
        ],
        height=450,
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
        return dcc.Graph(
            figure=figure_empty("dataset above threshold"), config={"staticPlot": True}
        )

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

    if series.index.size <= THRESHOLD_XAXES:
        xticktext = ticktext
        xtickvals = np.arange(series.index.size)
    else:
        xticktext = ticktext[::2]
        xtickvals = np.arange(series.index.size)[::2]

    UPDATE_XAXES = {
        "ticktext": xticktext,
        "tickvals": xtickvals,
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
    summary: pd.DataFrame,
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

    if (summary.size > THRESHOLD_SUMMARY) or (summary.index.size > THRESHOLD_XAXES):
        return dcc.Graph(
            figure=figure_empty("dataset above threshold"), config={"staticPlot": True}
        )

    vertical_spacing = 0.2 / rows

    fig = make_subplots(
        rows=rows,
        cols=cols,
        shared_xaxes=True,
        vertical_spacing=vertical_spacing,
        subplot_titles=subplot_titles,
    )

    fig.layout.images = [_generate_dict_watermark(n) for n in range(2, rows + 1)]

    for station in summary.columns.levels[0]:
        summary[(station, "n_left")] = (
            summary[(station, "days")].max()
            - summary[(station, "n_rain")]
            - summary[(station, "n_dry")]
        )

    data_dict = defaultdict(list)

    for station in summary.columns.levels[0]:
        for ufcol, series in summary[station].items():
            if ufcol in ufunc_cols + ["n_left"]:
                if ufcol in ufunc_cols:
                    _bar = go.Bar(
                        x=np.arange(series.index.size),
                        y=series,
                        name=f"{station} ({ufcol})",
                        legendgroup=station,
                        legendgrouptitle_text=station,
                        marker_line_width=0,
                        customdata=series.index,
                        hovertemplate=f"{station}<br>{ufcol}: %{{y}}<extra></extra>",
                    )
                    data_dict[station].append(_bar)
                if ufcol == "n_left":
                    _bar = go.Bar(
                        x=np.arange(series.index.size),
                        y=series,
                        name=f"<i>{station} (border)</i>",
                        legendgroup=station,
                        legendgrouptitle_text=station,
                        showlegend=True,
                        hoverinfo="skip",
                        marker_line_width=0,
                        marker_opacity=1,
                        legendrank=500,
                    )
                    data_dict[station].append(_bar)

    for counter, (ufcol, data) in enumerate(data_dict.items(), 1):
        fig.add_traces(data, rows=counter, cols=cols)

    fig.update_layout(
        title={"text": title, "pad": {"b": 20}},
        barmode="stack",
        hovermode="x",
        height=max([600, 250 * rows]),
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

    if series.index.size <= THRESHOLD_XAXES:
        xticktext = ticktext
        xtickvals = np.arange(series.index.size)
    else:
        xticktext = ticktext[::2]
        xtickvals = np.arange(series.index.size)[::2]

    UPDATE_XAXES = {
        "ticktext": xticktext,
        "tickvals": xtickvals,
        "gridcolor": pytemplate._FONT_COLOR_RGB_ALPHA.replace("0.4", "0.1"),
        "gridwidth": 2,
        # "nticks": 2,
        "ticklabelstep": 2,
    }

    UPDATE_YAXES = {
        "gridcolor": pytemplate._FONT_COLOR_RGB_ALPHA,
        "gridwidth": 2,
        "fixedrange": True,
        "title": "<b>Days</b>",
        "range": [0, summary[(station, "days")].max()],
    }

    def update_axis(fig, update, n, axis: str = "x"):
        n = "" if n == 1 else n
        fig.update(layout={f"{axis}axis{n}": update})

    fig.update(layout={f"xaxis{rows}": {"title": "<b>Date</b>"}})

    for n_row in range(1, rows + 1):
        for axis, update in zip(["x", "y"], [UPDATE_XAXES, UPDATE_YAXES]):
            update_axis(fig, update, n_row, axis)

    color_list = list(pytemplate.hktemplate.layout.colorway[:2]) + ["DarkGray"]

    for data, color in zip(fig.data, color_list * rows):
        data.marker.color = color

    return dcc.Graph(figure=fig)


def figure_summary_maxdate(
    summary_all: pd.DataFrame,
    ufunc_col: list[str] = None,
    rows: int = 3,
    cols: int = 1,
    subplot_titles: list[str] = None,
    title: str = "Maximum Rainfall Occurrence",
    periods: list[str] = None,
    bubble_sizes: list[int] = None,
):

    if summary_all[0].size > THRESHOLD_SUMMARY:
        return dcc.Graph(
            figure=figure_empty("dataset above threshold"), config={"staticPlot": True}
        )

    ufunc_col = ["max_date"] if ufunc_col is None else ufunc_col
    subplot_titles = (
        ["Biweekly", "Monthly", "Yearly"] if subplot_titles is None else subplot_titles
    )
    periods = ["biweekly", "monthly", "yearly"] if periods is None else periods

    fig = make_subplots(
        rows=rows,
        cols=cols,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=subplot_titles,
    )

    fig.layout.images = [_generate_dict_watermark(n) for n in range(2, rows + 1)]

    # Create new DF

    all_stat = []
    for summary, period in zip(summary_all, periods):
        for station in summary.columns.levels[0]:
            _max = summary[station].dropna(subset=ufunc_col)
            _max["max_date"] = pd.to_datetime(_max["max_date"])
            _max = _max.set_index("max_date")[["max"]]
            _max.columns = pd.MultiIndex.from_tuples([(period, station)])
            all_stat.append(_max)

    all_df = pd.concat(all_stat, axis=1)

    bubble_sizes = [8, 9, 10] if bubble_sizes is None else bubble_sizes

    data_dict = defaultdict(list)
    for period, bubble_size in zip(all_df.columns.levels[0], bubble_sizes):
        sizeref = 2.0 * all_df[period].max().max() / (bubble_size**2)
        for station, series in all_df[period].items():
            yvals = series.where(~series.notna(), station)
            _scatter = go.Scatter(
                x=series.index,
                y=yvals,
                mode="markers",
                marker_size=series.fillna(0),
                marker_sizeref=sizeref,
                legendgroup=station,
                legendgrouptitle_text=station,
                name=f"{period}",
                hovertemplate="<i>%{y}</i><br>%{customdata[0]}<br>%{customdata[1]} mm<extra></extra>",
                customdata=np.stack(
                    [
                        series.index.strftime("%d %B %Y"),
                        series.to_numpy(),
                    ],
                    axis=-1,
                ),
            )
            data_dict[period].append(_scatter)

    for counter, (period, data) in enumerate(data_dict.items(), 1):
        fig.add_traces(data, rows=counter, cols=cols)

    fig.update_layout(
        title_text=title,
        title_pad_b=20,
        height=1000,
        dragmode="zoom",
        legend_title="<b>Stations</b>",
        legend_itemsizing="constant",
        hovermode="closest",
    )

    def update_axis(fig, update, n, axis: str = "x"):
        n = "" if n == 1 else n
        fig.update(layout={f"{axis}axis{n}": update})

    # XAXES

    fig.update(layout={f"xaxis{rows}": {"title": "<b>Date</b>"}})

    # GENERAL UPDATE
    UPDATE_XAXES = {
        "gridcolor": pytemplate._FONT_COLOR_RGB_ALPHA.replace("0.4", "0.1"),
        "gridwidth": 2,
    }
    UPDATE_YAXES = {
        "gridcolor": pytemplate._FONT_COLOR_RGB_ALPHA.replace("0.4", "0.1"),
        "gridwidth": 2,
        "fixedrange": True,
        "title": "<b>Station</b>",
    }

    for n_row in range(1, rows + 1):
        for axis, update in zip(["x", "y"], [UPDATE_XAXES, UPDATE_YAXES]):
            update_axis(fig, update, n_row, axis)

    n_data = len(fig.data)
    n_split = n_data // 3

    if n_split < len(pytemplate.hktemplate.layout.colorway):
        colors = list(pytemplate.hktemplate.layout.colorway[:n_split])
    else:
        colorway_list = pytemplate.hktemplate.layout.colorway
        colors = list(islice(cycle(colorway_list), n_split))

    for data, color in zip(fig.data, colors * 3):
        data.marker.color = color

    return dcc.Graph(figure=fig)
