"""
A default configuration file read by the overlaidHists script
"""

## When using matplotlib, all text from the first column will be replaced
## with the corresponding text in the second column for titles and labels;
## this is necessary to correctly transform ROOT's special LaTeX sytax into
## proper LaTeX sytax for use by matplotlib.

## By default, matplotlib will render only symbols between $'s as TeX, but if
## enable the 'text.usetex' matplotlibrc setting, then everything is handled
## by the LaTeX engine on your system, in which case you can go wild with TeX.

replace = [
    # some defaults that should work for most cases
    ('pt'      , r'$p_\mathrm{T}$'),
    ('pT'      , r'$p_\mathrm{T}$'),
    ('p_{T}'   , r'$p_\mathrm{T}$'),
    ('#eta'    , r'$\eta$'),
    ('#phi'    , r'$\phi$'),
    ('#Deltam' , r'$\Delta m$'),
    ('fb^{-1}' , r'$\mathrm{fb}^{-1}$'),
    ('<'       , r'$<$'),
    ('>'       , r'$>$'),
    ('#'       , r''),
    ]

colors = [
    ## a default set of contrasting colors the author happens to like
    ( 82, 124, 219), # blue
    (212,  58, 143), # red
    (231, 139,  77), # orange
    (145,  83, 207), # purple
    (114, 173, 117), # green
    ( 67,  77,  83), # dark grey
    ]

markers_matplotlib = [
    'o', 's', '^', 'x', '*', 'D', 'h', '1'
    ]

markers_root = [
    ## This default set mirrors the matplotlib markers above
     4, # circle 
    25, # square
    26, # triangle
     5, # x
    30, # five-pointed star
    27, # diamond
    28, # cross
     3, # asterisk
    ]

## Define the size of the legend in ROOT
legend_width = 0.22        # Fraction of canvas width
legend_entry_height = 0.04 # Fraction of canvas height
max_legend_height = 0.3    # Fraction of canvas height

## For more complex needs, you may want to specify a list of files along with
## more descriptive names for the legend using the filenames option.  When
## enabled, any filenames on the command line will be ignored.

## filenames = [
##     ('histTTbar.root', r'$\bar{t}t$'),
##     ('histZmumu.root', r'$Z\rightarrow\mu\mu$'),
##     ]
