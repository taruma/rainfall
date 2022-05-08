import plotly.graph_objects as go
import plotly.express as px
import numpy as np


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


TEMPLATE_LABEL = dict(
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
    layout = go.Layout(hovermode="closest", **TEMPLATE_LABEL)

    fig = go.Figure(data, layout)

    return fig


def figure_bar(dataframe, barmode="stack"):

    if barmode == 'stack':
        col_df = dataframe.columns[::-1]
        bargap = 0
    else:
        col_df = dataframe.columns
        bargap = 0.5

    data = [
        go.Bar(
            x=dataframe.index,
            y=dataframe[col],
            name=col,
        )
        for col in col_df
    ]
    layout = go.Layout(hovermode="x unified", barmode=barmode, bargap=bargap, **TEMPLATE_LABEL)

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
