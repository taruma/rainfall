"""TEMPLATE PLOTLY BASED ON THEME"""
import plotly.io as pio
from dash_bootstrap_templates import load_figure_template
from pyconfig import appConfig
from plotly import colors

load_figure_template(appConfig.DASH_THEME.THEME.lower())
hktemplate = pio.templates[pio.templates.default]

# VARS
_TEMPLATE = appConfig.TEMPLATE
_FONT_FAMILY = hktemplate.layout.font.family
_FONT_COLOR_TUPLE = colors.hex_to_rgb(hktemplate.layout.font.color)
_FONT_COLOR_RGB_ALPHA = "rgba({},{},{},0.4)".format(*_FONT_COLOR_TUPLE)

## LAYOUT
# WATERMARK
_SOURCE_WATERMARK = _TEMPLATE.WATERMARK_SOURCE
hktemplate.layout.images = [
    dict(
        source=_SOURCE_WATERMARK,
        xref="x domain",
        yref="y domain",
        x=0.5,
        y=0.5,
        sizex=0.5,
        sizey=0.5,
        xanchor="center",
        yanchor="middle",
        name="watermark-hidrokit",
        layer="below",
        opacity=0.1,
    ),
]

## GENERAL
hktemplate.layout.hovermode = "x"
hktemplate.layout.margin.t = 80
hktemplate.layout.margin.b = 35
hktemplate.layout.margin.l = 55
hktemplate.layout.margin.r = 55
hktemplate.layout.margin.pad = 0
# hktemplate.layout.paper_bgcolor = "rgba(0,0,0,0)"
hktemplate.layout.paper_bgcolor = hktemplate.layout.plot_bgcolor

# LEGEND
_LEGEND_FONT_SIZE = 15
hktemplate.layout.showlegend = True
hktemplate.layout.legend.font.size = _LEGEND_FONT_SIZE
hktemplate.layout.legend.groupclick = "toggleitem"
# hktemplate.layout.legend.title.text = "<b>placeholder</b>"


def apply_legend_inside():
    hktemplate.layout.legend.xanchor = "left"
    hktemplate.layout.legend.yanchor = "top"
    hktemplate.layout.legend.x = 0.005
    hktemplate.layout.legend.y = 0.98
    hktemplate.layout.legend.orientation = "h"
    hktemplate.layout.legend.bordercolor = "black"
    hktemplate.layout.legend.borderwidth = 1
    hktemplate.layout.legend.bgcolor = "rgba(255,255,255,0.6)"


if _TEMPLATE.SHOW_LEGEND_INSIDE:
    apply_legend_inside()

# MODEBAR
hktemplate.layout.modebar.activecolor = "blue"
hktemplate.layout.modebar.add = (
    "hoverclosest hovercompare v1hovermode togglehover drawrect eraseshape".split()
)
# hktemplate.layout.modebar.remove = "toImage"
hktemplate.layout.modebar.bgcolor = "rgba(0,0,0,0)"
hktemplate.layout.modebar.color = "rgba(0,0,0,0.6)"

# NEWSHAPE
hktemplate.layout.newshape.line.color = "red"
hktemplate.layout.newshape.line.width = 3

# HOVERLABEL
hktemplate.layout.hoverlabel.font.family = _FONT_FAMILY

# TITLE
# hktemplate.layout.title.text = "<b>PLACEHOLDER TITLE</b>"
hktemplate.layout.title.pad = dict(b=10, l=0, r=0, t=0)
hktemplate.layout.title.x = 0
hktemplate.layout.title.xref = "paper"
hktemplate.layout.title.y = 1
hktemplate.layout.title.yref = "paper"
hktemplate.layout.title.yanchor = "bottom"
hktemplate.layout.title.font.size = 35

# XAXIS
_XAXIS_GRIDCOLOR = "black"  # hktemplate.layout.xaxis.gridcolor
_XAXIS_LINEWIDTH = 2
_XAXIS_TITLE_FONT_SIZE = 20
_XAXIS_TITLE_STANDOFF = 20
hktemplate.layout.xaxis.mirror = True
hktemplate.layout.xaxis.showline = True
hktemplate.layout.xaxis.linewidth = _XAXIS_LINEWIDTH
hktemplate.layout.xaxis.linecolor = _XAXIS_GRIDCOLOR
hktemplate.layout.xaxis.spikecolor = _XAXIS_GRIDCOLOR
hktemplate.layout.xaxis.gridcolor = _FONT_COLOR_RGB_ALPHA
hktemplate.layout.xaxis.gridwidth = _XAXIS_LINEWIDTH
# hktemplate.layout.xaxis.title.text = "<b>PLACEHOLDER XAXIS</b>"
hktemplate.layout.xaxis.title.font.size = _XAXIS_TITLE_FONT_SIZE
hktemplate.layout.xaxis.title.standoff = _XAXIS_TITLE_STANDOFF

# RANGESELECTOR XAXIS
def apply_rangeselector():
    hktemplate.layout.xaxis.rangeselector.buttons = [
        dict(
            count=1,
            label="1m",
            step="month",
            stepmode="backward",
            visible=True,
            name="button1",
        ),
        dict(
            count=6,
            label="6m",
            step="month",
            stepmode="backward",
            visible=True,
            name="button2",
        ),
        dict(
            count=1,
            label="YTD",
            step="year",
            stepmode="todate",
            visible=True,
            name="button3",
        ),
        dict(
            count=1,
            label="1y",
            step="year",
            stepmode="backward",
            visible=True,
            name="button4",
        ),
        dict(step="all", name="button5"),
    ]


if _TEMPLATE.SHOW_RANGESELECTOR:
    apply_rangeselector()

# YAXIS
_YAXIS_GRIDCOLOR = "black"  # hktemplate.layout.yaxis.gridcolor
_YAXIS_LINEWIDTH = 2
_YAXIS_TITLE_FONT_SIZE = 20
_YAXIS_TITLE_STANDOFF = 15
hktemplate.layout.yaxis.mirror = True
hktemplate.layout.yaxis.showline = True
hktemplate.layout.yaxis.linewidth = _YAXIS_LINEWIDTH
hktemplate.layout.yaxis.linecolor = _YAXIS_GRIDCOLOR
hktemplate.layout.yaxis.spikecolor = _YAXIS_GRIDCOLOR
hktemplate.layout.yaxis.rangemode = "tozero"
hktemplate.layout.yaxis.gridcolor = _FONT_COLOR_RGB_ALPHA
hktemplate.layout.yaxis.gridwidth = _YAXIS_LINEWIDTH
# hktemplate.layout.yaxis.title.text = "<b>PLACEHOLDER XAXIS</b>"
hktemplate.layout.yaxis.title.font.size = _YAXIS_TITLE_FONT_SIZE
hktemplate.layout.yaxis.title.standoff = _YAXIS_TITLE_STANDOFF

# SUBPLOTS
# ANNOTATION
hktemplate.layout.annotationdefaults.font.color = hktemplate.layout.font.color

## PLOT SPECIFIC

# HEATMAP

hktemplate.data.heatmap[0].colorbar.title.text = "placeholder"

# BAR
# hktemplate.data.bar[0].offset = 0
# hktemplate.data.bar[0].marker.color = "red"

# LAYOUT BAR
hktemplate.layout.barmode = "stack"
hktemplate.layout.bargap = 0
