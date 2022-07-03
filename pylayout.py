from dash import html, dcc
import dash_bootstrap_components as dbc
from pyconfig import appConfig
import plotly.io as pio
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
            [appConfig.GITHUB_REPO, "@", appConfig.VERSION],
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

HTML_SPONSORED = html.Div(
    [
        "sponsored by ",
        html.A("FIAKO Engineering", href="https://fiako.engineering"),
    ],
    className="text-center fs-5 mb-3",
)

ALERT_CONTRIBUTION = dbc.Alert(
    [
        "Tertarik untuk berkontribusi? Ingin terlibat proyek hidrokit seperti ini? hubungi saya di ",
        html.A("hi@taruma.info", href="mailto:hi@taruma.info", className="text-bold"),
        ". Langsung buat isu di ",
        html.A("Github", href=appConfig.GITHUB_LINK),
        " jika memiliki pertanyaan/komentar/kritik/saran atau menemui kesalahan di proyek ini.",
    ]
)

HTML_ALERT_CONTRIBUTION = pylayoutfunc.create_HTML_alert(ALERT_CONTRIBUTION)

ALERT_README = dbc.Alert(
    [
        "Informasi aplikasi ini dapat dilihat di ",
        html.A(
            "GitHub README",
            href="https://github.com/fiakoenjiniring/rainfall#readme",
        ),
        ".",
    ],
    color="warning",
    className="m-4",
)

HTML_ALERT_README = pylayoutfunc.create_HTML_alert(ALERT_README, className=None)

ALERT_SPONSOR = dbc.Alert(
    [
        "Terima kasih untuk ",
        html.A(
            "FIAKO Engineering",
            href="https://fiako.engineering",
        ),
        " yang telah mensponsori versi v1.1.0. Untuk catatan pembaruan bisa dilihat melalui ",
        html.A(
            "halaman rilis di github",
            href="https://github.com/fiakoenjiniring/rainfall/releases/tag/v1.1.0",
        ),
        ".",
    ],
    color="info",
)

HTML_ALERT_SPONSOR = pylayoutfunc.create_HTML_alert(ALERT_SPONSOR, className=None)


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
                figure=pyfigure.figure_empty(),
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
                figure=pyfigure.figure_empty(),
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
                            figure=pyfigure.figure_empty(),
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
                            figure=pyfigure.figure_empty(),
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

HTML_OTHER_PROJECTS = html.Div(
    [
        html.Span("other dashboard:"),
        html.A(
            [
                html.Del("BMKG", style={"text-decoration-style": "double"}),
                " 🛖 Explorer",
            ],
            href="https://github.com/taruma/dash-data-explorer",
            style={"text-decoration": "none"},
        ),
    ],
    className="d-flex gap-2 justify-content-center my-2",
)

HTML_MADEBY = html.Div(
    dcc.Markdown(
        "Made with [Dash+Plotly](https://plotly.com).",
        className="fs-4 text-center mt-2",
    ),
)

HTML_FOOTER = html.Div(
    html.Footer(
        [
            html.Span("\u00A9"),
            " 2022 ",
            # html.A(
            #     "Taruma Sakti Megariansyah",
            #     href="https://github.com/taruma",
            # ),
            # ", ",
            html.A(
              "PT. FIAKO ENJINIRING INDONESIA",
              href="https://fiako.engineering",
              target="_blank"
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
