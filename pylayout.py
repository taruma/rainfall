from dash import html, dcc
import dash_bootstrap_components as dbc
from pyconfig import appConfig
import plotly.io as pio
from pytemplate import hktemplate
import pyfigure

pio.templates.default = hktemplate

HTML_TITLE = html.Div(
    [
        html.H1(
            appConfig.DASH_APP.APP_TITLE,
            className="float fw-bold text-center mt-3 fs-1 fw-bold",
        ),
        html.Span(
            [appConfig.GITHUB_REPO, "@", appConfig.VERSION],
            className="text-muted",
        ),
    ],
    className="text-center",
)

HTML_SUBTITLE = html.P(
    [
        "created by ",
        html.A("taruma", href="https://github.com/taruma"),
        " & powered by ",
        html.A("hidrokit", href="https://github.com/hidrokit"),
    ],
    className="text-center fs-5",
)

ALERT_CONTRIBUTION = dbc.Alert(
    [
        "Tertarik untuk berkontribusi atau ikut bergabung untuk proyek seperti ini? Hubungi saya di ",
        html.A("hi@taruma.info", href="mailto:hi@taruma.info", className="text-bold"),
        ". Atau kunjungi langsung repository proyek ini di ",
        html.A("Github", href=appConfig.GITHUB_LINK),
        ".",
    ]
)

HTML_ALERT = html.Div(
    dbc.Container(
        dbc.Row([dbc.Col(ALERT_CONTRIBUTION, width="auto")], justify="center"),
        fluid=True,
    ),
    className="my-2",
)


DCC_UPLOAD = html.Div(
    dcc.Upload(
        id="dcc-upload",
        children=html.Div(
            [
                dbc.Button(
                    "Drag and Drop or Select Files",
                    color="primary",
                    outline=False,
                    class_name="fs-4 text-center",
                    id="button-upload",
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
                    dbc.Col(
                        [
                            dbc.Button(
                                "Use Example Data",
                                color="info",
                                id="button-skip",
                                class_name="fs-4 text-center",
                            ),
                        ],
                        class_name="fs-4 text-center",
                        width="auto",
                    ),
                ],
                justify="center",
            ),
        ],
        fluid=True,
    ),
)

HTML_ROW_TABLE = html.Div(
    dbc.Container(
        [
            dbc.Card(
                dbc.CardBody(
                    id="row-table-uploaded",
                    children=dcc.Graph(
                        figure=pyfigure.figure_empty(),
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
                                "Download Table As CSV",
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
                    figure=pyfigure.figure_empty(),
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
                # class_name="m-4",
            )
        ],
        fluid=True,
        id="row-download",
        class_name="my-5",
    )
)

HTML_ROW_TABLE_ANALYZE = html.Div(
    dbc.Container(
        dcc.Loading(
            children=dcc.Graph(
                figure=pyfigure.figure_empty(),
                config={"staticPlot": True},
            ),
            id="tab-analyze",
        ),
        fluid=True,
    )
)

_HTML_TROUBLESHOOT = html.Div(
    dbc.Container(
        [
            dbc.Row([html.Div("HEELLOOOO")]),
            dbc.Button("Hello", id="button-troubleshoot"),
            html.Div(id="row-troubleshoot"),
        ],
        fluid=True,
    )
)

HTML_MADEBY = html.Div(
    dcc.Markdown(
        "Made with [Dash+Plotly](https://plotly.com).",
        className="fs-4 text-center mt-5",
    ),
)

HTML_FOOTER = html.Div(
    html.Footer(
        [
            html.Span("\u00A9"),
            " 2022 ",
            html.A(
                "Taruma Sakti Megariansyah",
                href="https://github.com/taruma",
            ),
            ". MIT License. Visit on 👉 ",
            dbc.Badge(
                "Github",
                href=appConfig.GITHUB_LINK,
                color="secondary",
                class_name="text-uppercase fs-6",
                id="tooltip-github",
                target="_blank",
                style={"letter-spacing": "3px", "text-decoration": "none"},
            ),
            dbc.Tooltip(
                "👇 click me 👇", target="tooltip-github", placement="top", autohide=False
            ),
            " 👈.",
        ],
        className="text-center",
    ),
)
