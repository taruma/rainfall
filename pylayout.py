"""
This module defines the layout components for a Dash application used for rainfall analysis.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.io as pio
from pyconfig import appConfig
from pytemplate import hktemplate
import pyfigure
import pylayoutfunc

pio.templates.default = hktemplate

HTML_TITLE = html.Div(
    [
        html.H1(
            appConfig.DASH_APP.APP_TITLE,
            className="float fw-bold text-center mt-3 fs-1 fw-bold",
        ),
        html.Span(
            html.A(
                [appConfig.GITHUB_REPO, "@", appConfig.VERSION],
                href="https://github.com/taruma/rainfall",
                target="_blank",
            ),
            className="text-muted",
        ),
    ],
    className="text-center",
)

HTML_SUBTITLE = html.Div(
    [
        "created by ",
        html.A("taruma", href="https://github.com/taruma"),
        " & powered by ",
        html.A("hidrokit", href="https://github.com/hidrokit/hidrokit"),
    ],
    className="text-center fs-5",
)

ALERT_README = dbc.Alert(
    [
        "Rainfall Data Explorer (hidrokit-rainfall) is a web application for "
        "analyzing daily rainfall data, providing maximum rainfall, total rainfall, "
        "rainy days, dry days, and maximum rainfall events visualization, "
        "with added features like annual cumulative graph and consistency (mass curve)",
        ".",
    ],
    color="warning",
    className="m-4",
)

HTML_ALERT_README = pylayoutfunc.create_html_alert(ALERT_README, class_name=None)

DCC_UPLOAD = html.Div(
    dcc.Upload(
        id="dcc-upload",
        children=html.Div(
            [
                dbc.Button(
                    "Upload File (.csv)",
                    color="primary",
                    outline=False,
                    class_name="fs-4 text-center",
                    id="button-upload",
                    size="lg",
                )
            ]
        ),
        multiple=False,
        disable_click=False,
    ),
)

HTML_ROW_BUTTON_UPLOAD = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [DCC_UPLOAD],
                        width="auto",
                    ),
                ],
                justify="center",
            ),
        ],
        fluid=True,
    ),
)

HTML_ROW_BUTTON_EXAMPLE = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Button(
                                "Example 1 (5 Stations, 7 Years)",
                                color="success",
                                id="button-example-1",
                                class_name="text-center",
                                size="sm",
                            ),
                        ],
                        class_name="text-center",
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            dbc.Button(
                                "Example 2 (4 Stations, 2 Years)",
                                color="success",
                                id="button-example-2",
                                class_name="text-center",
                                size="sm",
                            ),
                        ],
                        class_name="text-center",
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            dbc.Button(
                                "Example 3 (1 Station, 9 Years)",
                                color="success",
                                id="button-example-3",
                                class_name="text-center",
                                size="sm",
                            ),
                        ],
                        class_name="text-center",
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            dbc.Button(
                                "Example 4 (7 Station, 1 Years)",
                                color="success",
                                id="button-example-4",
                                class_name="text-center",
                                size="sm",
                            ),
                        ],
                        class_name="text-center",
                        width="auto",
                    ),
                ],
                justify="center",
                class_name="my-3",
            ),
        ],
        fluid=True,
    )
)

HTML_ROW_TABLE = html.Div(
    dbc.Container(
        [
            dbc.Card(
                dbc.CardBody(
                    id="row-table-uploaded",
                    children=dcc.Graph(
                        figure=pyfigure.generate_empty_figure(),
                        config={"staticPlot": True},
                    ),
                ),
            ),
        ],
        fluid=True,
        class_name="my-3",
    )
)

HTML_ROW_BUTTON_VIZ = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            "Visualize Data",
                            color="success",
                            outline=True,
                            class_name="fs-4 fw-bold",
                            id="button-visualize",
                            disabled=True,
                        ),
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            dbc.Button(
                                "Download Table as CSV",
                                color="primary",
                                className="fs-4",
                                id="button-download-csv",
                            ),
                            dcc.Download(id="download-csv"),
                        ],
                        width="auto",
                        style={"visibility": "hidden"},
                        id="row-button-download-csv",
                    ),
                ],
                justify="center",
            )
        ],
        class_name="my-4",
    )
)

HTML_ROW_OPTIONS_GRAPH_RAINFALL = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label("Small Dataset (<= 2,920 data points) Options:"),
                            dbc.RadioItems(
                                options=[
                                    {"label": "Stack", "value": "stack"},
                                    {"label": "Group", "value": "group"},
                                    {"label": "Line", "value": "line"},
                                ],
                                value="stack",
                                id="radio-graphbar-options",
                                inline=True,
                            ),
                        ],
                        width="auto",
                    )
                ],
                justify="center",
            )
        ],
        fluid=True,
        style={"visibility": "hidden"},
        id="container-graphbar-options",
    )
)

HTML_ROW_GRAPH_ONE = html.Div(
    dbc.Container(
        [
            dcc.Loading(
                dcc.Graph(
                    id="graph-rainfall",
                    figure=pyfigure.generate_empty_figure(),
                    config={"staticPlot": True},
                )
            )
        ],
        fluid=True,
    )
)


HTML_ROW_BUTTON_ANALYZE = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Button(
                                [
                                    "Analyze Data",
                                ],
                                color="warning",
                                className="me-1 fs-4",
                                outline=True,
                                id="button-analyze",
                                disabled=True,
                            ),
                        ],
                        width="auto",
                    )
                ],
                justify="center",
            )
        ],
        fluid=True,
        class_name="my-5",
    )
)

HTML_ROW_TABLE_ANALYZE = html.Div(
    dbc.Container(
        dcc.Loading(
            children=dcc.Graph(
                figure=pyfigure.generate_empty_figure(),
                config={"staticPlot": True},
            ),
            id="tab-analysis",
        ),
        fluid=True,
    )
)

HTML_ROW_BUTTON_VIZ_ANALYSIS = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Button(
                                [
                                    "Visualize it!",
                                ],
                                color="danger",
                                className="me-1 fs-4",
                                outline=True,
                                id="button-viz-analysis",
                                disabled=True,
                            ),
                        ],
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            dbc.Button(
                                "Download Results as CSV",
                                color="primary",
                                className="fs-4",
                                id="button-download-analysis-csv",
                            ),
                            dcc.Download(id="download-analysis-csv"),
                        ],
                        width="auto",
                        style={"visibility": "hidden"},
                        id="row-button-download-analysis-csv",
                    ),
                ],
                justify="center",
            )
        ],
        fluid=True,
        class_name="my-5",
    )
)

HTML_ROW_GRAPH_ANALYSIS = html.Div(
    dbc.Container(
        dcc.Loading(
            children=dcc.Graph(
                figure=pyfigure.generate_empty_figure(),
                config={"staticPlot": True},
            ),
            id="tab-graph-analysis",
        ),
        fluid=True,
    ),
    className="my-3",
)

HTML_ROW_GRAPH_CUMSUM = html.Div(
    dbc.Container(
        [
            html.H3("Total Cumulative Annual", className="text-center"),
            dbc.Row(
                dbc.Col(
                    dcc.Loading(
                        children=dcc.Graph(
                            figure=pyfigure.generate_empty_figure(),
                            config={"staticPlot": True},
                        ),
                        id="tab-graph-cumsum",
                    ),
                    width={"size": 6, "offset": 3},
                ),
            ),
        ],
        fluid=True,
    ),
    className="my-3",
)

HTML_ROW_GRAPH_CONSISTENCY = html.Div(
    dbc.Container(
        [
            html.H3("Consistency (Double Mass Curve)", className="text-center"),
            dbc.Row(
                dbc.Col(
                    dcc.Loading(
                        children=dcc.Graph(
                            figure=pyfigure.generate_empty_figure(),
                            config={"staticPlot": True},
                        ),
                        id="tab-graph-consistency",
                    ),
                    width={"size": 6, "offset": 3},
                ),
            ),
        ],
        fluid=True,
    ),
    className="my-3",
)

HTML_FOOTER = html.Div(
    html.Footer(
        [
            html.Span("\u00A9"),
            " 2022-2024 ",
            html.A(
                "Taruma Sakti Megariansyah",
                href="https://dev.taruma.info",
                target="_blank",
            ),
            ". MIT License. Visit on ",
            html.A(
                "Github",
                href=appConfig.GITHUB_LINK,
            ),
            ".",
        ],
        className="text-center my-2",
    ),
)
