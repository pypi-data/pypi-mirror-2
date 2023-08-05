#!/usr/bin/env python
"""
Draw histograms to image files, specifying options on the command line.

You can overlay plots from multiple ROOT files with identical structure.
"""
__version__ = '1.6'

## Created by Jeff Klukas (klukas@wisc.edu), November 2009
## Updated May 2010


######## Import python libraries #############################################

import sys
import optparse
import shutil
import math
import os
import re
import tempfile

try:
    import multiprocessing as multi
    from Queue import Empty
    use_multiprocessing = True
except ImportError:
    use_multiprocessing = False

print """\
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
This tool is now called rootplot; overlayHists is deprecated

If rootplot is not available on your system, you can install it from the
rootplot package on the Python Package Index:
    http://packages.python.org/rootplot/
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

## Unless only displaying the help menu, import PyROOT
if '-h' not in sys.argv and len(sys.argv) > 1:
    try:
        import ROOT
    except ImportError:
        print """\
The program was unable to access PyROOT.  Usually, this just requires switching
to the same major version of python that used when compiling ROOT.  To
determine which version that is, try the following command:
    root -config 2>&1 | tr ' ' '\\n' | egrep 'python|PYTHON'
If this is different from the python version you are currently using, try
changing your PATH to point the new one.  For CMS users, this will all be set
up by running 'cmsenv'."""
        sys.exit(1)
    ROOT.gROOT.SetBatch()
    ROOT.TH1.SetDefaultSumw2()
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    if os.path.exists('rootlogon.C'):
        ROOT.gROOT.Macro('rootlogon.C')
    elif os.path.exists(os.path.expanduser('~/.rootlogon.C')):
        ROOT.gROOT.Macro(os.path.expanduser('~/.rootlogon.C'))


######## Define styles #######################################################

default_styles=r"""\
import ROOT # allows access to ROOT colors (e.g. ROOT.kRed)

#### If you place this file in your home directory as '~/.overlayHists', then
#### it will be automatically loaded whenever you call overlayHists.
#### Otherwise, just include it in the arguments to overlayHist to activate it.

##############################################################################
######## Handling of LaTeX Expressions in matplotlib #########################

## In the replace list below, all text from the first column will be replaced
## with the corresponding text in the second column for titles and labels;
## this is necessary to correctly transform ROOT's special LaTeX sytax into
## proper LaTeX sytax for use by matplotlib.

## By default, matplotlib will render only symbols between $'s as TeX, but if
## you enable the 'text.usetex' matplotlibrc setting, then everything is handled
## by the LaTeX engine on your system, in which case you can go wild with TeX.

replace = [
    # some defaults that should work for most cases
    (' pt '    , r' $p_\mathrm{T}$ '),
    ('pT '     , r'$p_\mathrm{T}$ '),
    (' pT'     , r' $p_\mathrm{T}$'),
    ('p_{T}'   , r'$p_\mathrm{T}$'),
    ('#eta'    , r'$\eta$'),
    ('#phi'    , r'$\phi$'),
    ('fb^{-1}' , r'$\mathrm{fb}^{-1}$'),
    ('pb^{-1}' , r'$\mathrm{pb}^{-1}$'),
    ('<'       , r'$<$'),
    ('>'       , r'$>$'),
    ('#'       , r''),
    ]

## If you include 'use_regexp' as the first item, the patterns to be replaced
## will function as regular expressions using python's re module rather than
## as simple text.  The example below turn's ROOT's superscript and subscript
## syntax into LaTeX:

## replace = [
##     ('use_regexp', True),
##     (r'\^\{(.*)\}', r'$^{\1}$'),
##     (r'\_\{(.*)\}', r'$_{\1}$'),
## ]

##############################################################################
######## Advanced Operation ##################################################

## For more complex needs, you may want to specify a list of files along with
## more descriptive names for the legend using the filenames option.  When
## enabled, any filenames on the command line will be ignored.

## filenames = [
##     ('histTTbar.root', r'$\bar{t}t$'),
##     ('histZmumu.root', r'$Z\rightarrow\mu\mu$'),
##     ]

## If empty, all factors set to 1; otherwise, requires list at least nfiles long
file_scale_factors = []

## Any of the following lists left empty will be filled according to the
## command-line options.  If filled, they must be at least as long as filenames.
## To have an entry default to the command-line options, set the value to None.
linecolors = []
fillcolors = []
markercolors = []
errorbarcolors_mpl = []
linestyles_mpl = []       # 'solid', 'dashed', 'dashdot', 'dotted'
linestyles_root = []      # 1 (solid), 2 (dashed), 3 (dotted), 4 (dashdot), ...
fillstyles_root = []      # 0 (hollow), 1001 (solid), 2001 (hatched), ...
markersizes = []          # in points for matplotlib
plotstyles_mpl = []       # 'bar', 'hist', 'errorbar', 'stack'
drawcommands_root = []    # a TH1::Draw option; include 'stack' to make stacked
alphas_mpl = []           # transparencies for fills (value from 0 to 1)

##############################################################################
######## Global Style Options ################################################

## Colors can be (r, g, b) tuples from 0 to 1 or 0 to 255, ROOT color constants
## (ROOT.kBlue or 600), or any matplotlib color specification if matplotlib is
## available on your system (allows names like 'blue')
colors = [
    ## a default set of contrasting colors the author happens to like
    ( 82, 124, 219), # blue
    (212,  58, 143), # red
    (231, 139,  77), # orange
    (145,  83, 207), # purple
    (114, 173, 117), # green
    ( 67,  77,  83), # dark grey
    ]

## Used with matplotlib output when --markers is specified
## http://matplotlib.sourceforge.net/api/
##        artist_api.html#matplotlib.lines.Line2D.set_marker
markers_mpl = [
    'o', 's', '^', 'x', '*', 'D', 'h', '1'
    ]

## Used with root output when --markers is specified
## http://root.cern.ch/root/html/TAttMarker.html
markers_root = [
     4, # circle
    25, # square
    26, # triangle
     5, # x
    30, # five-pointed star
    27, # diamond
    28, # cross
     3, # asterisk
    ]

#### Styles for --data
data_color = (0,0,0)
mc_color = (50, 150, 150) # Used if only files are present and value is not None
data_fmt = 'o'            # Marker style for matplotlib
data_marker = 4           # Marker style for ROOT

#### Titles produced by --area-normalize and --normalize
area_normalized_title = 'Fraction of Events in Bin'
file_normalized_title = 'Events Normalized to %s'
scale_normalized_title = 'Events Scaled by %d'

#### Overflow and underflow text labels
overflow_text = ' Overflow'
underflow_text = ' Underflow'
overflow_size = 'small'
overflow_alpha = 0.5       # For matplotlib output

#### Ratio plot
ratio_fraction = 0.3  # Fraction of the canvas that bottom plot occupies
ratio_cutoff = 10.    # Ignore bins this many times the average

#### Define how much headroom to add to the plot
top_padding_factor = 1.2
top_padding_factor_log = 5.

##############################################################################
######## ROOT Output #########################################################

#### Define the size of the legend in ROOT
legend_width = 0.22        # Fraction of canvas width
legend_entry_height = 0.04 # Fraction of canvas height
max_legend_height = 0.3    # Fraction of canvas height
legend_left_bound = 0.20   # For left justification
legend_right_bound = 0.87  # For right justification
legend_upper_bound = 0.89  # For top justification
legend_lower_bound = 0.15  # For bottom justification
legend_codes = { 1 : 'upper right',
                 2 : 'upper left',
                 3 : 'lower left',
                 4 : 'lower right',
                 5 : 'right',
                 6 : 'center left',
                 7 : 'center right',
                 8 : 'lower center',
                 9 : 'upper center',
                10 : 'center',
                }

#### Define the style for page numbers
numbering_size_root = 0.03  # Fraction of canvas width
numbering_align_root = 33   # Right-top adjusted
numbering_x_root = 0.97     # Fraction of canvas width
numbering_y_root = 0.985    # Fraction of canvas height

##############################################################################
######## matplotlib Output ###################################################

#### Define the style for page numbers
numbering_size_mpl = 'small'
numbering_ha_mpl = 'right'
numbering_va_mpl = 'top'
numbering_x_mpl = 0.98       # Fraction of canvas width
numbering_y_mpl = 0.98       # Fraction of canvas height

##############################################################################
######## HTML Output #########################################################

#### Number of columns for images in HTML output
ncolumns_html = 2

#### Provide a string containing CSS commands to control webpage output
stylesheet = 'body{padding: 10px; background: #ccccff; font-family: Georgia} img{border: solid black 1px; margin:10px;} h1{border-bottom: solid black 1px;}'

"""


######## Define classes and generators #######################################

class RootFile:
    """A wrapper for TFiles, allowing quick access to the name and Get."""
    def __init__(self, file_name, name=None):
        self.name = name
        if name == None:
            self.name = file_name[:-5]
        self.file = ROOT.TFile(file_name, 'read')
        if self.file.IsZombie():
            print "Error opening %s, exiting..." % file_name
            sys.exit(1)
    def Get(self, object_name, path=None):
        if path:
            return self.file.GetDirectory(path).Get(object_name)
        else:
            return self.file.Get(object_name)

def counter_generator():
    """Incremement the counter used to number plots."""
    k = 0
    while True:
        k += 1
        yield k
next_counter = counter_generator().next



######## These functions are the meat of this program #########################

#### A recursive function to drill down through directories
def process_directory(path, files, options):
    """Loop through all histograms in the directory and plot them."""
    if path == '' and os.path.exists(options.output):
        shutil.rmtree(options.output)
        os.makedirs(options.output)
    dir_to_make = '%s/%s' % (options.plot_dir, path)
    keys = files[0].file.GetDirectory(path).GetListOfKeys()
    plots_to_make = []
    for key in keys:
        name = key.GetName()
        classname = key.GetClassName()
        new_path = '%s/%s' % (path, name)
        if 'TDirectory' in classname:
            plots_to_make += process_directory(new_path, files, options)
        #### If key is a 1D histogram, add it to the list
        matches_path = options.regex.search(new_path)
        dimension = 0
        if ('TH1' in classname or
            #'TGraph' in classname or
            classname == 'TProfile'):
            dimension = 1
        if ('TH2' in classname or classname == 'TProfile2D'): dimension = 2
        if (matches_path and (dimension == 1 or
                              (dimension == 2 and options.draw2D))):
            if not os.path.exists(dir_to_make):
                os.makedirs(dir_to_make)
            counter = next_counter() # used for page numbers
            plots_to_make += [(path, name, counter)]
    return plots_to_make

#### Handle multiprocessing
def plotting_worker(queue, queue_globals, options):
    """Handle a single plot, communicating with the queue."""
    while True:
        try:
            args = queue.get(timeout=5)
        except Empty:
            break
        process_hist(*args, **{'options':options})
        queue_globals.nfinished += 1
        report_progress(queue_globals.nfinished, options.nplots,
                        options.output, options.ext)
        queue.task_done()

#### This is where all the plotting actually happens
def process_hist(path, name, counter, options):
    if options.mpl:
        process_hist_mpl(path, name, counter, options)
    else:
        process_hist_root(path, name, counter, options)

def process_hist_root(path, name, counter, options):
    """Overlay all the instances of this plot in ROOT and apply the options."""
    files = open_rootfiles(options.filenames)
    options = process_local_options(options, name)
    global canvas
    canvas = ROOT.TCanvas()
    if options.ratio:
        pads = divide_canvas(canvas, options.ratio_fraction)
        pads[0].cd()
    else:
        pads = [canvas]
    hists, histmax = [], None
    first_draw = True
    stack = ROOT.THStack('fullst%.3i' % counter, "")
    for i, file in enumerate(files):
        hist = file.file.GetDirectory(path).Get(name)
        if not hist: continue
        if hist.InheritsFrom('TH1'):
            dimension = hist.GetDimension()
        else:
            dimension = 1
        title, xlabel, ylabel = get_labels(hist, options)
        hist.Scale(options.file_scale_factors[i])
        if options.area_normalize:
            ylabel = options.area_normalized_title
        if type(options.normalize) is float:
            ylabel = options.scale_normalized_title % options.normalize
            hist.Scale(options.normalize)
        if type(options.normalize) is int:
            filename = files[options.normalize - 1].name
            ylabel = options.file_normalized_title % filename
        hist.SetTitle("%s;%s;%s" % (title, xlabel, ylabel))
        hists.append(hist)
    for hist in hists:
        if options.area_normalize:
            integral = hist.Integral()
            if integral: hist.Scale(1. / integral)
        if type(options.normalize) is float:
            hist.Scale(options.normalize)
        if type(options.normalize) is int:
            nbins = hist.GetNbinsX()
            lowbin, highbin = 1, nbins + 1
            normhist = hists[options.normalize - 1]
            if options.range:
                xedges = [normhist.GetXaxis().GetBinLowEdge(i)
                          for j in range(1, nbins + 1)]
                lowbin, highbin = parse_range(xedges, options.range)
            integral = normhist.Integral(lowbin, highbin)
            if integral:
                hist.Scale(integral / hist.Integral(lowbin, highbin))
        if 'stack' in options.drawcommands_root[i]:
            stack.Add(hist)
        histmax = max(histmax, hist.GetMaximum(), stack.GetMaximum())
    if options.efficiency:
        histmax = 1. / options.top_padding_factor
    stack.SetTitle("%s;%s;%s" % (title, xlabel, ylabel))
    if options.gridx or options.grid:
        for pad in pads:
            pad.SetGridx(not pad.GetGridx())
    if options.gridy or options.grid:
        pads[0].SetGridy(not pads[0].GetGridy())
    legend = ROOT.TLegend(*parse_legend_root(options))
    for com in options.drawcommands_root:
        if 'stack' in com:
            first_draw = prep_first_draw(stack, histmax, options)
            stack.Draw(options.draw)
            break
    for i, (file, hist) in enumerate(zip(files, hists)):
        hist.SetLineColor(options.linecolors[i])
        hist.SetFillColor(options.fillcolors[i])
        hist.SetMarkerColor(options.markercolors[i])
        hist.SetFillStyle(options.fillstyles_root[i])
        hist.SetMarkerStyle(options.markers_root[i])
        hist.SetMarkerSize(options.markersizes[i])
        if dimension == 1:
            nbins = hist.GetNbinsX()
            if options.efficiency_from:
                denom = file.file.Get(options.efficiency_from)
                num = [hist.GetBinContent(j) for j in range(1, nbins + 1)]
                den = [denom.GetBinContent(j) for j in range(1, nbins + 1)]
                eff, up, down = wilson(num, den)
                for j in range(nbins):
                    hist.SetBinContent(j + 1, eff[j])
                    hist.SetBinError(j + 1, max(up[j], down[j]))
            if options.overflow:
                hist.AddBinContent(nbins, hist.GetBinContent(nbins + 1))
            if options.underflow:
                hist.AddBinContent(1, hist.GetBinContent(0))
            if 'stack' not in options.drawcommands_root[i]:
                if first_draw:
                    first_draw = prep_first_draw(hist, histmax, options)
                    hist.Draw(options.drawcommands_root[i])
                else:
                    hist.Draw("same " + options.drawcommands_root[i])
        else:
            hist.Draw(options.draw2D)
        legend.AddEntry(hist, file.name)
    if options.ratio and dimension == 1:
        pads[1].cd()
        stack_ratio = plot_ratio_root(hists, options)
        pads[0].cd()
    if options.logx:
        for pad in pads:
            pad.SetLogx(True)
    if options.logy:
        for pad in pads:
            pad.SetLogy(True)
    if options.numbering:
        display_page_number(counter, options)
    if options.overflow and dimension == 1:
        display_overflow(stack, hist)
    if options.underflow and dimension == 1:
        display_underflow(stack, hist)
    if options.legend and dimension == 1:
        legend.Draw()
    save_plot(options.plot_dir, path, name, options.ext, counter)

#### This is where all the plotting actually happens
def process_hist_mpl(path, name, counter, options):
    """Overlay all the instances of this plot and output using matplotlib."""
    files = open_rootfiles(options.filenames)
    options = process_local_options(options, name)
    fig = plt.figure(1, figsize=parse_size(options.size))
    plt.clf() # clear figure
    axes, hists, = plt.axes(), []
    axes_list = [axes, axes]
    if options.ratio:
        axes_list = divide_axes(axes, options.ratio_fraction)
        axes = axes_list[0]
        fig.sca(axes)
    fullstack, barstack, histmax = r2m.HistStack(), r2m.HistStack(), None
    allempty = True
    #### Apply options to hist from each file
    for i, file in enumerate(files):
        roothist = file.Get(name, path)
        if roothist.InheritsFrom('TH1') and roothist.GetEntries() > 0:
            allempty = False
        if roothist.InheritsFrom('TGraph'):
            allempty = False
        if roothist.InheritsFrom('TH1'):
            dimension = roothist.GetDimension()
        else:
            dimension = 1
        title, xlabel, ylabel = get_labels(roothist, options)
        roothist.Scale(options.file_scale_factors[i])
        if options.normalize:
            if type(options.normalize) is int:
                file_name = files[options.normalize - 1].name
                ylabel = options.file_normalized_title % file_name
            else:
                ylabel = options.scale_normalized_title % options.normalize
        if dimension == 1:
            hist = r2m.Hist(roothist, replace=options.replace, label=file.name,
                            title=title, xlabel=xlabel, ylabel=ylabel)
        else:
            hist = r2m.Hist2D(roothist, replace=options.replace,
                              label=file.name, title=title,
                              xlabel=xlabel, ylabel=ylabel)
        if options.efficiency_from:
            denom = r2m.Hist(file.file.Get(options.efficiency_from))
            hist.y, up, down = wilson(hist.y, denom.y)
            hist.yerr = np.array([up, down])
        if dimension == 1:
            if options.overflow:
                hist.y[-1] += hist.overflow
            if options.underflow:
                hist.y[0] += hist.underflow
            if options.area_normalize:
                if sum(hist.y):
                    hist.scale(1./sum(hist.y))
            if options.normalize:
                numerhist = hists[options.normalize - 1]
                if type(options.normalize) is int:
                    hists[options.normalize - 1]
                    if options.range:
                        lowbin, highbin = parse_range(hist.xedges,
                                                      options.range)
                        numer = numerhist.TH1F().Integral(lowbin, highbin)
                        denom = hist.TH1F().Integral(lowbin, highbin)
                    else:
                        numer = sum(numerhist.y)
                        denom = sum(hist.y)
                    if denom:
                        hist.scale(numer / denom)
                else:
                    hist.scale(options.normalize)
            if options.plotstyles_mpl[i] == "stack":
                barstack.add(hist, log=options.logy,
                             edgecolor=options.linecolors[i],
                             facecolor=options.fillcolors[i])
                histmax = max(histmax, barstack.max())
            else:
                histmax = max(histmax, max(hist))
        fullstack.add(hist)
        hists.append(hist)
    if allempty:
        plt.figtext(0.5, 0.5, "No Entries", ha='center', va='center')
    elif dimension == 1:
        for i, (file, hist) in enumerate(zip(files, hists)):
            if options.plotstyles_mpl[i] == "errorbar":
                if options.logy:
                    # Logy would fail if hist all zeroes
                    if np.nonzero(hist.y)[0].tolist():
                        plt.yscale('log')
                hist.errorbar(yerr=True, fmt=options.markers_mpl[i],
                              color=options.fillcolors[i],
                              ecolor=options.errorbarcolors_mpl[i])
            if options.plotstyles_mpl[i] == "hist":
                for j in range(hist.nbins):
                    hist.y[j] = max(hist.y[j], 1e-10)
                hist.hist(alpha=options.alphas_mpl[i], histtype='stepfilled',
                          log=options.logy, edgecolor=options.linecolors[i],
                          facecolor=options.fillcolors[i])
            if options.plotstyles_mpl[i] == "bar":
                hist.bar(alpha=options.alphas_mpl[i], log=options.logy,
                         edgecolor=options.linecolors[i],
                         facecolor=options.fillcolors[i])
            if options.logx:
                for ax in axes_list:
                    ax.set_xscale('log')
        if barstack.hists:
            barstack.barstack()
        plt.xlim(hist.xedges[0], hist.xedges[-1])
        if options.logy and 'hist' in options.plotstyles_mpl:
            my_min = fullstack.min(threshold=1.1e-10)
            rounded_min = 1e100
            while (rounded_min > my_min):
                rounded_min /= 10
            plt.ylim(ymin=rounded_min)
        if options.zero and not options.logy:
            plt.ylim(ymin=0.)
        if options.ymin:
            plt.ylim(ymin=options.ymin)
        if options.ymax:
            plt.ylim(ymax=options.ymax)
        if options.efficiency:
            plt.ylim(ymax=1.)
        elif histmax != 0 and not options.ymax:
            plt.ylim(ymax=histmax * options.top_padding_factor)
        if options.overflow:
            plt.text(hist.x[-1], plt.ylim()[0], options.overflow_text,
                     rotation='vertical', ha='center',
                     alpha=options.overflow_alpha, size=options.overflow_size)
        if options.underflow:
            plt.text(hist.x[0], plt.ylim()[0], options.underflow_text,
                     rotation='vertical', ha='center',
                     alpha=options.overflow_alpha, size=options.overflow_size)
        if options.gridx or options.grid:
            axes.xaxis.grid()
        if options.gridy or options.grid:
            axes.yaxis.grid()
        if options.legend != 'None':
            try:
                options.legend = int(options.legend)
            except ValueError:
                pass
            plt.legend(numpoints=1, loc=options.legend)
    else:
        drawfunc = getattr(hist, options.mpl2D)
        if 'col' in options.mpl2D:
            drawfunc()
        else:
            drawfunc(color=options.fillcolors[0])
    plt.title(fullstack[-1].title)
    plt.ylabel(fullstack[-1].ylabel)
    fig.sca(axes_list[1])
    plt.xlabel(fullstack[-1].xlabel)
    if options.ratio:
        fig.sca(axes_list[1])
        plot_ratio_mpl(hists, options)
    if options.numbering:
        plt.figtext(options.numbering_x_mpl, options.numbering_y_mpl,
                    counter, size=options.numbering_size_mpl,
                    ha=options.numbering_ha_mpl, va=options.numbering_va_mpl)
    output_file_name = '%s/%s/%s' % (options.plot_dir, path, name)
    plt.savefig(output_file_name, transparent=options.transparent,
                dpi=options.dpi)


######## Define some supporting functions #####################################

def open_rootfiles(filenames):
    """Return a list of RootFile objects from a list of file names."""
    try:
        return [RootFile(name) for name in filenames]
    except TypeError:
        return [RootFile(name, displayname) for name, displayname in filenames]

def parse_size(size_option):
    """Return a width and height parsed from size_option."""
    xpos = size_option.find('x')
    return float(size_option[:xpos]), float(size_option[xpos+1:])

def parse_color(color, tcolor=False):
    """
    Return an rgb tuple or a ROOT TColor.

    Input can be a ROOT color index (i.e. 5 or ROOT.kRed) or an rgb(a) tuple.
    """
    if color is None:
        return None
    elif color == 'none' or color == 'None':
        return 'none'
    r, g, b = 0, 0, 0
    try:
        color = ROOT.gROOT.GetColor(color)
        r, g, b = color.GetRed(), color.GetGreen(), color.GetBlue()
    except TypeError:
        try:
            if max(color) > 1.:
                color = [x/256. for x in color][0:3]
        except TypeError:
            pass
        try:
            color = mpal.colors.colorConverter.to_rgb(color)
        except NameError:
            pass
        r, g, b = color[0:3]
    if tcolor:
        return ROOT.TColor.GetColor(r, g, b)
    return (r, g, b)

def get_labels(hist, options):
    """Return the appropriate histogram and axis titles for hist."""
    title = hist.GetTitle()
    xlabel = hist.GetXaxis().GetTitle()
    ylabel = hist.GetYaxis().GetTitle()
    if options.title:
        if options.title.startswith('+'):
            title += options.title[1:]
        else:
            title = options.title
    if options.xlabel:
        if options.xlabel.startswith('+'):
            xlabel += options.xlabel[1:]
        else:
            xlabel = options.xlabel
    if options.ylabel:
        if options.ylabel.startswith('+'):
            ylabel += options.ylabel[1:]
        else:
            ylabel = options.ylabel
    return title, xlabel, ylabel

def save_plot(plot_dir, path, name, ext, counter):
    """Save the canvas to the output format defined by --ext."""
    output_file_name = '%s/%s/%s.%s' % (plot_dir, path, name, ext)
    canvas.SaveAs(output_file_name)

def report_progress(counter, nplots, output, ext, divisor=1):
    """Print the current number of finished plots."""
    if counter % divisor == 0:
        print("\r%i plots of %i written to %s/ in %s format" %
              (counter, nplots, output, ext)),
        sys.stdout.flush()

def merge_pdf(output, plots_to_make):
    """Merge together all the produced plots into one pdf file."""
    if not plots_to_make:
        print "No output files, so no merged pdf was made"
        return
    print "Writing %s.pdf..." % output
    paths = ["%s%s/%s" % (output, path, name)
             for (path, name, counter) in plots_to_make]
    paths = [x.replace(' ', r'\ ') for x in paths]
    os.system('gs -q -dBATCH -dNOPAUSE -sDEVICE=pdfwrite '
              '-dAutoRotatePages=/All '
              '-sOutputFile=%s.pdf ' % output +
              '.pdf '.join(paths) + '.pdf')

def display_page_number(page_number, options):
    """Add a page number to the top corner of the canvas."""
    page_text = ROOT.TText()
    page_text.SetTextSize(options.numbering_size_root)
    page_text.SetTextAlign(options.numbering_align_root)
    page_text.DrawTextNDC(options.numbering_x_root, options.numbering_y_root,
                          '%i' % page_number)

def display_overflow(stack, hist):
    """Add the overflow to the last bin and print 'Overflow' on the bin."""
    nbins = hist.GetNbinsX()
    x = 0.5 * (hist.GetBinLowEdge(nbins) +
               hist.GetBinLowEdge(nbins + 1))
    y = stack.GetMinimum('nostack')
    display_bin_text(x, y, nbins, 'Overflow')

def display_underflow(stack, hist):
    """Add the underflow to the first bin and print 'Underflow' on the bin."""
    nbins = hist.GetNbinsX()
    x = 0.5 * (hist.GetBinLowEdge(1) +
               hist.GetBinLowEdge(2))
    y = stack.GetMinimum('nostack')
    display_bin_text(x, y, nbins, 'Underflow')

def display_bin_text(x, y, nbins, text):
    """Overlay TEXT on this bin."""
    bin_text = ROOT.TText()
    bin_text.SetTextSize(min(1. / nbins, 0.04))
    bin_text.SetTextAlign(12)
    bin_text.SetTextAngle(90)
    bin_text.SetTextColor(13)
    bin_text.SetTextFont(42)
    bin_text.DrawText(x, y, text)

def prep_first_draw(hist, histmax, options):
    """Set all the pad attributes that depend on the first object drawn."""
    hist.SetMaximum(histmax * options.top_padding_factor)
    if options.zero and not ROOT.gPad.GetLogy():
        hist.SetMinimum(0.)
    if options.ymin:
        hist.SetMinimum(options.ymin)
    if options.ymax:
        hist.SetMaximum(options.ymax)
    if options.ratio:
        hist.GetXaxis().SetBinLabel(1, '') # Don't show numbers below top plot
        hist.GetXaxis().SetTitle('')
        if hist.GetYaxis().GetTitle() == '':
            hist.GetYaxis().SetTitle('Content')
        ## Avoid overlap of y-axis numbers by supressing zero
        if (hist.GetMaximum() > 0 and
            hist.GetMinimum() / hist.GetMaximum() < 0.25):
            hist.SetMinimum(hist.GetMaximum() / 10000)
    return False

def divide_canvas(canvas, ratio_fraction):
    """Divide the canvas into two pads; the bottom is ratio_fraction tall."""
    ## Both pads are set to the full canvas size to maintain font sizes
    ## Fill style 4000 used to ensure pad transparency because of this
    margins = [ROOT.gStyle.GetPadTopMargin(), ROOT.gStyle.GetPadBottomMargin()]
    useable_height = 1 - (margins[0] + margins[1])
    canvas.Clear()
    pad = ROOT.TPad('mainPad', 'mainPad', 0., 0., 1., 1.)
    pad.SetFillStyle(4000)
    pad.Draw()
    pad.SetBottomMargin(margins[1] + ratio_fraction * useable_height)
    pad_ratio = ROOT.TPad('ratioPad', 'ratioPad', 0., 0., 1., 1.);
    pad_ratio.SetFillStyle(4000)
    pad_ratio.Draw()
    pad_ratio.SetTopMargin(margins[0] + (1 - ratio_fraction) * useable_height)
    return pad, pad_ratio

def plot_ratio_root(hists, options):
    """Plot the ratio of each hist in hists to the ratio_indexth hist."""
    ratio_index = options.ratio - 1
    stack_ratio = ROOT.THStack('stRatio', ';%s;Ratio'
                               % hists[1].GetXaxis().GetTitle())
    for hist in (hists[0:ratio_index] + hists[ratio_index + 1:]):
        ratio_hist = hist.Clone()
        ratio_hist.Sumw2()
        ratio_hist.Divide(hists[ratio_index])
        average = ratio_hist.Integral() / ratio_hist.GetNbinsX()
        for j in range(ratio_hist.GetNbinsX()):
            if ratio_hist.GetBinContent(j) > options.ratio_cutoff * average:
                ratio_hist.SetBinContent(j, 0)
                ratio_hist.SetBinError(j, 0)
        stack_ratio.Add(ratio_hist)
    stack_ratio.Draw()
    stack_ratio.GetYaxis().SetNdivisions(507) # Avoids crowded labels
    stack_ratio.Draw("nostack e")
    return stack_ratio

def divide_axes(axes, ratio_fraction):
    """Create two subaxes, the lower one taking up ratio_fraction of total."""
    x1, y1, x2, y2 = axes.get_position().get_points().flatten().tolist()
    width = x2 - x1
    height = y2 - y1
    lower_height = height * ratio_fraction
    upper_height = height - lower_height
    lower_axes = plt.axes([x1, y1, width, lower_height], axisbg='None')
    upper_axes = plt.axes([x1, y1 + lower_height, width, upper_height],
                          axisbg='None', sharex=lower_axes)
    ## Make original axes and the upper ticklabels invisible
    axes.set_xticks([])
    axes.set_yticks([])
    plt.setp(upper_axes.get_xticklabels(), visible=False)
    return upper_axes, lower_axes

def plot_ratio_mpl(hists, options):
    """Plot the ratio of each hist in hists to the ratio_indexth hist."""
    ratio_index = options.ratio - 1
    stack = r2m.HistStack()
    for i in range(len(hists)):
        if i != ratio_index:
            ratio_hist = hists[i] / hists[ratio_index]
            for j in range(ratio_hist.nbins):
                average = sum(ratio_hist.y) / ratio_hist.nbins
                if ratio_hist.y[j] > options.ratio_cutoff * average:
                    ratio_hist.y[j] = None
                    ratio_hist.yerr[j] = None
            stack.add(ratio_hist, fmt=options.markers_mpl[i],
                  color=options.fillcolors[i],
                  ecolor=options.errorbarcolors_mpl[i])
    stack.errorbar(yerr=True)
    plt.gca().yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(
        nbins=5, steps=[1, 2, 5, 10]))
    plt.ylim(ymax=plt.ylim()[1]/1.01)
    plt.ylabel('Ratio')

def wilson(numerator, denominator):
    nbins = len(numerator)
    eff = [numerator[i] / denominator[i] for i in range(nbins)]
    up = []
    down = []
    for i in range(nbins):
        n = denominator[i]
        sqrt = math.sqrt(eff[i] * (1 - eff[i]) / n + 1 / (4 * n * n))
        up.append(-eff[i] + (1/(1 + 1/n) * (eff[i] + 1/(2*n) + sqrt)))
        down.append(eff[i] - (1/(1 + 1/n) * (eff[i] + 1/(2*n) - sqrt)))
    return eff, up, down

def make_html_index(base_dir, directory, filetype, stylesheet, ncolumns=2):
    fullpath = '%s%s' % (base_dir, directory)
    output = open('%s/index.html' % fullpath, 'w')
    contents = sorted(os.listdir(fullpath))
    subdirs = fullpath.split('/')
    pathnav = '/'.join(['<a href="%s">%s</a>' %
                        ('../' * (len(subdirs) - i - 1), subdirs[i])
                        for i in range(len(subdirs))])
    nav_items = ['<li><a href="%s">%s</a></li>' % (x, x) for x in contents
                 if os.path.isdir("%s/%s/%s" % (base_dir, directory, x))]
    navigation = '\n    '.join(nav_items)
    img_items = ['<a name="%s"><a href="index.html#%s"><img src="%s"></a></a>'
                 % (x,x,x) for x in contents if x.endswith(filetype)]
    image_markup = '\n' + '\n'.join(img_items)
    image_markup = re.sub('((\\n<img.*){%i})' % ncolumns,
                          r'\1<br>', image_markup)
    output.write(
        '''
        <html>
        <head>
        <style type="text/css">%s</style>
        <title>%s</title>
        </head>
        <body>
        <h1>Navigation</h1>
          %s
          <ul>
            <li><a href="..">..</a></li>
              %s
          </ul>
        <h1>Images</h1>
        %s
        </body>
        </html>''' % (stylesheet, directory, pathnav, navigation, image_markup))
    output.close()

def parse_range(xedges, expression):
    """Returns the indices of the low and high bins indicated in expression."""
    closest = lambda l,y: l.index(min(l, key=lambda x:abs(x-y)))
    match = re.match(r'([^x]*)x([^x]*)', expression)
    lower, upper = float(match.group(1)), float(match.group(2))
    lowbin = closest(xedges, lower) + 1
    highbin = closest(xedges, upper)
    return lowbin, highbin

def parse_legend_root(options):
    """Return the corners to use for the legend based on options."""
    legend_height = min(options.legend_entry_height * options.nfiles + 0.02,
                        options.max_legend_height)
    if type(options.legend) is int:
        options.legend = options.legend_codes[options.legend]
    elif options.legend.lower() == 'none':
        options.legend = None
    if options.legend:
        if 'upper' in options.legend:
            top = options.legend_upper_bound
            bottom = options.legend_upper_bound - legend_height
        elif 'lower' in options.legend:
            bottom = options.legend_lower_bound
            top = options.legend_lower_bound + legend_height
        else:
            top = 0.5 + legend_height / 2
            bottom = 0.5 - legend_height / 2
        if 'left' in options.legend:
            left = options.legend_left_bound
            right = options.legend_left_bound + options.legend_width
        elif 'right' in options.legend:
            right = options.legend_right_bound
            left = options.legend_right_bound - options.legend_width
        else:
            right = 0.5 + options.legend_width / 2
            left = 0.5 - options.legend_width / 2
        return [left, bottom, right, top]
    return [0, 0, 0, 0]

def append_to_options(config, options):
    """Add all attributes in config to options."""
    for attribute in dir(config):
        if '__' not in attribute:
            attr = getattr(config, attribute)
            setattr(options, attribute, attr)
    return options

def add_options_from_configuration(options):
    """Define a set of global variables storing style information"""
    configdir = tempfile.mkdtemp()
    sys.path.insert(0, configdir)
    sys.path.insert(0, '')
    f = open(configdir + '/default_overlay_config.py', 'w')
    f.write(default_styles)
    f.close()
    if options.config:
        shutil.move(configdir + '/default_overlay_config.py',
                    'overlayHists_config.py')
        print "Wrote overlayHists_config.py to the current directory"
        sys.exit(0)
    import default_overlay_config
    options = append_to_options(default_overlay_config, options)
    rc_path = os.path.expanduser('~/.overlayHists')
    if os.path.exists(rc_path):
        shutil.copy(rc_path, configdir + '/overlay_rc.py')
        options.config_files.insert(0, 'overlay_rc.py')
    for f in options.config_files:
        try:
            user_config = __import__(f[:-3])
        except ImportError:
            print "%s not found!  Exiting..." % f
            sys.exit(1)
        options = append_to_options(user_config, options)
    shutil.rmtree(configdir)
    return options

def process_options(options):
    """Select plot-level options based on the user-level input."""
    options.nfiles = nfiles = len(options.filenames)
    if nfiles > 1: options.draw2D = None
    if options.merge: options.ext = 'pdf'
    if options.stack: options.mpl = 'stack'
    elif options.bar: options.mpl = 'bar'
    elif options.errorbar: options.mpl = 'errorbar'
    elif options.hist: options.mpl = 'hist'
    if options.mpl and type(options.mpl) is not str:
        options.mpl = 'hist'
    try:
        global matplotlib
        import matplotlib
    except ImportError:
        if options.mpl:
            print("Unable to load matplotlib, "
                  "which is required for these options")
            sys.exit(1)
    else:
        global r2m, np, plt
        if options.ext == 'png':
            matplotlib.use('AGG')
        if options.ext == 'pdf':
            matplotlib.use('PDF')
        if options.ext == 'ps':
            matplotlib.use('PS')
        if options.mpl or options.colormap:
            from matplotlib import pyplot as plt
        if options.colormap:
            cmap = plt.get_cmap(options.colormap)
            if options.ncolors < nfiles:
                options.ncolors = nfiles
            options.colors = [cmap(float(i)/options.ncolors)
                              for i in range(nfiles)]
        else:
            options.ncolors = len(options.colors)
            if nfiles > options.ncolors:
                print "Not enough colors defined!"
                sys.exit(1)
        if options.mpl:
            try:
                import root2matplot as r2m
                import numpy as np
            except ImportError:
                print("Unable to load root2matplot, "
                      "which is required for operation with matplotlib")
                sys.exit(1)
    if options.normalize:
        if '.' in options.normalize:
            options.normalize = float(options.normalize)
        else:
            options.normalize = int(options.normalize)
    if options.efficiency_from:
        options.efficiency = True
    if not options.file_scale_factors:
        options.file_scale_factors = [1.0 for i in xrange(nfiles)]
    if not options.markers:
        options.markers_mpl = ['o' for i in xrange(nfiles)]
    if not options.linecolors:
        options.linecolors = options.colors
    if not options.fillcolors:
        options.fillcolors = options.colors
    if not options.linestyles_mpl:
        options.linestyles_mpl = ['solid' for i in xrange(nfiles)]
    if not options.linestyles_root:
        options.linestyles_root = [1 for i in xrange(nfiles)]
    if not options.fillstyles_root:
        if options.fill or options.data:
            options.fillstyles_root = [1001 for i in xrange(nfiles)]
        else:
            options.fillstyles_root = [0 for i in xrange(nfiles)]
    if not options.markercolors:
        options.markercolors = options.colors
    if not options.plotstyles_mpl:
        options.plotstyles_mpl = [options.mpl for i in xrange(nfiles)]
    if not options.drawcommands_root:
        options.drawcommands_root = [options.draw for i in xrange(nfiles)]
    if not options.markersizes:
        if options.markers: size = ROOT.gStyle.GetMarkerSize()
        else: size = 0
        options.markersizes = [size for i in xrange(nfiles)]
    if not options.errorbarcolors_mpl:
        options.errorbarcolors_mpl = [None for i in xrange(nfiles)]
    if not options.alphas_mpl:
        options.alphas_mpl = [options.alpha for i in xrange(nfiles)]
    if options.efficiency:
        for i in range(len(options.drawcommands_root)):
            if options.drawcommands_root[i] != 'stack':
                options.drawcommands_root[i] += 'e'
        options.draw += 'e'
    if options.data:
        i = options.data - 1
        options.linecolors[i] = options.data_color
        options.fillcolors[i] = options.data_color
        options.plotstyles_mpl[i] = 'errorbar'
        options.drawcommands_root[i] = 'e'
        options.markers_root[i] = options.data_marker
        options.draw = 'nostack hist'
        if not options.markersizes[i]:
            options.markersizes[i] = ROOT.gStyle.GetMarkerSize()
        if nfiles == 2 and options.mc_color:
            options.fillcolors[(i+1)%2] = options.mc_color
    for opt in ['linecolors', 'fillcolors', 'markercolors',
                'errorbarcolors_mpl']:
        colors = getattr(options, opt)
        setattr(options, opt, [parse_color(x, not options.mpl)
                               for x in colors])
    return options

def process_local_options(options, name):
    """Turn on sticky options for a particular plot."""
    if options.sticky:
        if 'Norm' in name: options.area_normalize = True
        if 'Eff' in name: options.efficiency = True
        if 'Logx' in name: options.logx = True
        if 'Logy' in name: options.logy = True
        if 'Zero' in name: options.zero = True
	if 'Overflow' in name: options.overflow = True
        if 'Underflow' in name: options.underflow = True
        if 'Ratio' in name: options.ratio = True
    if options.logy:
        options.zero = False
        options.top_padding_factor = options.top_padding_factor_log
    return options


######## Define the main program #############################################

def main():
    usage="""usage: %prog [options] [style_config.py] [file1.root ...]

Documentation: http://packages.python.org/root2matplot/

Function: overlays corresponding histograms from several files, dumping the
  images into a directory structure that mirrors that of the ROOT file.  Most
  style options can be controlled from your rootlogon.C macro.

Power users: advanced operation using configuration files is described in the
  full online documentation.  This allows you control over colors, styles,
  names for the legends, and more.  Get the default config with --config, make
  your changes, and include it as an argument on the command line.

Matplotlib: if you have the matplotlib python plotting library installed on your
  system, you can produce output in matplotlib.  This will be activated by
  enabling any of the options 'mpl', 'bar', 'errorbar', 'hist', or 'stack'."""

    parser = optparse.OptionParser(usage=usage,
                                   version='%s %s' % ('%prog', __version__))
    parser.add_option('--config', action='store_true',
                      help="do nothing but write a template configuration file "
                      "called overlayHists_config.py")
    parser.add_option('-e', '--ext', default='png',
                      help="choose an output extension; default is png")
    parser.add_option('-m', '--markers', action='store_true', default=False,
                      help="add markers to histograms")
    parser.add_option('-s', '--sticky', action='store_true', default=False,
                      help="enable name-based special plotting options "
                      "(see below)")
    parser.add_option('--merge', action='store_true', default=False,
                      help="creates a single pdf file containing all plots")
    parser.add_option('--noclean', action='store_true', default=False,
                      help="skips destroying the output directory before "
                      "drawing")
    parser.add_option('--data', type='int', default=0, metavar='FILENUM',
                      help="the histogram from the FILENUMth (starting from 1) "
                      "file will be drawn as black datapoints, while all "
                      "others will be filled, as is the custom for showing "
                      "data vs. Monte Carlo.")
    parser.add_option('--output', default='overlaidHists', metavar='NAME',
                      help="name of output directory; default is "
                      "'overlaidHists'")
    parser.add_option('--numbering', action='store_true', default=False,
                      help="add a page number in the upper right of each plot")
    parser.add_option('--path', default='',
                      help="only process plot(s) in the given location or its "
                      "subdirectories; PATH may be a regular expression (use "
                      ".* for wildcard)")
    parser.add_option('--ymax', type='float', default=None,
                      help="set the maximum value of the y-axis")
    parser.add_option('--ymin', type='float', default=None,
                      help="set the minimum value of the y-axis")
    parser.add_option('--normalize', metavar='VALUE', default=None,
                      help="if integer, normalize to the VALUEth file "
                      "(starting with 1); if float, scale by VALUE")
    parser.add_option('--range', metavar='LOWxHIGH',
                      help="only use the specified data range in determining "
                      "the normalization")
    parser.add_option('--colormap', default=None,
                      help="Select colors from the given matplotlib "
                      "colormap rather than the defaults")
    parser.add_option('--ncolors', type='int', default=None,
                      help="The number of colors with which to divide the "
                      "colormap")
    parser.add_option('--legend', default=1, metavar='LOC',
                      help="Place legend in LOC, according to matplotlib "
                      "location codes; examples include 'upper right', "
                      "'center', or 'center left'")
    parser.add_option('--title', default=None,
                      help="Replace the plot titles, or add to them by "
                      "preceeding with a '+'")
    parser.add_option('--xlabel', default=None,
                      help="Replace the x-axis labels, or add to them by "
                      "preceeding with a '+'")
    parser.add_option('--ylabel', default=None,
                      help="Replace the y-axis labels, or add to them by "
                      "preceeding with a '+'")
    parser.add_option('--grid', action='store_true', default=False,
                      help="Toggle the grid on or off for both axes")
    parser.add_option('--gridx', action='store_true', default=False,
                      help="Toggle the grid on or off for the x axis")
    parser.add_option('--gridy', action='store_true', default=False,
                      help="Toggle the grid on or off for the y axis")
    parser.add_option('--efficiency-from', default=None, metavar='DENOM',
                      help="Divide all plots by the histogram in path DENOM")
    parser.add_option('--processors', type='int', default=4, metavar='NUM',
                      help="Divide plot making up into NUM different processes")
    group1 = optparse.OptionGroup(
        parser,
        "Special plotting options",
        "Use the command line options given below to apply changes to all "
        "plots.  If you only wish to apply an option to a specific plot, "
        "you can use '-s' "
        "to turn on sticky keywords (such as 'Norm').  Any plot that includes "
        "the given keyword in its ROOT name will have the option applied "
        "regardless of its presence or absence on the command line."
        )
    group1.add_option('-n', '--area-normalize', action='store_true',
                      default=False,
                      help="'Norm': area normalize the histograms")
    group1.add_option('--efficiency', action='store_true', default=False,
                      help="'Eff' : force y axis scale to run from 0 to 1")
    group1.add_option('--logx', action='store_true', default=False,
                      help="'Logx': force log scale for x axis")
    group1.add_option('--logy', action='store_true', default=False,
                      help="'Logy': force log scale for y axis")
    group1.add_option('--zero', action='store_true', default=False,
                      help="'Zero': force zero for the y-axis minimum")
    group1.add_option('--overflow', action='store_true', default=False,
                      help="'Overflow' : display overflow content in "
                      "highest bin")
    group1.add_option('--underflow', action='store_true', default=False,
                      help="'Underflow': display underflow content in "
                      "lowest bin")
    group1.add_option('--ratio', type='int', default=0, metavar='FILENUM',
                      help="'Ratio': cut the canvas in two, displaying on the "
                      "bottom the ratio of each histogram to the histogram in "
                      "the FILENUMth (starting from 1) file.")
    group2 = optparse.OptionGroup(parser,"Options specific to ROOT (default)"
                                  " output")
    group2.add_option('--draw', default='p H', metavar='"p H"',
                      help="argument to pass to ROOT's Draw command; "
                      "try 'e' for error bars")
    group2.add_option('--draw2D', default='box', metavar='"box"',
                      help="argument to pass to ROOT's Draw command for 2D "
                      "hists (only drawn when a single file is present); set "
                      'to "" to turn off 2D drawing')
    group2.add_option('-f', '--fill', action='store_true', default=False,
                      help="Histograms will have a color fill")
    group3 = optparse.OptionGroup(parser,
                                "Producing output with matplotlib")
    group3.add_option('--mpl', action="store_true", default=False,
                      help="produce output in matplotlib; automatically "
                      "turned on by --stack, --errorbar, --bar, or --hist")
    group3.add_option('--mpl2D', default='box', metavar='"box"',
                      help="Type of plot to produce for 2D histograms in "
                      "matplotlib.  Choose from 'contour', 'col', 'colz', or "
                      "'box'")
    group3.add_option('--stack', action="store_true", default=False,
                      help="output a matplotlib stacked bar graph")
    group3.add_option('--errorbar', action="store_true", default=False,
                      help="output a matplotlib errorbar graph")
    group3.add_option('--bar', action="store_true", default=False,
                      help="output a matplotlib bar graph")
    group3.add_option('--hist', action="store_true", default=False,
                      help="output a matplotlib hist graph (with solid fill)")
    group3.add_option('--alpha', type='float', default=0.5,
                      help="set the transparency factor used for matplotlib "
                      "bar and hist graphs "
                      "(default is 0.5; 1.0 is fully opaque)")
    group3.add_option('--transparent', action="store_true", default=False,
                      help="use a transparent background")
    group3.add_option('--size', default='6x4.5',
                      help="Define the plot size as "
                      "'width x height' in inches; default is '6x4.5'")
    group3.add_option('--dpi', type=float, default=None,
                      help="Set the resolution of matplotlib output (default "
                      "is 100)")
    parser.add_option_group(group2)
    parser.add_option_group(group3)
    parser.add_option_group(group1)
    options, arguments = parser.parse_args()
    options.plot_dir = '%s/%s' % (os.path.abspath('.'), options.output)
    options.regex = re.compile(options.path)
    for arg in arguments:
        if arg[-5:] != ".root" and arg[-3:] != ".py":
            raise TypeError("Arguments must be root files "
                            "or python configurations!")
    options.config_files = [x for x in arguments if x[-3:] == ".py"]
    filenames_from_interface = [x for x in arguments if x[-5:] == ".root"]
    ## add style options and create the canvas
    options = add_options_from_configuration(options)
    if "filenames" in dir(options):
        if filenames_from_interface:
            print "Warning: filenames parameter defined in configuration;"
            print "         filenames on the command line will be ignored."
    else:
        options.filenames = filenames_from_interface
    files = open_rootfiles(options.filenames)
    ## if no filenames provided, just display the help message
    if len(options.filenames) == 0:
        parser.print_help()
        sys.exit(0)
    options = process_options(options)
    plots_to_make = process_directory('', files, options)
    options.nplots = len(plots_to_make)
    if use_multiprocessing:
        queue = multi.JoinableQueue()
        queue_globals = multi.Manager().Namespace()
        queue_globals.nfinished = 0
        qargs = (queue, queue_globals, options)
        for args in plots_to_make:
            queue.put(args)
        for i in range(options.processors):
            p = multi.Process(target=plotting_worker,
                              name="worker-%i"%i, args=qargs)
            p.daemon = True
            p.start()
        queue.join()
    else:
        for i, args in enumerate(plots_to_make):
            process_hist(*args, **{'options':options})
            report_progress(i, options.nplots, options.output, options.ext)
    report_progress(options.nplots, options.nplots, options.output, options.ext)
    print ''
    if options.ext in ['png', 'gif']:
        try:
            set
        except NameError:
            import sets
        dirs = set([''])
        for path, name, counter in plots_to_make:
            while path.rfind('/') != -1:
                dirs.add(path)
                path = path[:path.rfind('/')]
        for directory in dirs:
            make_html_index(options.output, directory, options.ext,
                            options.stylesheet, options.ncolumns_html)
    if options.merge:
        merge_pdf(options.output, plots_to_make)


if __name__ == '__main__':
    if '--timing' in sys.argv:
        sys.argv.remove('--timing')
        try:
            import cProfile
        except ImportError:
            import profile
            profile.run('main()', 'timing')
        else:
            cProfile.run('main()', 'timing')
        import pstats
        p = pstats.Stats('timing')
        p.sort_stats('cumulative').print_stats(25)
    else:
        main()

