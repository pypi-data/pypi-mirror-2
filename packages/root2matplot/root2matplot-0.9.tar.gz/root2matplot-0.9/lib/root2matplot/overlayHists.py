#!/usr/bin/env python
"""
Draw histograms to image files, specifying options on the command line.

You can overlay plots from multiple ROOT files with identical structure.
"""
__version__ = '1.4'

## Created by Jeff Klukas (klukas@wisc.edu), November 2009
## Updated March 2010


######## Import python libraries #############################################

import sys
import optparse
import shutil
import math
import os
import re

try:
    import multiprocessing
    from Queue import Empty
    use_multiprocessing = True
except ImportError:
    use_multiprocessing = False

## If we actually plan to do something other than show the help menu, 
## import the PyROOT package
if '-h' not in sys.argv and len(sys.argv) > 1:
    import ROOT
    # ROOT parses options when the first ROOT command is called, so we must
    # add '-b' before that to get batch mode, but we must immediately remove
    # it to avoid interference with option parsing for this script.
    sys.argv.append('-b')
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    sys.argv.remove('-b')
    if os.path.exists('rootlogon.C'):
        ROOT.gROOT.Macro('rootlogon.C')


######## Define styles #######################################################

default_styles=r"""
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

##############################################################################
######## Pretty File Names ###################################################

## For more complex needs, you may want to specify a list of files along with
## more descriptive names for the legend using the filenames option.  When
## enabled, any filenames on the command line will be ignored.

## filenames = [
##     ('histTTbar.root', r'$\bar{t}t$'),
##     ('histZmumu.root', r'$Z\rightarrow\mu\mu$'),
##     ]

##############################################################################
######## Global Style Options ################################################

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

#### Styles for --data
data_color = (0,0,0)
mc_color = (231, 139, 77)
data_fmt = 'o'       # Choose marker for matplotlib
data_marker = 4      # Choose marker for ROOT

#### Titles produced by --area-normalize and --normalize
area_normalized_title = "Fraction of Events in Bin"
file_normalized_title = "Events Normalized to %s"
scale_normalized_title = "Events Scaled by %d"

#### Overflow and underflow text labels
overflow_text = " Overflow"
underflow_text = " Underflow"
overflow_size = 'small'
overflow_alpha = 0.5       # For matplotlib output

#### Ratio plot
ratio_fraction = 0.3

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

##############################################################################
######## matplotlib Output ###################################################

alpha = 0.5 # Used for bar, hist

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
    def Get(self, object_name):
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
def process_directory(path, files):
    """Loop through all histograms in the directory and plot them."""
    dir_to_make = '%s/%s' % (options.plot_dir, path)
    keys = files[0].file.GetDirectory(path).GetListOfKeys()
    key = keys[0]
    plots_to_make = []
    while key:
        obj = key.ReadObj()
        key = keys.After(key)
        name = obj.GetName()
        new_path = '%s/%s' % (path, name)
        if obj.IsA().InheritsFrom('TDirectory'):
            plots_to_make += process_directory(new_path, files)
        #### If obj is a desired histogram, process it
        matches_path = options.regex.search(new_path)
        is_1D_histogram = (obj.IsA().InheritsFrom('TH1') and
                           not obj.IsA().InheritsFrom('TH2') and
                           not obj.IsA().InheritsFrom('TH3'))
        if (matches_path and is_1D_histogram):
            if not os.path.exists(dir_to_make):
                os.makedirs(dir_to_make)
            counter = next_counter() # used for page numbers
            plots_to_make += [(path, name, counter)]
    return plots_to_make

#### Handle multiprocessing
def plotting_worker(queue):
    """Handle a single plot, communicating with the queue."""
    while True:
        try:
            args = queue.get(timeout=5)
        except Empty:
            break
        process_hist(*args)
        queue.task_done()

#### This is where all the plotting actually happens
def process_hist(path, name, counter):
    if options.mpl:
        process_hist_matplotlib(path, name, counter)
    else:
        process_hist_root(path, name, counter)

def process_hist_root(path, name, counter):
    """Overlay all the instances of this plot in ROOT and apply the options."""
    try:
        files = [RootFile(filename) for filename in options.filenames]
    except TypeError:
        files = [RootFile(filename, displayname) for filename, displayname
                 in options.filenames]
    global canvas
    canvas = ROOT.TCanvas()
    hist = files[0].file.GetDirectory(path).Get(name)
    title = hist.GetTitle()
    x_title = hist.GetXaxis().GetTitle()
    y_title = hist.GetYaxis().GetTitle()
    if options.title:
        if options.title[0] == '+':
            title += options.title[1:]
        else:
            title = options.title
    if options.xlabel:
        if options.xlabel[0] == '+':
            x_title += options.xlabel[1:]
        else:
            x_title = options.xlabel
    if options.ylabel:
        if options.xlabel[0] == '+':
            y_title += options.ylabel[1:]
        else:
            y_title = options.ylabel
    if options.area_normalize or (options.sticky and 'Norm' in name):
        y_title = options.area_normalized_title
    if options.normalize:
        if type(options.normalize) == type(int()):
            file_name = files[options.normalize - 1].name
            y_title = options.file_normalized_title % file_name
        else:
            y_title = options.scale_normalized_title % options.normalize
    hists = []
    #### Apply options to hist from each file
    for i, file in enumerate(files):
        hist = file.file.GetDirectory(path).Get(name)
        if not hist: continue
        hist.SetTitle(file.name)
        if options.efficiency_from:
            denom = file.file.Get(options.efficiency_from)
            nbins = hist.GetNbinsX();
            num = [hist.GetBinContent(j) for j in range(1, nbins + 1)]
            den = [denom.GetBinContent(j) for j in range(1, nbins + 1)]
            eff, up, down = wilson(num, den)
            for j in range(nbins):
                hist.SetBinContent(j + 1, eff[j])
                hist.SetBinError(j + 1, max(up[j], down[j]))
        color = ROOT.TColor.GetColor(*options.colors[i][0:3])
        hist.SetLineColor(color)
        if options.fill or (options.data and (i+1) != options.data):
            color = ROOT.TColor.GetColor(*options.mc_color[0:3])
            hist.SetLineColor(color)
            hist.SetFillColor(color)
            hist.SetFillStyle(1001)
        if options.markers:
            hist.SetMarkerColor(color)
            hist.SetMarkerStyle(options.marker_styles[i])
        else:
            hist.SetMarkerSize(0)
        if options.overflow or (options.sticky and 'Overflow' in name):
            nbins = hist.GetNbinsX()
            overflow = hist.GetBinContent(nbins + 1)
            hist.AddBinContent(nbins, overflow)
        if options.underflow or (options.sticky and 'Underflow' in name):
            underflow = hist.GetBinContent(0)
            hist.AddBinContent(1, underflow)
        if options.area_normalize or (options.sticky and 'Norm' in name):
            integral = hist.Integral()
            if integral: hist.Scale(1. / integral)
        hists.append(hist)
    if options.normalize:
        if type(options.normalize) == type(int()):
            integral = hists[options.normalize - 1].Integral()
            if integral:
                for hist in hists:
                    hist.Scale(integral / hist.Integral())
        else:
            hist.Scale(options.normalize)
    #### Combine hists in a THStack and draw
    pads = [canvas]
    stack = ROOT.THStack('st%.3i' % counter, title)
    legend_height = min(options.legend_entry_height * len(files) + 0.02,
                        options.max_legend_height)
    if type(options.legend) == type(int()):
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
        legend_loc = [left, bottom, right, top]
    else:
        legend_loc = [0,0,0,0]
    legend = ROOT.TLegend(*legend_loc)
    for i, hist in enumerate(hists):
        if (i+1) != options.data:
            stack.Add(hist)
        legend.AddEntry(hist)
    stack.Draw(options.draw)
    stack.GetXaxis().SetTitle(x_title)
    stack.GetYaxis().SetTitle(y_title)
    if options.ratio or (options.sticky and 'Ratio' in name):
        pads, stack, stack_ratio = add_ratio_plot(hists, stack, counter)
        pads[1].cd()
        stack_ratio.Draw(options.draw)
        pads[0].cd()
    pads[0].SetLogx(options.logx or (options.sticky and 'Logx' in name))
    pads[0].SetLogy(options.logy or (options.sticky and 'Logy' in name))
    stack.Draw(options.draw)
    if options.efficiency or (options.sticky and 'Eff' in name):
        stack.Draw(options.draw + 'e')
        stack.SetMaximum(1.)
        stack.SetMinimum(0.)
    if options.data:
        color = ROOT.TColor.GetColor(*options.data_color[0:3])
        hists[options.data - 1].SetLineColor(color)
        hists[options.data - 1].SetMarkerColor(color)
        hists[options.data - 1].SetMarkerStyle(options.data_marker)
        hists[options.data - 1].SetMarkerSize(ROOT.gStyle.GetMarkerSize())
        if hists[options.data - 1].GetMaximum() > stack.GetMaximum():
            stack.SetMaximum(hists[options.data - 1].GetMaximum() * 1.2)
        hists[options.data - 1].Draw('same e')
    if options.numbering:
        display_page_number(counter)
    if options.overflow or (options.sticky and 'Overflow' in name):
        display_overflow(stack, hist)
    if options.underflow or (options.sticky and 'Underflow' in name):
        display_underflow(stack, hist)
    legend.Draw()
    save_plot(stack, options.plot_dir, path, name, counter)

#### This is where all the plotting actually happens
def process_hist_matplotlib(path, name, counter):
    """Overlay all the instances of this plot and output using matplotlib."""
    try:
        files = [RootFile(filename) for filename in options.filenames]
    except TypeError:
        files = [RootFile(filename, displayname) for filename, displayname
                 in options.filenames]
    xpos = options.size.find('x')
    width = float(options.size[:xpos])
    height = float(options.size[xpos+1:])
    plt.figure(1, figsize=(width, height))
    ax = plt.axes()
    ax.cla()
    hists = []
    stack = r2m.HistStack()
    #### Apply options to hist from each file
    for i, file in enumerate(files):
        title, xlabel, ylabel = '', '', ''
        if options.title:
            if options.title[0] == "+":
                title += options.title[1:]
            else:
                title = options.title
        if options.xlabel:
            if options.xlabel[0] == "+":
                xlabel += options.xlabel[1:]
            else:
                xlabel = options.xlabel
        if options.ylabel:
            if options.ylabel[0] == "+":
                ylabel += options.ylabel[1:]
            else:
                ylabel = options.ylabel
        if options.normalize:
            if type(options.normalize) == type(int()):
                file_name = files[options.normalize - 1].name
                ylabel = options.file_normalized_title % file_name
            else:
                ylabel = options.scale_normalized_title % options.normalize
        hist = r2m.Hist(file.file.GetDirectory(path).Get(name),
                        replace=options.replace, title=title,
                        xlabel=xlabel, ylabel=ylabel)
        hists.append(hist)
    for i, file in enumerate(files):
        hist = hists[i]
        if options.efficiency_from:
            denom = r2m.Hist(file.file.Get(options.efficiency_from))
            eff, up, down = wilson([sum(hist.y)], [sum(denom.y)])
            hist.label += (" ($%.1f \pm %.1f\\%%$)" %
                           (eff[0] * 100., max(up[0], down[0]) * 100.))
            hist.y, up, down = wilson(hist.y, denom.y)
            hist.yerr = np.array([up, down])
        if options.overflow or (options.sticky and 'Overflow' in name):
            hist.y[-1] += hist.overflow
        if options.underflow or (options.sticky and 'Underflow' in name):
            hist.y[0] += hist.underflow
        if options.area_normalize or (options.sticky and 'Norm' in name):
            hist.y /= sum(hist.y)
        if options.normalize:
            if type(options.normalize) == type(int()):
                hist.scale(sum(hists[options.normalize - 1]) / sum(hist.y))
            else:
                hist.scale(options.normalize)
        if options.markers: fmt = options.marker_styles[i]
        else:               fmt = 'o'
        if options.data and (i+1) == options.data:
            datahist = hist
            datahist.label = file.name
        else:
            color = options.colors[i]
            if options.data:
                color = options.mc_color
            stack.add(hist, label=file.name, color=color, fmt=fmt)
    if options.errorbar:
        if options.data:
            try:
                stack.hist(histtype='stepfilled')
            except ValueError:
                pass
            datahist.errorbar(yerr=True, fmt=options.data_fmt,
                              color=options.data_color)
        else:
            plots = stack.errorbar(yerr=True)
    if options.stack:
        stack.barstack()
    if options.bar:
        stack.bar(alpha=options.alpha)
    if options.hist:
        try:
            stack.hist(alpha=options.alpha, histtype='stepfilled')
        except ValueError:
            pass
    if options.efficiency:
        plt.ylim(0, 1)
    plt.xlim(hist.xedges[0], hist.xedges[-1])
    if options.logx: ax.set_xscale('log')
    if options.logy: ax.set_yscale('log')
    if options.numbering:
        plt.text(0.98, 0.98, counter, transform=plt.figure(1).transFigure,
                 size="small", ha='right', va='top')
    if options.overflow or (options.sticky and 'Overflow' in name):
        plt.text(hist.x[-1], plt.ylim()[0], options.overflow_text,
                 rotation='vertical', ha='center',
                 alpha=options.overflow_alpha, size=options.overflow_size)
    if options.underflow or (options.sticky and 'Underflow' in name):
        plt.text(hist.x[0], plt.ylim()[0], options.underflow_text,
                 rotation='vertical', ha='center',
                 alpha=options.overflow_alpha, size=options.overflow_size)
    stack.show_titles()
    if options.legend != 'None':
        plt.legend(numpoints=1, loc=options.legend)
    output_file_name = '%s/%s/%s' % (options.plot_dir, path, name)
    plt.savefig(output_file_name, transparent=options.transparent,
                dpi=options.dpi)
    if options.ext == "pdf":
        shutil.copy("%s.pdf" % output_file_name, "%.3i.pdf" % counter)
    report_progress(counter)



######## Define some supporting functions #####################################

def save_plot(stack, plot_dir, path, name, counter):
    """Save the canvas to the output format defined by --ext."""
    output_file_name = '%s/%s/%s.%s' % (plot_dir, path, name, options.ext)
    canvas.SaveAs(output_file_name)
    if options.ext == 'pdf':
        numbered_pdf_name = '%.3i.pdf' % counter
        shutil.copy(output_file_name, numbered_pdf_name)
    report_progress(counter)

def report_progress(counter, divisor=1):
    """Print the current number of finished plots."""
    if counter % divisor == 0:
        print "\r%i plots of %i written to %s/" % (counter, options.nplots,
                                                   options.output),
        sys.stdout.flush()

def merge_pdf():
    """Merge together all the produced plots into one pdf file."""
    if "001.pdf" not in os.listdir('.'):
        print "No output files, so no merged pdf was made"
        return
    print "Writing %s.pdf..." % options.output
    os.system('gs -q -dBATCH -dNOPAUSE -sDEVICE=pdfwrite '
              '-dAutoRotatePages=/All '
              '-sOutputFile=%s.pdf ' % options.output +
              '[0-9][0-9][0-9].pdf')
    os.system('rm [0-9]*.pdf')

def display_page_number(page_number):
    """Add a page number to the top corner of the canvas."""
    page_text = ROOT.TText()
    page_text.SetTextSize(0.03)
    page_text.SetTextAlign(33)
    page_text.DrawTextNDC(0.97, 0.985, '%i' % page_number)

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

def add_ratio_plot(hists, stack, counter):
    """Divide canvas into two parts, and plot the ratio on the bottom."""
    ## Both pads are set to the full canvas size to maintain font sizes
    ## Fill style 4000 used to ensure pad transparency because of this
    div = options.ratio_fraction
    margins = [ROOT.gStyle.GetPadTopMargin(), ROOT.gStyle.GetPadBottomMargin()]
    useable_height = 1 - (margins[0] + margins[1])
    canvas.Clear()
    pad = ROOT.TPad('mainPad', 'mainPad', 0., 0., 1., 1.)
    pad.SetFillStyle(4000)
    pad.Draw()
    pad.SetBottomMargin(margins[1] + div * useable_height)
    pad_ratio = ROOT.TPad('ratioPad', 'ratioPad', 0., 0., 1., 1.);
    pad_ratio.SetFillStyle(4000)
    pad_ratio.Draw()
    pad_ratio.SetTopMargin(margins[0] + (1 - div) * useable_height)
    pad.cd()
    stack.Draw()
    stack_ratio = ROOT.THStack('stRatio%.3i' % counter,
                               ';%s;Ratio' % stack.GetXaxis().GetTitle())
    for hist in hists[1:]:
        ratio_hist = hist.Clone()
        ratio_hist.Divide(hists[0])
        stack_ratio.Add(ratio_hist)
    stack_ratio.Draw()
    stack_ratio.GetYaxis().SetNdivisions(507) # Avoids crowded labels
    stack.GetXaxis().SetBinLabel(1, '') # Don't show numbers below top plot
    stack.GetXaxis().SetTitle('')
    if stack.GetYaxis().GetTitle() == '':
        stack.GetYaxis().SetTitle('Content')
    # Avoid overlap of y-axis numbers by supressing zero
    if stack.GetMinimum() / stack.GetMaximum() < 0.25:
        stack.SetMinimum(stack.GetMaximum() / 10000)
    return [pad, pad_ratio], stack, stack_ratio

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

def add_options_from_configuration(options):
    """Define a set of global variables storing style information"""
    def append_to_options(config, options):
        for attribute in dir(config):
            if '__' not in attribute:
                attr = getattr(config, attribute)
                setattr(options, attribute, attr)
        return options
    f = open('default_overlay_config.py', 'w')
    f.write(default_styles)
    f.close()
    if options.config:
        os.rename('default_overlay_config.py', 'overlayHists_config.py')
        print "Wrote overlayHists_config.py to the current directory"
        sys.exit(0)
    sys.path.insert(0, '')
    import default_overlay_config
    options = append_to_options(default_overlay_config, options)
    os.remove('default_overlay_config.py')
    os.remove('default_overlay_config.pyc')
    sys.path.insert(0, '')
    for f in options.config_files:
        user_config = __import__(f[:-3])
        options = append_to_options(user_config, options)
    return options

def process_options(options):
    nfiles = len(options.filenames)
    mpl_option_activated = (options.stack or options.errorbar or
                            options.bar or options.hist)
    if options.mpl:
        if not mpl_option_activated:
            options.errorbar = True
    else:
        options.mpl = mpl_option_activated
    try:
        global matplotlib
        import matplotlib
        if options.ext == "png":
            matplotlib.use('AGG')
        if options.ext == "pdf":
            matplotlib.use('PDF')
        if options.ext == "ps":
            matplotlib.use('PS')
        imported_matplotlib = True
    except ImportError:
        if options.mpl:
            print("Unable to load matplotlib, "
                  "which is required for these options")
            sys.exit(1)
        imported_matplotlib = False
    if options.mpl:
        try:
            global r2m, np, plt
            import root2matplot as r2m
            import numpy as np
            from matplotlib import pyplot as plt
            options.marker_styles = options.markers_matplotlib
        except ImportError:
            print("Unable to load root2matplot, "
                  "which is required for operation with matplotlib")
            sys.exit(1)
    else:
        options.marker_styles = options.markers_root
    if imported_matplotlib:
        if options.colormap:
            cmap = plt.get_cmap(options.colormap)
            if options.ncolors < nfiles:
                options.ncolors = nfiles
            options.colors = [cmap(float(i)/options.ncolors)
                              for i in range(nfiles)]
        else:
            options.colors = [[value/256. for value in options.colors[i]]
                              for i in range(nfiles)]
            options.ncolors = len(options.colors)
            if nfiles > options.ncolors:
                print "Not enough colors defined!"
                sys.exit(1)
    if options.normalize:
        if '.' in options.normalize:
            options.normalize = float(options.normalize)
        else:
            options.normalize = int(options.normalize)
    if options.efficiency_from:
        options.efficiency = True
    return options


######## Define the main program #############################################

def main():
    usage="""usage: %prog [options] [style_config.py] [file1.root ...]

Documentation: http://packages.python.org/root2matplot/

Function: overlays corresponding histograms from several files, dumping the
  images into a directory structure that mirrors that of the ROOT file and,
  if output format is pdf, also merging all images into a single file.
  Most style options can be controlled from your rootlogon.C macro.

Power users: advanced operation using configuration files is described in the
  full online documentation.  This allows you control over colors, styles,
  names for the legends, and more.  Get the default config with --config.

Matplotlib: if you have the matplotlib python plotting library installed on your
  system, you can produce output in matplotlib.  By activating any of the
  options 'bar', 'errorbar', 'hist', or 'stack', output will be produced in
  matplotlib."""
    
    parser = optparse.OptionParser(usage=usage, 
                                   version='%s %s' % ('%prog', __version__))
    parser.add_option('--config', action="store_true",
                      help="do nothing but write a template configuration file "
                      "called overlayHists_config.py")
    parser.add_option('-e', '--ext', default='pdf', 
                      help="choose an output extension; default is pdf")
    parser.add_option('-m', '--markers', action='store_true', default=False,
                      help="add markers to histograms")
    parser.add_option('-s', '--sticky', action='store_true', default=False,
                      help="enable name-based special plotting options "
                      "(see below)")
    parser.add_option('--data', default=0, type='int', metavar='FILENUM',
                      help="The histogram from file #FILENUM (starting from 1) "
                      "will be drawn as black datapoints, while all others "
                      "will be filled, as is the custom for showing data vs. "
                      "Monte Carlo.")
    parser.add_option('--output', default='overlaidHists', metavar='NAME',
                      help="name of output directory; default is "
                      "'overlaidHists'")
    parser.add_option('--numbering', action='store_true', default=False,
                      help="add a page number in the upper right of each plot")
    parser.add_option('--path', default='', 
                      help="only process plot(s) in the given location or in "
                      "subdirectories; PATH may be a regular expression (use "
                      ".* for wildcard)")
    parser.add_option('--normalize', metavar='VALUE',
                      help="if integer, normalize to the VALUEth file "
                      "(starting with 1); if float, scale by VALUE")
    parser.add_option('--colormap', default=None,
                      help="Select colors from the given matplotlib "
                      "colormap rather than the defaults")
    parser.add_option('--ncolors', type=int, default=None,
                      help="The number of colors with which to divide the "
                      "colormap")
    parser.add_option('--legend', default=1, metavar="LOC",
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
    parser.add_option('--efficiency-from', default=None, metavar="DENOM",
                      help="Divide all plots by the histogram in path DENOM")
    group1 = optparse.OptionGroup(
        parser,
        "Special plotting options",
        "Use the command line options given below to apply changes to all "
        "plots.  If you only wish to apply an option to a specific plot, "
        "you can use '-s' "
        "to turn on sticky keywords (such as 'Norm').  Any plot that includes "
        "the given keyword in its ROOT name will have the option applied "
        "regardless of its presence or absence on the command line.  "
        "'ratio' is currently only available in ROOT output."
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
    group1.add_option('--overflow', action='store_true', default=False,
                      help="'Overflow' : display overflow content in "
                      "highest bin")
    group1.add_option('--underflow', action='store_true', default=False,
                      help="'Underflow': display underflow content in "
                      "lowest bin")
    group1.add_option('--ratio', action='store_true', default=False,
                      help="'Ratio': display a ratio plot below the normal "
                      "plot")
    group2 = optparse.OptionGroup(parser,
                                "Options specific to ROOT (default) output")
    group2.add_option('--draw', default='nostack p H',
                      help="pass DRAW to ROOT's Draw command; default is "
                      "'nostack p H'; try 'nostack e' for error bars")
    group2.add_option('-f', '--fill', action='store_true', default=False,
                      help="Histograms will have a color fill")
    group3 = optparse.OptionGroup(parser,
                                "Producing output with matplotlib")
    group3.add_option('--mpl', action="store_true", default=False,
                      help="produce output in matplotlib; automatically "
                      "turned on by --stack, --errorbar, --bar, or --hist")
    group3.add_option('--stack', action="store_true", default=False,
                      help="output a matplotlib stacked bar graph")
    group3.add_option('--errorbar', action="store_true", default=False,
                      help="output a matplotlib errorbar graph")
    group3.add_option('--bar', action="store_true", default=False,
                      help="output a matplotlib bar graph")
    group3.add_option('--hist', action="store_true", default=False,
                      help="output a matplotlib hist graph (with solid fill)")
    group3.add_option('--transparent', action="store_true", default=False,
                      help="use a transparent background")
    group3.add_option('--size', default='6x4.5',
                      help="Define the plot size as "
                      "'width x height' in inches; default is '6x4.5'")
    group3.add_option('--dpi', default=None,
                      help="Set the resolution of matplotlib output (default "
                      "is 100)")
    parser.add_option_group(group2)
    parser.add_option_group(group3)
    parser.add_option_group(group1)
    global options
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
    try:
        files = [RootFile(filename) for filename in options.filenames]
    except TypeError:
        files = [RootFile(filename, displayname) for filename, displayname
                 in options.filenames]
    ## if no filenames provided, just display the help message
    if len(options.filenames) == 0:
        parser.print_help()
        sys.exit(0)
    options = process_options(options)
    ## here, we decend into the files to start plotting
    plots_to_make = process_directory('', files)
    options.nplots = len(plots_to_make)
    if use_multiprocessing:
        queue = multiprocessing.JoinableQueue()
        for args in plots_to_make:
            queue.put(args)
        for i in range(4):
            p = multiprocessing.Process(target=plotting_worker,
                                        name="worker-%i"%i, args=(queue,))
            p.daemon = True
            p.start()
        queue.join()
    else:
        for args in plots_to_make:
            process_hist(*args)
    print "\r%i plots of %i written to %s/" % (options.nplots, options.nplots,
                                               options.output)
    if options.ext == 'pdf':
        merge_pdf()


if __name__ == '__main__':
    if '--timing' in sys.argv:
        sys.argv.remove('--timing')
        try:
            import cProfile
            cProfile.run('main()', 'timing')
        except ImportError:
            import profile
            profile.run('main()', 'timing')
        import pstats
        p = pstats.Stats('timing')
        p.sort_stats('cumulative').print_stats(25)
    else:
        main()

