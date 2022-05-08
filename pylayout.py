from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from pyconfig import appConfig
from pytemplate import hktemplate
from datetime import datetime
import pyfigure


def create_table_layout(
    dataframe,
    idtable,
    filename=None,
    filedate=None,
    editable=False,
    deletable=True,
    renamable=False,
):
    new_dataframe = dataframe.reset_index()
    new_dataframe.DATE = new_dataframe.DATE.dt.date
    table = dash_table.DataTable(
        id=idtable,
        columns=[
            {"name": i, "id": i, "deletable": deletable, "renamable": renamable}
            for i in new_dataframe.columns
        ],
        data=new_dataframe.to_dict("records"),
        page_size=20,
        editable=editable,
        cell_selectable=True,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
        style_cell={"font-family": hktemplate.layout.font.family},
        style_header={"font-size": 20, "textAlign": "center", "font-weight": "bold"},
    )
    add_title = (
        f' ({filename}:{datetime.fromtimestamp(filedate).strftime("%Y-%m-%d")})'
        if (filename is not None) and (filedate is not None)
        else ""
    )
    title_table = f"TABEL DATA" + add_title
    return html.H2(title_table, className="text-center"), table


def create_table_summary(
    summary,
    idtable,
    editable=False,
    deletable=True,
    renamable=False,
):
    new_summary = summary.reset_index()
    new_summary.DATE = new_summary.DATE.dt.date

    flatten_index = new_summary.columns.to_flat_index()
    new_id = ["_".join(colx) if colx[1] != "" else colx[0] for colx in flatten_index]
    new_summary.columns = new_id

    table = dash_table.DataTable(
        id=idtable,
        columns=[
            {"name": name, "id": id, "deletable": deletable, "renamable": renamable}
            for name, id in zip(flatten_index, new_id)
        ],
        data=new_summary.to_dict("records"),
        page_size=20,
        editable=editable,
        cell_selectable=True,
        filter_action="native",
        sort_action="native",
        style_table={"overflowX": "auto"},
        style_cell={"font-family": hktemplate.layout.font.family},
        style_header={"font-size": 20, "textAlign": "center", "font-weight": "bold"},
        merge_duplicate_headers=True,
    )
    return table


def create_tabcard_layout(tables: list, tab_names: list = None, disabled: list = None):

    disabled = [False] * len(tables) if disabled is None else disabled
    tab_names = ["Biweekly", "Monthly", "Yearly"] if tab_names is None else tab_names

    tab = []
    for table, tab_name, active in zip(tables, tab_names, disabled):
        _tab = dbc.Tab(
            dbc.Card(dbc.CardBody([table]), class_name="my-3"), label=tab_name
        )
        tab.append(_tab)

    return dbc.Tabs(tab)


HTML_TITLE = html.Div(
    [
        html.H1(
            appConfig.DASH_APP.APP_TITLE,
            className="float fw-bold text-center mt-3 fs-1 fw-bold",
        ),
        html.Span(
            [appConfig.GITHUB_REPO, "@", appConfig.VERSION],
            # href=appConfig.GITHUB_LINK,
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
        id="upload-data",
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
        class_name="",
    ),
)

HTML_ROW_TABLE = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            dbc.Card(
                                dbc.CardBody(
                                    id="output-data-upload",
                                    children=dcc.Graph(
                                        figure=pyfigure.figure_empty(),
                                        config={"staticPlot": True},
                                    ),
                                ),
                            )
                        ),
                        class_name="",
                    ),
                ],
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
                        [
                            dbc.Button(
                                "Visualize Data",
                                color="success",
                                outline=True,
                                class_name="fs-4 text-center fw-bold",
                                id="button-visualize",
                                disabled=True,
                            ),
                        ],
                        width="auto",
                    ),
                    dbc.Col(
                        [
                            dbc.Button(
                                [
                                    "Download Table As CSV",
                                ],
                                color="primary",
                                className="me-1 fs-4",
                                id="button-download-csv",
                            ),
                            dcc.Download(id="download-csv"),
                        ],
                        width="auto",
                        style={"visibility": "hidden"},
                        id="visibility-download-button",
                    ),
                ],
                justify="center",
                class_name="m-3",
            )
        ],
        class_name="mt-5",
    )
)

HTML_ROW_OPTIONS_GRAPH_RAINFALL = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label("Small Dataset Options:"),
                            dbc.RadioItems(
                                options=[
                                    {"label": "Stack", "value": "stack"},
                                    {"label": "Group", "value": "group"},
                                    {"label": "Line", "value": "line"},
                                ],
                                value="stack",
                                id="graph-bar-options",
                                inline=True,
                            ),
                        ],
                        width="auto",
                    )
                ],
                justify="center",
                class_name="",
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
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            dcc.Graph(
                                id="section-graph",
                                figure=pyfigure.figure_empty(),
                                config={"staticPlot": True},
                            )
                        )
                    )
                ],
                justify="center",
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
                class_name="m-4",
            )
        ],
        fluid=True,
        id="row-download",
    )
)

HTML_ROW_TABLE_ANALYZE = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            html.Div(
                                children=dcc.Graph(
                                    figure=pyfigure.figure_empty(),
                                    config={"staticPlot": True},
                                ),
                                id="col-table-analyze",
                            ),
                        ),
                    )
                ],
                justify="center",
            )
        ],
        fluid=True,
    )
)

# HTML_ROW_TABLE_ANALYZE = html.Div(dbc.Container(["EMPTY"], id="col-table-analyze"))

HTML_MADEBY = html.Div(
    dcc.Markdown(
        "made with [Dash+Plotly](https://plotly.com)".lower(),
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
