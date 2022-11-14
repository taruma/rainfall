from __future__ import annotations
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from pytemplate import hktemplate
from datetime import datetime
from pyconfig import appConfig


def create_table_layout(
    dataframe,
    idtable,
    filename=None,
    filedate=None,
    editable: list | bool = False,
    deletable=True,
    renamable=False,
):
    from collections.abc import Iterable

    new_dataframe = dataframe.rename_axis("DATE").reset_index()
    new_dataframe.DATE = new_dataframe.DATE.dt.date

    editable = (
        editable
        if isinstance(editable, Iterable)
        else [editable] * len(new_dataframe.columns)
    )

    table = dash_table.DataTable(
        id=idtable,
        columns=[
            {
                "name": i,
                "id": i,
                "deletable": deletable,
                "renamable": renamable,
                "editable": edit_col,
            }
            for i, edit_col in zip(new_dataframe.columns, editable)
        ],
        data=new_dataframe.to_dict("records"),
        page_size=20,
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
    title_table = f"DATA TABLE" + add_title
    return html.H2(title_table, className="text-center"), table


def create_table_summary(
    summary,
    idtable,
    editable=False,
    deletable=True,
    renamable=False,
):
    new_summary = summary.rename_axis("DATE").reset_index()
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
        filter_action="none",
        sort_action="native",
        style_table={"overflowX": "auto"},
        style_cell={"font-family": hktemplate.layout.font.family},
        style_header={"font-size": 20, "textAlign": "center", "font-weight": "bold"},
        merge_duplicate_headers=True,
    )
    return table


def create_tabcard_table_layout(
    tables: list,
    tab_names: list = None,
    disabled: list = None,
    active_tab: str = None,
):

    disabled = [False] * len(tables) if disabled is None else disabled
    tab_names = ["Biweekly", "Monthly", "Yearly"] if tab_names is None else tab_names

    tab = []
    for table, tab_name, active in zip(tables, tab_names, disabled):
        _tab = dbc.Tab(
            dbc.Card(dbc.CardBody([table]), class_name="my-3"),
            label=tab_name,
            disabled=active,
            tab_id=tab_name,
        )
        tab.append(_tab)

    active_tab = tab_names[0] if active_tab is None else active_tab

    return dbc.Tabs(tab, active_tab=active_tab)


def create_tabcard_graph_layout(
    graphs: list[dcc.Graph],
    tab_names: list = None,
    disabled: list = None,
    active_tab: str = None,
):

    disabled = [False] * len(graphs) if disabled is None else disabled
    tab_names = ["Biweekly", "Monthly", "Yearly"] if tab_names is None else tab_names

    tab = []
    for graph, tab_name, active in zip(graphs, tab_names, disabled):
        _tab = dbc.Tab(
            dbc.Card(dbc.CardBody([graph]), class_name="my-3"),
            label=tab_name,
            disabled=active,
            tab_id=tab_name,
        )
        tab.append(_tab)

    active_tab = tab_names[0] if active_tab is None else active_tab

    return dbc.Tabs(tab, active_tab=active_tab)


def create_HTML_alert(alert: dbc.Alert, className: str = "my-2"):
    return html.Div(
        dbc.Container(
            dbc.Row([dbc.Col(alert, width="auto")], justify="center"),
            fluid=True,
        ),
        className=className,
    )
