import re
import numpy
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

def sort_index(l, ascending=True):
    index = [i[0] for i in sorted(enumerate(l), key=lambda x:x[1])]
    return index if ascending else index[::-1]

def nsort( l ):
    """
    Sort the given list in the way that humans expect. For example,

    >>> l = ["1", "4", "2" , "0"]
    >>> natural(l)
    >>> l
    ['0', '1', '2', '4']

    Note that negative values (its argument takes only string!) is shifted to the backward

    >>> l = ["-1","3","-2", "4"]
    >>> natural(l)
    >>> l
    ['3', '4', '-1', '-2']

    """
    ll = l[:]
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    ll.sort( key=alphanum_key )
    return ll

def hsm_axes(fig,nfm=False):
    nullfmt   = NullFormatter()         # no labels

    pad = 0.05  if nfm else 0.02

    left, width = 0.1, 0.5
    bottom, height = 0.1, 0.5
    bottom_h = left_h = left+width+pad

    rect_hsm= [left, bottom, width, height]
    rect_qrep = [left, bottom_h, width, 0.3]
    rect_prep = [left_h, bottom, 0.3, height]

    ax1 = fig.add_axes(rect_hsm)
    ax2 = fig.add_axes(rect_qrep)
    ax3 = fig.add_axes(rect_prep)
    if nfm:
        ax2.xaxis.set_major_formatter(nullfmt)
        ax3.yaxis.set_major_formatter(nullfmt)

    return [ax1, ax2,ax3]

def hsm_axes1(fig,nfm=False):
    nullfmt   = NullFormatter()         # no labels

    left, width = 0.1, 0.5
    bottom, height = 0.1, 0.5
    bottom_h = left_h = left+width+0.01

    rect_hsm= [left, bottom, width, height]
    rect_qrep = [left, bottom_h, width, 0.3]
    rect_prep = [left_h, bottom, 0.3, height]
    rect_eval = [left_h, bottom_h, 0.3, 0.3]

    ax1 = fig.add_axes(rect_hsm)
    ax2 = fig.add_axes(rect_qrep)
    ax3 = fig.add_axes(rect_prep)
    ax4 = fig.add_axes(rect_eval)
    if nfm:
        ax2.xaxis.set_major_formatter(nullfmt)
        ax3.yaxis.set_major_formatter(nullfmt)
        ax4.xaxis.set_major_formatter(nullfmt)
        ax4.yaxis.set_major_formatter(nullfmt)

    return [ax1, ax2, ax3, ax4]




hsm_cdict ={'blue': ((0.0, 1, 1),
                  (0.1, 1, 1),
                  (0.25, 1, 1),
                  (0.4, 1, 1),
                  (0.6, 0.56, 0.56),
                  (1, 0, 0)),
        'green': ((0.0, 1, 1),
                  (0.1, 1, 1),
                  (0.325, 0, 0),
                  (0.4, 1, 1),
                  (0.6, 1, 1),
                  (0.8, 1, 1),
                  (1, 0, 0)),
        'red': ((0.0, 1, 1),
                (0.1, 1, 1),
                (0.3, 0, 0),
                (0.4, 0, 0),
                (0.6, 0.56, 0.56),
                (0.7, 0.7, 0.7),
                (0.8, 1, 1),
                (1, 1, 1))}

hsm_cmap = matplotlib.colors.LinearSegmentedColormap('hsm_colormap',hsm_cdict,256)
