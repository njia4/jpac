import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import rgb_to_hsv, hex2color
from cycler import cycler
# from jcolor import jcolor

##################################################
###                Color Scheme                ###
##################################################
# A set of color combination found by Nathan Schine
COLOR_CODES = {
    "reds"              : ['#fee5d9', '#fcae91', '#fb6a4a', '#de2d26', '#a50f15'], 
    "yelloworangereds"  : ['#ffffb2', '#fecc5c', '#fd8d3c', '#f03b20', '#bd0026'], 
    "purplereds"        : ['#f1eef6', '#d7b5d8', '#df65b0', '#dd1c77', '#980043'], 
    "bluepurples"       : ['#edf8fb', '#b3cde3', '#8c96c6', '#8856a7', '#810f7c'], 
    "redpurples"        : ['#feebe2', '#fbb4b9', '#f768a1', '#c51b8a', '#7a0177'], 
    "purples"           : ['#f2f0f7', '#cbc9e2', '#9e9ac8', '#756bb1', '#54278f'], 
    "yellowgreenblues"  : ['#ffffcc', '#a1dab4', '#41b6c4', '#2c7fb8', '#253494'], 
    "blues"             : ['#eff3ff', '#bdd7e7', '#6baed6', '#3182bd', '#08519c'], 
    "greenblues"        : ['#f0f9e8', '#bae4bc', '#7bccc4', '#43a2ca', '#0868ac'], 
    "purpleblues"       : ['#f1eef6', '#bdc9e1', '#74a9cf', '#2b8cbe', '#045a8d'], 
    "purplebluegreens"  : ['#f6eff7', '#bdc9e1', '#67a9cf', '#1c9099', '#016c59'], 
    "bluegreens"        : ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837'], 
    "yellowgreens"      : ['#ffffcc', '#c2e699', '#78c679', '#31a354', '#006837'], 
    "greens"            : ['#edf8e9', '#bae4b3', '#74c476', '#31a354', '#006d2c'], 
    "yelloworangebrowns": ['#ffffd4', '#fed98e', '#fe9929', '#d95f0e', '#993404'], 
    "oranges"           : ['#feedde', '#fdbe85', '#fd8d3c', '#e6550d', '#a63603'], 
    "orangereds"        : ['#fef0d9', '#fdcc8a', '#fc8d59', '#e34a33', '#b30000'], 
    "greys"             : ['#f7f7f7', '#cccccc', '#969696', '#636363', '#252525'], 
}
COLOR_NAMES = list(COLOR_CODES.keys())

# Color names sorted by hue
COLOR_NAME_SORT_HUE = sorted(COLOR_NAMES, key=lambda x: -rgb_to_hsv(hex2color(COLOR_CODES[x][-1]))[0])

# Custom plotting style using these colors
COLOR_STYLES = {k: {'color': v[2], 'mfc': v[1], 'mec': v[4]} for k, v in COLOR_CODES.items()}

# Manually ordered color to have best distinguishability between two plots
COLOR_NAME_SORT_CONTRAST = ['reds', 'blues', 'greens', 'purplereds', 'greys', 'greenblues', 'yelloworangebrowns', 'yellowgreens', 'redpurples', 'oranges']
CYCLER_CONTRAST = cycler(color=[COLOR_CODES[n][2] for n in COLOR_NAME_SORT_CONTRAST]) \
                + cycler(mfc=[COLOR_CODES[n][1] for n in COLOR_NAME_SORT_CONTRAST]) \
                + cycler(mec=[COLOR_CODES[n][4] for n in COLOR_NAME_SORT_CONTRAST])

#################################################
###             RC Params Presets             ###
#################################################
# Utility function to use the preset
def set_rcParams(params):
    for _key in params.keys(): mpl.rcParams[_key] = params[_key]

# Good for daily plot using Jupyter. The size is choosen for OneNote. 
JPLOT_RCPARAMS_JUPYTER = {
    'lines.linewidth'              : .9          , # Line widht of the line plot. Also the error bar width. 
    'lines.markersize'             : 5           , 
    'lines.markeredgewidth'        : 1.          ,
    'errorbar.capsize'             : 0.          ,
    'image.aspect'                 : 'auto'      , # It sets the aspect ratio to be the same as the axes
    'image.origin'                 : 'lower'     , # Put the (0, 0) at the bottom left (instead of the top left). 
    'figure.constrained_layout.use': True        , # Figure constrained_layout
    'figure.figsize'               : [2.5, 2.5]  ,
    'figure.dpi'                   : 120         ,
    'axes.prop_cycle'              : CYCLER_CONTRAST , # Color and style cycler
    'savefig.bbox'                 : 'tight'     , # Default saving
}

JPLOT_RCPARAMS_NATURE = {
    'figure.figsize'               : [3, 3]
}
