import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import pyfigure, pyfunc, pylayout, pylayoutfunc
from dash import dcc, html, Input, Output, State
from pathlib import Path
from pyconfig import appConfig
from pytemplate import hktemplate

pio.templates.default = hktemplate

# DASH APP CONFIG
APP_TITLE = appConfig.DASH_APP.APP_TITLE
UPDATE_TITLE = appConfig.DASH_APP.UPDATE_TITLE
DEBUG = appConfig.DASH_APP.DEBUG

# BOOTSRAP THEME
THEME = appConfig.DASH_THEME.THEME
dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
)

# GLOBAL VARS
SUMMARY_ALL = None

# APP
app = dash.Dash(
    APP_TITLE,
    external_stylesheets=[getattr(dbc.themes, THEME), dbc_css],
    title=APP_TITLE,
    update_title=UPDATE_TITLE,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
    suppress_callback_exceptions=True,
)
server = app.server

app.layout = dbc.Container(
    [
        pylayout.HTML_TITLE,
        pylayout.HTML_SUBTITLE,
        pylayout.HTML_ALERT_README,
        pylayout.HTML_ROW_BUTTON_UPLOAD,
        pylayout.HTML_ROW_TABLE,
        pylayout.HTML_ROW_BUTTON_VIZ,
        pylayout.HTML_ROW_OPTIONS_GRAPH_RAINFALL,
        pylayout.HTML_ROW_GRAPH_ONE,
        pylayout.HTML_ROW_BUTTON_ANALYZE,
        pylayout.HTML_ROW_TABLE_ANALYZE,
        pylayout.HTML_ROW_BUTTON_VIZ_ANALYSIS,
        pylayout.HTML_ROW_GRAPH_ANALYSIS,
        pylayout.HTML_ALERT_CONTRIBUTION,
        pylayout.HTML_MADEBY,
        pylayout.HTML_OTHER_PROJECTS,
        pylayout.HTML_FOOTER,
    ],
    fluid=True,
    className="dbc",
)


@app.callback(
    [
        Output("row-table-uploaded", "children"),
        Output("dcc-upload", "disabled"),
        Output("button-upload", "disabled"),
        Output("button-visualize", "disabled"),
        Output("button-visualize", "outline"),
    ],
    Input("dcc-upload", "contents"),
    State("dcc-upload", "filename"),
    State("dcc-upload", "last_modified"),
    Input("button-skip", "n_clicks"),
    prevent_initial_call=True,
)
def callback_upload(content, filename, filedate, _):
    ctx = dash.callback_context

    if content is not None:
        children, dataframe = pyfunc.parse_upload_data(content, filename, filedate)

    if ctx.triggered[0]["prop_id"] == "button-skip.n_clicks":
        dataframe = pd.read_csv(
            Path(r"./example_1Y7S.csv"), index_col=0, parse_dates=True
        )
        filename = None
        filedate = None

    upload_disabled = False
    button_upload_disabled = False
    button_viz_disabled = True
    button_viz_outline = True

    if dataframe is not None:
        children = pylayoutfunc.create_table_layout(
            dataframe,
            "output-table",
            filename=filename,
            filedate=filedate,
            editable=True,
            renamable=True,
        )
        upload_disabled = False
        button_upload_disabled = False
        button_viz_disabled = False
        button_viz_outline = False

    return [
        children,
        upload_disabled,
        button_upload_disabled,
        button_viz_disabled,
        button_viz_outline,
    ]


@app.callback(
    [
        Output("graph-rainfall", "figure"),
        Output("row-button-download-csv", "style"),
        Output("graph-rainfall", "config"),
        Output("container-graphbar-options", "style"),
        Output("button-analyze", "disabled"),
        Output("button-analyze", "outline"),
    ],
    Input("button-visualize", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    State("radio-graphbar-options", "value"),
    prevent_initial_call=True,
)
def callback_visualize(_, table_data, table_columns, graphbar_opt):
    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

    row_download_table_style = {"visibility": "visible"}
    row_graph_config = {"staticPlot": False}
    row_graphbar_options_style = {"visibility": "hidden"}
    button_analyze_disabled = False
    button_analyze_outline = False

    if dataframe.size > (366 * 8):
        fig = pyfigure.figure_scatter(dataframe)
    else:
        row_graphbar_options_style = {"visibility": "visible"}
        if graphbar_opt in ["group", "stack"]:
            fig = pyfigure.figure_bar(dataframe, graphbar_opt)
        else:
            fig = pyfigure.figure_scatter(dataframe)

    return [
        fig,
        row_download_table_style,
        row_graph_config,
        row_graphbar_options_style,
        button_analyze_disabled,
        button_analyze_outline,
    ]


@app.callback(
    Output("download-csv", "data"),
    Input("button-download-csv", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    prevent_initial_call=True,
)
def callback_download_table(_, table_data, table_columns):
    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)
    return dcc.send_data_frame(dataframe.to_csv, "derived_table.csv")


@app.callback(
    [
        Output("tab-analysis", "children"),
        Output("button-viz-analysis", "disabled"),
        Output("button-viz-analysis", "outline"),
        Output("row-button-download-analysis-csv", "style"),
    ],
    Input("button-analyze", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    prevent_initial_call=True,
)
def callback_analyze(_, table_data, table_columns):
    global SUMMARY_ALL

    button_viz_analysis_disabled = True
    button_viz_analysis_outline = True
    row_button_download_analysis_style = {"visibility": "hidden"}

    try:
        dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)
        SUMMARY_ALL = pyfunc.generate_summary_all(dataframe, n_days=["16D", "MS", "YS"])
        tables = [
            pylayoutfunc.create_table_summary(
                summary, f"table-analyze-{counter}", deletable=False
            )
            for counter, summary in enumerate(SUMMARY_ALL)
        ]

        children = pylayoutfunc.create_tabcard_table_layout(tables)
        button_viz_analysis_disabled = False
        button_viz_analysis_outline = False
        row_button_download_analysis_style = {"visibility": "visible"}
    except Exception as e:
        children = html.Div(f"SOMETHING ERROR {e}")

    return [
        children,
        button_viz_analysis_disabled,
        button_viz_analysis_outline,
        row_button_download_analysis_style,
    ]


@app.callback(
    Output("download-analysis-csv", "data"),
    Input("button-download-analysis-csv", "n_clicks"),
    prevent_initial_call=True,
)
def callback_download_results(_):

    dataframe = pd.concat(SUMMARY_ALL, axis=1, keys=["Biweekly", "Monthly", "Yearly"])
    return dcc.send_data_frame(dataframe.to_csv, "results.csv")


@app.callback(
    Output("tab-graph-analysis", "children"),
    Input("button-viz-analysis", "n_clicks"),
    prevent_initial_call=True,
)
def callback_troubleshoot(_):
    from itertools import product

    label_periods = ["Biweekly", "Monthly", "Yearly"]
    label_maxsum = ["Max + Sum"]
    label_raindry = ["Dry + Rain"]
    label_ufunc = label_maxsum + label_raindry

    graphs_maxsum = [
        pyfigure.figure_summary_maxsum(
            summary, title=f"<b>{period}: {title}</b>", period=period
        )
        for summary, title, period in zip(SUMMARY_ALL, label_maxsum * 3, label_periods)
    ]
    graphs_raindry = [
        pyfigure.figure_summary_raindry(
            summary, title=f"<b>{period}: {title}</b>", period=period
        )
        for summary, title, period in zip(SUMMARY_ALL, label_raindry * 3, label_periods)
    ]
    graph_maxdate = [pyfigure.figure_summary_maxdate(SUMMARY_ALL)]

    all_graphs = graphs_maxsum + graphs_raindry + graph_maxdate
    labels = [": ".join(i) for i in product(label_ufunc, label_periods)]
    labels += ["Maximum Rainfall Occurrence"]

    children = pylayoutfunc.create_tabcard_graph_layout(all_graphs, labels)

    return children


@app.callback(
    Output("row-troubleshoot", "children"),
    Input("button-troubleshoot", "n_clicks"),
    prevent_initial_call=True,
)
def _callback_troubleshoot(_):
    return html.Div("troubleshoot")


if __name__ == "__main__":
    app.run_server(debug=DEBUG)
