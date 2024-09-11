import matplotlib
from jplot.jtyle import *

print('jplot imported!')

def jsubplots(nrows, ncols=None, **kwargs):
    # Calculated size automatically
    if (ncols is None): nrows, ncols = [1, nrows]
    w, h = mpl.rcParams['figure.figsize']
    size = (w*ncols, h*nrows)
    
    params = {}
    params.update({'figsize': size})
    params.update(kwargs)
    
    return plt.subplots(nrows, ncols, **params)

def get_jcolor(name):
    if isinstance(name, str):
        jcolor = COLOR_STYLES[name]
    elif isinstance(name, int):
        jcolor = COLOR_STYLES[COLOR_NAMES[name]]
    else:
        return {}
    return jcolor

def jplot(ax, xdat, ydat, jcolor=None, **kwargs):
    _style = {}
    
    if (not jcolor is None):
        _style.update(get_jcolor(jcolor))
        
    _style.update(kwargs)
        
    return ax.plot(xdat, ydat, **_style)

def jerrbar(ax, xdat, ydat, xerr=None, yerr=None, jcolor=None, **kwargs):
    style = {'ls': 'none', 'marker': 'o'}
    
    if (not jcolor is None):
        style.update(get_jcolor(jcolor))
        # style['ecolor'] = style['mec'] # Set the errorbar color the same with the marker edge color
    style.update(kwargs)
    return ax.errorbar(xdat, ydat, xerr=xerr, yerr=yerr, **style)

def get_marker_cval(cval, crange, cmap):
    # Normalize cval
    crange = (min(cval), max(cval)) if crange=='auto' else crange
    c_min, c_max = crange
    c_norm = (cval - c_min) / (c_max - c_min)

    # Create a colormap instance
    colormap = mpl.cm.get_cmap(cmap) if isinstance(cmap, str) else cmap
    # Generate the colors for each data point
    fc = [colormap(c) for c in c_norm]
    # Calculate face colors with half the lightness in HLS format
    ec = [colorsys.rgb_to_hls(c[0], c[1], c[2]) for c in fc]
    ec = [(h, l / 2, s) for h, l, s in ec]
    ec = [colorsys.hls_to_rgb(h, l, s) for h, l, s in ec]
    
    return fc, ec

def jpscatter(ax, xval, yval, cval, xerr=None, yerr=None, crange='auto', cmap='viridis'):
    # Fill fake error value if not assigned
    xerr = [None]*len(cval) if xerr is None else xerr
    yerr = [None]*len(cval) if yerr is None else yerr
    
    # Get the color map for markers
    fc, ec = get_marker_cval(cval, crange, cmap)
    
    # Global style
    style = {'marker': 'o', 'capsize': None, 'ms':5.}

    # Add error bars with custom colors
    for ii in range(len(xval)):
        color = {'mfc': fc[ii], 'mec': ec[ii], 'ecolor': ec[ii]}
        style.update(color)
        ax.errorbar(xval[ii], yval[ii], xerr=xerr[ii], yerr=yerr[ii], **style)
    
    return
