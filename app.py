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

# GLOBAL DATASET
DATAFRAME = None
DF_FILENAME = None
DF_FILEDATE = None

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
    global DATAFRAME, DF_FILENAME, DF_FILEDATE

    ctx = dash.callback_context

    if content is not None:
        DF_FILENAME = filename
        DF_FILEDATE = filedate
        children, DATAFRAME = pyfunc.parse_upload_data(content, filename, filedate)

    if ctx.triggered[0]["prop_id"] == "button-skip.n_clicks":
        DATAFRAME = pd.read_csv(
            Path(r"./example_dataset.csv"), index_col=0, parse_dates=True
        )
        filename = None
        filedate = None

    button_viz_disabled = True
    button_upload_disabled = False
    upload_disabled = False
    button_viz_outline = True

    if DATAFRAME is not None:
        children = pylayout.create_table_layout(
            DATAFRAME,
            "output-table",
            filename=filename,
            filedate=filedate,
            editable=True,
            renamable=True,
        )
        button_viz_disabled = False
        button_upload_disabled = False
        upload_disabled = False
        button_viz_outline = False

    return [
        children,
        upload_disabled,  # upload_disabled,
        button_upload_disabled,  # button_upload_disabled,
        button_viz_disabled,  # button_viz_disabled,
        button_viz_outline,
    ]


@app.callback(
    [
        Output("section-graph", "figure"),
        Output("visibility-download-button", "style"),
        Output("section-graph", "config"),
        Output("container-graphbar-options", "style"),
        Output("button-analyze", "disabled"),
    ],
    Input("button-visualize", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    State("graph-bar-options", "value"),
    prevent_initial_call=True,
)
def callback_visualize(_, table_data, table_columns, graphbar_opt):
    global DATAFRAME

    DATAFRAME = pyfunc.transform_to_dataframe(table_data, table_columns)

    download_row_visible = {"visibility": "visible"}
    static_plot_enabled = {"staticPlot": False}
    row_graphbar_visibile = {"visibility": "hidden"}
    button_analyze_disabled = False

    if DATAFRAME.size > (366 * 8):
        fig = pyfigure.figure_scatter(DATAFRAME)
    else:
        row_graphbar_visibile = {"visibility": "visible"}
        if graphbar_opt in ["group", "stack"]:
            fig = pyfigure.figure_bar(DATAFRAME, graphbar_opt)
        else:
            fig = pyfigure.figure_scatter(DATAFRAME)

    return [
        fig,
        download_row_visible,
        static_plot_enabled,
        row_graphbar_visibile,
        button_analyze_disabled,
    ]


@app.callback(
    Output("download-csv", "data"),
    Input("button-download-csv", "n_clicks"),
    prevent_initial_call=True,
)
def callback_download(_):
    return dcc.send_data_frame(DATAFRAME.to_csv, "derived_table.csv")


@app.callback(
    Output("col-table-analyze", "children"),
    Input("button-analyze", "n_clicks"),
    State("output-table", "derived_virtual_data"),
    State("output-table", "columns"),
    prevent_initial_call=True,
)
def callback_analyze(n_clicks, table_data, table_columns):
    global DATAFRAME

    DATAFRAME = pyfunc.transform_to_dataframe(table_data, table_columns)
    summary_all = pyfunc.generate_summary_all(DATAFRAME, n_days=["16D", "MS", "YS"])

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
