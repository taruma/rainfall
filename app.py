"""Main Dash App for Rainfall Analysis"""

from itertools import product
from pathlib import Path
from dash import dcc, html, Input, Output, State
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import plotly.io as pio
from pyconfig import appConfig
from pytemplate import hktemplate
import pyfigure, pyfunc, pylayout, pylayoutfunc  # pylint: disable=multiple-imports

pio.templates.default = hktemplate

# DASH APP CONFIG
APP_TITLE = appConfig.DASH_APP.APP_TITLE
UPDATE_TITLE = appConfig.DASH_APP.UPDATE_TITLE
DEBUG = appConfig.DASH_APP.DEBUG

# BOOTSRAP THEME
THEME = appConfig.DASH_THEME.THEME
DBC_CSS = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.1.2/dbc.min.css"
)

# APP
app = dash.Dash(
    APP_TITLE,
    external_stylesheets=[getattr(dbc.themes, THEME), DBC_CSS],
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
        pylayout.HTML_ALERT_README,
        pylayout.HTML_ROW_BUTTON_UPLOAD,
        pylayout.HTML_ROW_BUTTON_EXAMPLE,
        pylayout.HTML_ROW_TABLE,
        pylayout.HTML_ROW_BUTTON_VIZ,
        pylayout.HTML_ROW_OPTIONS_GRAPH_RAINFALL,
        pylayout.HTML_ROW_GRAPH_ONE,
        pylayout.HTML_ROW_BUTTON_ANALYZE,
        pylayout.HTML_ROW_TABLE_ANALYZE,
        pylayout.HTML_ROW_BUTTON_VIZ_ANALYSIS,
        pylayout.HTML_ROW_GRAPH_ANALYSIS,
        pylayout.HTML_ROW_GRAPH_CUMSUM,
        pylayout.HTML_ROW_GRAPH_CONSISTENCY,
        html.Hr(),
        pylayout.HTML_SUBTITLE,
        pylayout.HTML_FOOTER,
    ],
    fluid=False,
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
    Input("button-example-1", "n_clicks"),
    Input("button-example-2", "n_clicks"),
    Input("button-example-3", "n_clicks"),
    Input("button-example-4", "n_clicks"),
    prevent_initial_call=True,
)
def callback_upload(content, filename, filedate, _b1, _b2, _b3, _b4):
    """Callback for uploading data and displaying the table."""

    ctx = dash.callback_context

    if content is not None:
        children, dataframe = pyfunc.parse_upload_data(content, filename, filedate)

    example_data = {
        "button-example-1.n_clicks": r"./example_7Y5S.csv",
        "button-example-2.n_clicks": r"./example_2Y4S_named.csv",
        "button-example-3.n_clicks": r"./example_9Y1S_named.csv",
        "button-example-4.n_clicks": r"./example_1Y7S_named.csv",
    }

    context_trigger_prop_id = ctx.triggered[0]["prop_id"]

    if context_trigger_prop_id in example_data:
        example_file = example_data[context_trigger_prop_id]
        dataframe = pd.read_csv(Path(example_file), index_col=0, parse_dates=True)
        filename = None
        filedate = None

    upload_disabled = False
    button_upload_disabled = False
    button_viz_disabled = True
    button_viz_outline = True

    if dataframe is not None:
        editable = [False] + [True] * len(dataframe.columns)
        children = pylayoutfunc.create_table_layout(
            dataframe,
            "output-table",
            filename=filename,
            filedate=filedate,
            editable=editable,
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
    """Callback for visualizing the rainfall data."""

    dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

    row_download_table_style = {"visibility": "visible"}
    row_graph_config = {"staticPlot": False}
    row_graphbar_options_style = {"visibility": "hidden"}
    button_analyze_disabled = False
    button_analyze_outline = False

    if dataframe.size > (366 * 8):
        fig = pyfigure.generate_scatter_figure(dataframe)
    else:
        row_graphbar_options_style = {"visibility": "visible"}
        if graphbar_opt in ["group", "stack"]:
            fig = pyfigure.generate_bar_figure(dataframe, graphbar_opt)
        else:
            fig = pyfigure.generate_scatter_figure(dataframe)

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
    """Callback for downloading the table data."""
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
    """Callback for analyzing the rainfall data."""

    button_viz_analysis_disabled = True
    button_viz_analysis_outline = True
    row_button_download_analysis_style = {"visibility": "hidden"}

    try:
        dataframe = pyfunc.transform_to_dataframe(table_data, table_columns)

        # SUMMARY
        summary_all = pyfunc.generate_summary_all(dataframe, n_days=["16D", "MS", "YS"])
        tables_summary = [
            pylayoutfunc.create_table_summary(
                summary, f"table-analyze-{counter}", deletable=False
            )
            for counter, summary in enumerate(summary_all)
        ]

        # CUMUMLATIVE SUM
        cumsum = pyfunc.calculate_cumulative_sum(dataframe)

        _, table_cumsum = pylayoutfunc.create_table_layout(
            cumsum, "table-cumsum", deletable=False
        )

        table_cumsum = [table_cumsum]

        # LAYOUT
        tables_all = tables_summary + table_cumsum
        tab_names = "Biweekly Monthly Yearly Cumulative".split()

        children = pylayoutfunc.create_tabcard_table_layout(
            tables_all, tab_names=tab_names
        )

        button_viz_analysis_disabled = False
        button_viz_analysis_outline = False
        row_button_download_analysis_style = {"visibility": "visible"}
    except (TypeError, ValueError) as e:
        children = html.Div(
            f"Input data or columns are not in the expected format: {e}"
        )
    except KeyError as e:
        children = html.Div(f"Dataframe does not have the expected columns: {e}")

    return [
        children,
        button_viz_analysis_disabled,
        button_viz_analysis_outline,
        row_button_download_analysis_style,
    ]


@app.callback(
    Output("download-analysis-csv", "data"),
    Input("button-download-analysis-csv", "n_clicks"),
    State("table-analyze-0", "data"),
    State("table-analyze-0", "columns"),
    State("table-analyze-1", "data"),
    State("table-analyze-1", "columns"),
    State("table-analyze-2", "data"),
    State("table-analyze-2", "columns"),
    State("table-cumsum", "data"),
    State("table-cumsum", "columns"),
    prevent_initial_call=True,
)
def callback_download_results(
    _,
    biweekly_data,
    biweekly_columns,
    monthly_data,
    monthly_columns,
    yearly_data,
    yearly_columns,
    cumsum_data,
    cumsum_columns,
):
    """Callback for downloading the analysis results."""

    biweekly = (biweekly_data, biweekly_columns)
    monthly = (monthly_data, monthly_columns)
    yearly = (yearly_data, yearly_columns)

    summary_all = []
    for period in (biweekly, monthly, yearly):
        data, columns = period
        dataframe = pyfunc.transform_to_dataframe(
            data,
            columns,
            multiindex=True,
            apply_numeric=False,
            parse_dates=["max_date"],
        )
        summary_all.append(dataframe)

    cumsum = pyfunc.transform_to_dataframe(cumsum_data, cumsum_columns)
    stations = cumsum.columns.to_list()
    cumsum.columns = pd.MultiIndex.from_product([stations, [""]])

    dataframe_all = pd.concat(
        summary_all + [cumsum],
        axis=1,
        keys=["Biweekly", "Monthly", "Yearly", "Cumulative"],
    )

    return dcc.send_data_frame(dataframe_all.to_csv, "results.csv")


@app.callback(
    Output("tab-graph-analysis", "children"),
    Output("tab-graph-cumsum", "children"),
    Output("tab-graph-consistency", "children"),
    Input("button-viz-analysis", "n_clicks"),
    State("table-analyze-0", "data"),
    State("table-analyze-0", "columns"),
    State("table-analyze-1", "data"),
    State("table-analyze-1", "columns"),
    State("table-analyze-2", "data"),
    State("table-analyze-2", "columns"),
    State("table-cumsum", "data"),
    State("table-cumsum", "columns"),
    prevent_initial_call=True,
)
def callback_graph_analysis(
    _,
    biweekly_data,
    biweekly_columns,
    monthly_data,
    monthly_columns,
    yearly_data,
    yearly_columns,
    cumsum_data,
    cumsum_columns,
):
    """Callback for generating the analysis graphs."""

    label_periods = ["Biweekly", "Monthly", "Yearly"]
    label_maxsum = ["Max + Sum"]
    label_raindry = ["Dry + Rain"]
    label_ufunc = label_maxsum + label_raindry

    biweekly = (biweekly_data, biweekly_columns)
    monthly = (monthly_data, monthly_columns)
    yearly = (yearly_data, yearly_columns)

    summary_all = []
    for summary_period in (biweekly, monthly, yearly):
        data, columns = summary_period
        dataframe = pyfunc.transform_to_dataframe(
            data,
            columns,
            multiindex=True,
            apply_numeric=False,
            parse_dates=["max_date"],
        )
        summary_all.append(dataframe)

    graphs_maxsum = [
        pyfigure.generate_summary_maximum_sum(
            summary,
            title=f"<b>{period}: {title}</b>",
            period=period,
            subplot_titles=["Max", "Sum"],
        )
        for summary, title, period in zip(summary_all, label_maxsum * 3, label_periods)
    ]
    graphs_raindry = [
        pyfigure.generate_summary_rain_dry(
            summary, title=f"<b>{period}: {title}</b>", period=period
        )
        for summary, title, period in zip(summary_all, label_raindry * 3, label_periods)
    ]
    graph_maxdate = [pyfigure.generate_summary_maximum_date(summary_all)]

    all_graphs = graphs_maxsum + graphs_raindry + graph_maxdate
    labels = [": ".join(i) for i in product(label_ufunc, label_periods)]
    labels += ["Maximum Rainfall Events"]

    children_analysis = pylayoutfunc.create_tabcard_graph_layout(
        all_graphs, labels, active_tab="Maximum Rainfall Events"
    )

    # CUMSUM

    cumsum = pyfunc.transform_to_dataframe(cumsum_data, cumsum_columns)

    graph_cumsum = [
        pyfigure.generate_cumulative_sum(cumsum, data_column=station)
        for station in cumsum.columns
    ]

    children_cumsum = pylayoutfunc.create_tabcard_graph_layout(
        graph_cumsum, cumsum.columns
    )

    # CONSISTENCY

    if cumsum.columns.size == 1:
        children_consistency = (
            dcc.Graph(
                figure=pyfigure.generate_empty_figure(
                    text="Not Available for Single Station"
                ),
                config={"staticPlot": True},
            ),
        )
    else:
        graph_consistency = [
            pyfigure.generate_scatter_with_trendline(cumsum, data_column=station)
            for station in cumsum.columns
        ]

        children_consistency = pylayoutfunc.create_tabcard_graph_layout(
            graph_consistency, cumsum.columns
        )

    return children_analysis, children_cumsum, children_consistency


if __name__ == "__main__":
    app.run_server(debug=DEBUG)
