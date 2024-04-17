"""
This module contains functions for creating table and graph layouts 
    using Dash and Bootstrap components.
"""

from collections.abc import Iterable
from datetime import datetime
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from pytemplate import hktemplate


def create_table_layout(
    dataframe,
    idtable,
    filename=None,
    filedate=None,
    editable: list | bool = False,
    deletable=True,
    renamable=False,
):
    """
    Create a table layout using the given dataframe.

    Args:
        dataframe (pandas.DataFrame): The input dataframe.
        idtable (str): The ID of the DataTable component.
        filename (str, optional): The name of the file. Defaults to None.
        filedate (int, optional): The timestamp of the file. Defaults to None.
        editable (list or bool, optional): A list of booleans indicating
            the editability of each column,
            or a single boolean value to be applied to all columns. Defaults to False.
        deletable (bool, optional): Whether the columns are deletable. Defaults to True.
        renamable (bool, optional): Whether the columns are renamable. Defaults to False.

    Returns:
        tuple: A tuple containing the title element and the DataTable component.
    """

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
    title_table = "DATA TABLE" + add_title
    return html.H2(title_table, className="text-center"), table


def create_table_summary(
    summary,
    idtable,
    editable=False,
    deletable=True,
    renamable=False,
):
    """
    Creates a table summary using the provided summary data.

    Args:
        summary (pandas.DataFrame): The summary data to be displayed in the table.
        idtable (str): The ID of the DataTable component.
        editable (bool, optional): Specifies whether the table cells are editable.
            Defaults to False.
        deletable (bool, optional): Specifies whether the table columns are deletable.
            Defaults to True.
        renamable (bool, optional): Specifies whether the table columns are renamable.
            Defaults to False.

    Returns:
        dash_table.DataTable: The created DataTable component.
    """

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
    """
    Create a tabbed card layout with tables.

    Args:
        tables (list): A list of tables to be displayed in each tab.
        tab_names (list, optional): A list of tab names.
            Defaults to ["Biweekly", "Monthly", "Yearly"].
        disabled (list, optional): A list of booleans indicating whether each tab is disabled.
            Defaults to None.
        active_tab (str, optional): The active tab. Defaults to None.

    Returns:
        dbc.Tabs: A tabbed card layout with the specified tables and settings.
    """

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
    """
    Create a layout with tab cards containing graphs.

    Args:
        graphs (list[dcc.Graph]): A list of Dash Core Component Graph objects.
        tab_names (list, optional): A list of tab names.
            Defaults to ["Biweekly", "Monthly", "Yearly"].
        disabled (list, optional): A list of boolean values indicating whether
            each tab is disabled. Defaults to None.
        active_tab (str, optional): The ID of the active tab. Defaults to None.

    Returns:
        dbc.Tabs: A Dash Bootstrap Components Tabs object containing tab cards with graphs.
    """

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


def create_html_alert(alert: dbc.Alert, class_name: str = "my-2"):
    """
    Creates an HTML alert container with the specified alert component and class name.

    Parameters:
        alert (dbc.Alert): The alert component to be displayed.
        className (str, optional): The class name to be applied to the alert container. 
            Defaults to "my-2".

    Returns:
        html.Div: The HTML alert container.

    """
    return html.Div(
        dbc.Container(
            dbc.Row([dbc.Col(alert, width="auto")], justify="center"),
            fluid=True,
        ),
        className=class_name,
    )
