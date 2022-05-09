import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.io as pio
import pyfigure
import pyfunc
import pylayout
from dash import dcc, Input, Output, State
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
        pylayout.HTML_ALERT,
        pylayout.HTML_ROW_BUTTON_UPLOAD,
        pylayout.HTML_ROW_TABLE,
        pylayout.HTML_ROW_BUTTON_VIZ,
        pylayout.HTML_ROW_OPTIONS_GRAPH_RAINFALL,
        pylayout.HTML_ROW_GRAPH_ONE,
        pylayout.HTML_ROW_BUTTON_ANALYZE,
        pylayout.HTML_ROW_TABLE_ANALYZE,
        pylayout.HTML_MADEBY,
        pylayout.HTML_FOOTER,
    ],
    fluid=True,
    className="dbc",
)


@app.callback(
    [
        Output("output-data-upload", "children"),
        Output("upload-data", "disabled"),
        Output("button-upload", "disabled"),
        Output("button-visualize", "disabled"),
        Output("button-visualize", "outline"),
    ],
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
    Input("button-skip", "n_clicks"),
    prevent_initial_call=True,
)
def callback_upload(content, filename, filedate, _):
    ctx = dash.callback_context

    if content is not None:
        children, dataframe = pyfunc.parse_upload_data(content, filename, filedate)

    if ctx.triggered[0]["prop_id"] == "button-skip.n_clicks":
        dataframe = pd.read_csv(
            Path(r"./example_dataset.csv"), index_col=0, parse_dates=True
        )
        filename = None
        filedate = None

    upload_disabled = False
    button_upload_disabled = False
    button_viz_disabled = True
    button_viz_outline = True

    if dataframe is not None:
        children = pylayout.create_table_layout(
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
        Output("section-graph", "figure"),
        Output("visibility-download-button", "style"),
        Output("section-graph", "config"),
        Output("container-graphbar-options", "style"),
        Output("button-analyze", "disabled"),
        Output("button-analyze", "outline"),
    ],
    Input("button-visualize", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    State("graph-bar-options", "value"),
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
    Output("col-table-analyze", "children"),
    Input("button-analyze", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    prevent_initial_call=True,
)
def callback_analyze(_, table_data, table_columns):
    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

    summary_all = pyfunc.generate_summary_all(dataframe, n_days=["16D", "MS", "YS"])
    tables = [
        pylayout.create_table_summary(
            summary, f"table-analyze-{counter}", deletable=False
        )
        for counter, summary in enumerate(summary_all)
    ]

    children = pylayout.create_tabcard_layout(tables)

    return children


if __name__ == "__main__":
    app.run_server(debug=DEBUG)
