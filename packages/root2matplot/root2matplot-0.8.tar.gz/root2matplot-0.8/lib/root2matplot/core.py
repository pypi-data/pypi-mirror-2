"""
Core implementation of the module
"""

################ Import python libraries

import math
import numpy as np
import matplotlib as mpl
import ROOT
import re
import copy


################ Define constants

_all_whitespace_string = re.compile(r'\s*$')


################ Define classes

class Hist2D(object):
    """A container to hold the paramters from a 2D ROOT histogram."""
    def __init__(self, hist, label="__nolabel__", title=None,
                 xlabel=None, ylabel=None):
        try:
            if not hist.InheritsFrom("TH2"):
                raise TypeError("%s does not inherit from TH2" % hist)
        except:
            raise TypeError("%s is not a ROOT object" % hist)
        array = np.array
        self.nbinsx = nx = hist.GetNbinsX()
        self.nbinsy = ny = hist.GetNbinsY()
        self.binlabelsx = _process_bin_labels([hist.GetXaxis().GetBinLabel(i)
                                               for i in range(1, nx + 1)])
        if self.binlabelsx:
            self.nbinsx = nx = self.binlabelsx.index('')
            self.binlabelsx = self.binlabelsx[:ny]
        self.binlabelsy = _process_bin_labels([hist.GetYaxis().GetBinLabel(i)
                                               for i in range(1, ny + 1)])
        if self.binlabelsy:
            self.nbinsy = ny = self.binlabelsy.index('')
            self.binlabelsy = self.binlabelsy[:ny]
        self.content = array([array([hist.GetBinContent(i, j)
                                     for i in range(1, nx + 1)])
                              for j in range(1, ny + 1)])
        self.xedges = array([hist.GetXaxis().GetBinLowEdge(i)
                             for i in range(1, nx + 2)])
        self.yedges = array([hist.GetYaxis().GetBinLowEdge(i)
                             for i in range(1, ny + 2)])
        self.x      = array([(self.xedges[i+1] + self.xedges[i])/2
                             for i in range(nx)])
        self.y      = array([(self.yedges[i+1] + self.yedges[i])/2
                             for i in range(ny)])
    def contour(self, **kwargs):
        """Draw a contour plot."""
        _load_pyplot()
        cs = plt.contour(self.x, self.y, self.content, **kwargs)
        plt.clabel(cs, inline=1, fontsize=10)
        if self.binlabelsx is not None:
            plt.xticks(np.arange(self.nbinsx), self.binlabelsx)
        if self.binlabelsy is not None:
            plt.yticks(np.arange(self.nbinsy), self.binlabelsy)
        return cs
    def col(self, **kwargs):
        """Draw a colored box plot using pyploy.imshow."""
        _load_pyplot()
        plot = plt.imshow(self.content, interpolation='nearest',
                          extent=[self.xedges[0], self.xedges[-1],
                                  self.yedges[0], self.yedges[-1]],
                          aspect='auto', origin='lower', **kwargs)
        return plot
    def colz(self, **kwargs):
        """Draw a colored box plot with a colorbar using pyplot.imshow."""
        plot = self.col(**kwargs)
        plt.colorbar(plot)
        return plot
    def box(self, maxsize=40, **kwargs):
        """
        Draw a box plot with size indicating content using pyplot.scatter.

        The data will be normalized, with the largest box using a marker of
        size maxsize (in points).
        """
        _load_pyplot()
        x = np.hstack([self.x for i in range(self.nbinsy)])
        y = np.hstack([[yval for i in range(self.nbinsx)] for yval in self.y])
        maxvalue = np.max(self.content)
        sizes = self.content.flatten() / maxvalue * maxsize
        plot = plt.scatter(x, y, sizes, marker='s', **kwargs)
        return plot
        
class Hist(object):
    """A container to hold the parameters from a ROOT histogram."""
    def __init__(self, hist, replace=None, label="__nolabel__", title=None,
                 xlabel=None, ylabel=None):
        try:
            if not hist.InheritsFrom("TH1"):
                raise TypeError("%s does not inherit from TH1" % hist)
        except:
            raise TypeError("%s is not a ROOT object" % hist)
        array = np.array
        self.nbins  = n = hist.GetNbinsX()
        self.binlabels = _process_bin_labels([hist.GetXaxis().GetBinLabel(i)
                                         for i in range(1, n + 1)])
        if self.binlabels:
            # Get rid of extra non-labeled bins
            self.nbins = n = self.binlabels.index('')
            self.binlabels = self.binlabels[:n]
        self.xedges = array([hist.GetBinLowEdge(i) for i in range(1, n + 2)])
        self.x      = array([(self.xedges[i+1] + self.xedges[i])/2
                             for i in range(n)])
        self.xerr   = array([(self.xedges[i+1] - self.xedges[i])/2
                             for i in range(n)])
        self.y      = array([hist.GetBinContent(i) for i in range(1, n + 1)])
        self.yerr   = array([hist.GetBinError(  i) for i in range(1, n + 1)])
        self.width  = array([self.xedges[i+1] - self.xedges[i]
                             for i in range(self.nbins)])
        self.underflow = hist.GetBinContent(0)
        self.overflow  = hist.GetBinContent(self.nbins + 1)
        self.title  = _parse_latex(hist.GetTitle(), replace)
        self.xlabel = _parse_latex(hist.GetXaxis().GetTitle(), replace)
        self.ylabel = _parse_latex(hist.GetYaxis().GetTitle(), replace)
        if title : self.title  = _parse_latex(title, replace)
        if xlabel: self.xlabel = _parse_latex(xlabel, replace)
        if ylabel: self.ylabel = _parse_latex(ylabel, replace)
        self.label = _parse_latex(label, replace)
    def __getitem__(self, index):
        """Return the contents of the indexth bin."""
        return self.y[index]
    def __setitem__(self, index, value):
        """Set the contents of the indexth bin."""
        self.y[index] = value
    def __len__(self):
        """Return the number of bins."""
        return self.nbins
    def __iter__(self):
        """Return the contents of the bins."""
        return iter(self.y)
    def show_titles(self):
        """Add the titles defined in the ROOT histogram to the figure."""
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
    def delete_bin(self, index):
        """
        Delete a the contents of a bin, sliding all the other data one bin to
        the left.  This can be useful for histograms with labeled bins.
        """
        self.nbins -= 1
        self.xedges = self.xedges[:-1]
        self.x = self.x[:-1]
        self.width = self.width[:-1]
        self.y = np.delete(self.y, index)
        self.xerr = np.delete(self.xerr, index)
        self.yerr = np.delete(self.yerr, index)
        if self.binlabels:
            self.binlabels.pop(index)
    def hist(self, **kwargs):
        """
        Generate a matplotlib hist figure.

        All additional keyword arguments will be passed to pyplot.hist.
        """
        _load_pyplot()
        plot = plt.hist(self.x, weights=self.y, bins=self.xedges,
                        label=self.label, **kwargs)
        if self.binlabels is not None:
            plt.xticks(np.arange(self.nbins), self.binlabels)
        plt.xlim(self.xedges[0], self.xedges[-1])
        return plot
    def errorbar(self, xerr=False, yerr=False, **kwargs):
        """
        Generate a matplotlib errorbar figure.

        All additional keyword arguments will be passed to pyplot.errorbar.
        """
        if xerr:
            kwargs['xerr'] = self.xerr
        if yerr:
            kwargs['yerr'] = self.yerr
        _load_pyplot()
        errorbar = plt.errorbar(self.x, self.y, label=self.label, **kwargs)
        if self.binlabels is not None:
            plt.xticks(np.arange(self.nbins), self.binlabels)
        plt.xlim(self.xedges[0], self.xedges[-1])
        return errorbar
    def errorbarh(self, xerr=False, yerr=False, **kwargs):
        """
        Generate a horizontal matplotlib errorbar figure.

        All additional keyword arguments will be passed to pyplot.errorbar.
        """
        if xerr: kwargs['xerr'] = self.yerr
        if yerr: kwargs['yerr'] = self.xerr
        _load_pyplot()
        errorbar = plt.errorbar(self.y, self.x, label=self.label, **kwargs)
        if self.binlabels is not None:
            plt.yticks(np.arange(self.nbins), self.binlabels)
        plt.ylim(self.xedges[0], self.xedges[-1])
        return errorbar
    def bar(self, xerr=False, yerr=False, **kwargs):
        """
        Generate a matplotlib bar figure.

        All additional keyword arguments will be passed to pyplot.bar.
        """
        if xerr: kwargs['xerr'] = self.xerr
        if yerr: kwargs['yerr'] = self.yerr
        _load_pyplot()
        bar = plt.bar(self.xedges[0:-1], self.y, self.width, label=self.label,
                      **kwargs)
        return bar
    def barh(self, xerr=False, yerr=False, yoffset=0., width=0.8, **kwargs):
        """
        Generate a horizontal matplotlib bar figure.

        All additional keyword arguments will be passed to pyplot.barh.
        """
        if xerr: kwargs['xerr'] = self.yerr
        if yerr: kwargs['yerr'] = self.xerr
        _load_pyplot()
        xcontent = [self.xedges[i] + self.width[i] * yoffset
                    for i in range(len(self.xedges) - 1)]
        width = self.width * width
        barh = plt.barh(xcontent, self.y, width, label=self.label,
                       **kwargs)
        if self.binlabels is not None:
            plt.yticks(np.arange(self.nbins), self.binlabels)
        return barh
    def TH1F(self, name=""):
        """Return a ROOT.TH1F object with the contents of this Hist"""
        th1f = ROOT.TH1F(name, "", self.nbins, self.xedges)
        th1f.SetTitle("%s;%s;%s" % (self.title, self.xlabel, self.ylabel))
        for i in range(self.nbins):
            th1f.SetBinContent(i + 1, self.y[i])
        return th1f
    def divide_wilson(self, denominator):
        """
        Return an efficiency plot with Wilson score interval errors.

        This function is called by the division operator:
          hist3 = hist1.divide_wilson(hist2) <--> hist3 = hist1/hist2
        """
        eff, upper_err, lower_err = wilson_interval(self.y, denominator.y)
        quotient = copy.deepcopy(self)
        quotient.y = np.array(eff)
        quotient.yerr = np.array([lower_err, upper_err])
        return quotient
    def __div__(self, denominator):
        return self.divide_wilson(denominator)

class HistStack(object):
    """
    A container to hold Hist objects for plotting together.

    When plotting, the title and the x and y labels of the last Hist added
    will be used unless specified otherwise in the constructor.
    """
    def __init__(self, hists=None, title=None, xlabel=None, ylabel=None,
                 replace=None):
        self.hists  = []
        self.kwargs = []
        self.title  = _parse_latex(title, replace)
        self.xlabel = _parse_latex(xlabel, replace)
        self.ylabel = _parse_latex(ylabel, replace)
        if hists:
            for hist in hists:
                self.add(hist, replace)
    def __getitem__(self, index):
        """Return the indexth hist in the stack."""
        return self.hists[index]
    def __setitem__(self, index, value):
        """Replace the indexth hist in the stack with value."""
        self.hists[index] = value
    def __len__(self):
        """Return the number of hists in the stack."""
        return len(self.hists)
    def __iter__(self):
        return iter(self.hists)
    def max(self):
        """Return the value of the highest bin of all the hists in the stack."""
        maxes = [max(x) for x in self.hists]
        return max(maxes)
    def min(self):
        """Return the value of the lowest bin of all the hists in the stack."""
        mins = [min(x) for x in self.hists]
        return min(mins)
    def show_titles(self):
        self.hists[-1].show_titles()
    def add(self, hist, replace=None, **kwargs):
        """
        Add a Hist object to this stack.

        Any additional keyword arguments will be added to just this Hist 
        when the stack is plotted.
        """
        if "label" in kwargs:
            hist.label = _parse_latex(kwargs['label'], replace)
            del kwargs['label']
        self.hists.append(hist)
        self.kwargs.append(kwargs)
    def hist(self, **kwargs):
        """
        Make a matplotlib hist plot.

        Any additional keyword arguments will be passed to pyplot.hist, which
        allows a vast array of possibilities.  Particlularly, the histtype
        values such as 'barstacked' and 'stepfilled' give completely different
        results.  You will probably want to include a transparency value
        (i.e. alpha=0.5).
        """
        _load_pyplot()
        contents = np.dstack([hist.y for hist in self.hists])
        xedges = self.hists[0].xedges
        x = np.dstack([hist.x for hist in self.hists])
        labels = [hist.label for hist in self.hists]
        try:
            clist = [item['color'] for item in self.kwargs]
            plt.gca().set_color_cycle(clist)
            ## kwargs['color'] = clist # For newer version of matplotlib
        except: pass
        plot = plt.hist(x, weights=contents, bins=xedges,
                        label=labels, **kwargs)
    def bar3d(self, **kwargs):
        """
        Info
        """
        _load_pyplot()
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = Axes3D(fig)
        plots = []
        labels = []
        for i, hist in enumerate(self.hists):
            if self.title  is not None: hist.title  = self.title
            if self.xlabel is not None: hist.xlabel = self.xlabel
            if self.ylabel is not None: hist.ylabel = self.ylabel
            labels.append(hist.label)
            all_kwargs = copy.copy(kwargs)
            all_kwargs.update(self.kwargs[i])
            all_kwargs.pop('fmt', None)
            bar = ax.bar(hist.x, hist.y, zs=i, zdir='y', width=hist.width,
                         **all_kwargs)
            plots.append(bar)
        #ax.yaxis.set_ticks(np.arange(len(labels)))
        ax.yaxis.set_ticklabels(labels)
        ax.set_ylim3d(-1, len(labels))
        return plots
    def barstack(self, **kwargs):
        """
        Make a matplotlib bar plot, with each Hist stacked upon the last.

        Any additional keyword arguments will be passed to pyplot.bar.
        """
        bottom = None # if this is set to zeroes, it fails for log y
        plots = []
        for i, hist in enumerate(self.hists):
            if self.title  is not None: hist.title  = self.title
            if self.xlabel is not None: hist.xlabel = self.xlabel
            if self.ylabel is not None: hist.ylabel = self.ylabel
            all_kwargs = copy.copy(kwargs)
            all_kwargs.update(self.kwargs[i])
            all_kwargs.pop('fmt', None)
            bar = hist.bar(bottom=bottom, **all_kwargs)
            plots.append(bar)
            if not bottom: bottom = [0. for i in range(self.hists[0].nbins)]
            bottom = [sum(pair) for pair in zip(bottom, hist.y)]
        return plots
    def barh(self, **kwargs):
        """
        Make a horizontal clustered matplotlib bar plot.

        Any additional keyword arguments will be passed to pyplot.barh.
        """
        plots = []
        fullwidth = 0.8
        spacer = (1. - fullwidth) / 2
        width = 0.8 / len(self.hists)
        for i, hist in enumerate(self.hists):
            if self.title  is not None: hist.title  = self.title
            if self.xlabel is not None: hist.ylabel = self.xlabel
            if self.ylabel is not None: hist.xlabel = self.ylabel
            all_kwargs = copy.copy(kwargs)
            all_kwargs.update(self.kwargs[i])
            all_kwargs.pop('fmt', None)
            bar = hist.barh(yoffset=width*i + spacer, width=width, **all_kwargs)
            plots.append(bar)
        return plots
    def errorbar(self, offset=False, **kwargs):
        """
        Make a matplotlib errorbar plot, with all Hists in the stack overlaid.

        Passing 'offset=True' will slightly offset each dataset so overlapping
        errorbars are still visible.  Any additional keyword arguments will
        be passed to pyplot.errorbar.
        """
        plots = []
        _load_pyplot()
        for i, hist in enumerate(self.hists):
            if self.title  is not None: hist.title  = self.title
            if self.xlabel is not None: hist.xlabel = self.xlabel
            if self.ylabel is not None: hist.ylabel = self.ylabel
            all_kwargs = copy.copy(kwargs)
            all_kwargs.update(self.kwargs[i])
            transform = plt.gca().transData
            if offset:
                index_offset = (len(self.hists) - 1)/2.
                pixel_offset = 1./72 * (i - index_offset)
                transform = transforms.ScaledTranslation(
                    pixel_offset, 0, plt.gcf().dpi_scale_trans)
                transform = plt.gca().transData + transform
            errorbar = hist.errorbar(transform=transform, **all_kwargs)
            plots.append(errorbar)
        return plots
    def errorbarh(self, **kwargs):
        """
        Make a horizontal matplotlib errorbar plot, with all Hists in the
        stack overlaid.

        Any additional keyword arguments will be passed to pyplot.errorbar.
        """
        plots = []
        for i, hist in enumerate(self.hists):
            if self.title  is not None: hist.title  = self.title
            if self.xlabel is not None: hist.ylabel = self.xlabel
            if self.ylabel is not None: hist.xlabel = self.ylabel
            all_kwargs = copy.copy(kwargs)
            all_kwargs.update(self.kwargs[i])
            errorbar = hist.errorbarh(**all_kwargs)
            plots.append(errorbar)
        return plots
    def bar(self, **kwargs):
        """
        Make a matplotlib bar plot, with all Hists in the stack overlaid.

        Any additional keyword arguments will be passed to pyplot.bar.  You will
        probably want to include a transparency value (i.e. alpha=0.5).
        """
        plots = []
        for i, hist in enumerate(self.hists):
            if self.title  is not None: hist.title  = self.title
            if self.xlabel is not None: hist.xlabel = self.xlabel
            if self.ylabel is not None: hist.ylabel = self.ylabel
            all_kwargs = copy.copy(kwargs)
            all_kwargs.update(self.kwargs[i])
            all_kwargs.pop('fmt', None)
            bar = hist.bar(**all_kwargs)
            plots.append(bar)
        return plots

    
################ Define functions and classes for navigating within ROOT

class RootFile:
    """A wrapper for TFiles, allowing easier access to methods."""
    def __init__(self, file_name, name=None):
        self.name = name
        if name == None:
            self.name = file_name[:-5]
        self.file = ROOT.TFile(file_name, 'read')
        if self.file.IsZombie():
            raise ValueError("Error opening %s" % file_name)
    def cd(self, directory=''):
        """Make directory the current directory."""
        self.file.cd(directory)
    def get(self, object_name):
        """Return a Hist object from the given path within this file."""
        return Hist(self.file.Get(object_name))

def ls(directory=None):
    """Return a python list of ROOT object names from the given directory."""
    if directory == None:
        keys = ROOT.gDirectory.GetListOfKeys()
    else:
        keys = ROOT.gDirectory.GetDirectory(directory).GetListOfKeys()
    key = keys[0]
    names = []
    while key:
        obj = key.ReadObj()
        key = keys.After(key)
        names.append(obj.GetName())
    return names

def pwd():
    """Return ROOT's present working directory."""
    return ROOT.gDirectory.GetPath()

def get(object_name):
    """Return a Hist object with the given name."""
    return Hist(ROOT.gDirectory.Get(object_name))


################ Define additional helping functions

def _load_pyplot():
    global plt, transforms
    import matplotlib.pyplot as plt
    import matplotlib.transforms as transforms

def _parse_latex(string, replacements):
    """Modify a string based on a dictionary of replacements."""
    if not replacements:
        return string
    for key, value in replacements:
        string = string.replace(key, value)
    if re.match(_all_whitespace_string, string):
        return ""
    return string

def _process_bin_labels(binlabels):
    has_labels = False
    for binlabel in binlabels:
        if binlabel:
            has_labels = True
    if has_labels:
        return binlabels
    else:
        return None

def wilson_interval(numerator_array, denominator_array):
    eff, upper_err, lower_err = [], [], []
    for n, d in zip(numerator_array, denominator_array):
        p = float(n) / d
        s = math.sqrt(p * (1 - p) / d + 1 / (4 * d * d))
        t = p + 1 / (2 * d)
        eff.append(p)
        upper_err.append(-p + 1/(1 + 1/d) * (t + s))
        lower_err.append(+p - 1/(1 + 1/d) * (t - s))
    return eff, upper_err, lower_err

def axes_broken_y(axes, upper_frac=0.5, break_frac=0.02, ybounds=None,
                  xlabel=None, ylabel=None):
    """
    Replace the current axes with a set of upper and lower axes.

    The new axes will be transparent, with a breakmark drawn between them.  They
    share the x-axis.  Returns (upper_axes, lower_axes).

    If ybounds=[ymin_lower, ymax_lower, ymin_upper, ymax_upper] is defined,
    upper_frac will be ignored, and the y-axis bounds will be fixed with the
    specified values.
    """
    def breakmarks(axes, y_min, y_max, xwidth=0.008):
        x1, y1, x2, y2 = axes.get_position().get_points().flatten().tolist()
        segment_height = (y_max - y_min) / 3.
        xoffsets = [0, +xwidth, -xwidth, 0]
        yvalues  = [y_min + (i * segment_height) for i in range(4)]
        # Get color of y-axis
        for loc, spine in axes.spines.iteritems():
            if loc  == 'left':
                color = spine.get_edgecolor()
        for x_position in [x1, x2]:
            line = mpl.lines.Line2D(
                [x_position + offset for offset in xoffsets], yvalues,
                transform=plt.gcf().transFigure, clip_on=False,
                color=color)
            axes.add_line(line)
    _load_pyplot()
    # Readjust upper_frac if ybounds are defined
    if ybounds:
        if len(ybounds) != 4:
            print "len(ybounds) != 4; aborting..."
            return
        ymin1, ymax1, ymin2, ymax2 = [float(value) for value in ybounds]
        data_height1, data_height2 = (ymax1 - ymin1), (ymax2 - ymin2)
        upper_frac = data_height2 / (data_height1 + data_height2)
    x1, y1, x2, y2 = axes.get_position().get_points().flatten().tolist()
    width = x2 - x1
    lower_height = (y2 - y1) * ((1 - upper_frac) - 0.5 * break_frac)
    upper_height = (y2 - y1) * (upper_frac - 0.5 * break_frac)
    upper_bottom = (y2 - y1) - upper_height + y1
    lower_axes = plt.axes([x1, y1, width, lower_height], axisbg='None')
    upper_axes = plt.axes([x1, upper_bottom, width, upper_height],
                          axisbg='None', sharex=lower_axes)
    # Erase the edges between the axes
    for loc, spine in upper_axes.spines.iteritems():
        if loc == 'bottom':
            spine.set_color('none')
    for loc, spine in lower_axes.spines.iteritems():
        if loc == 'top':
            spine.set_color('none')
    upper_axes.get_xaxis().set_ticks_position('top')
    lower_axes.get_xaxis().set_ticks_position('bottom')
    plt.setp(upper_axes.get_xticklabels(), visible=False)
    breakmarks(upper_axes, y1 + lower_height, upper_bottom)
    # Set ylims if ybounds are defined
    if ybounds:
        lower_axes.set_ylim(ymin1, ymax1)
        upper_axes.set_ylim(ymin2, ymax2)
        lower_axes.set_autoscaley_on(False)
        upper_axes.set_autoscaley_on(False)
        upper_axes.yaxis.get_label().set_position((0, 1 - (0.5 / (upper_frac/(1+break_frac)))))
        lower_axes.yaxis.get_label().set_position((0, 0.5 / ((1 - upper_frac)/(1+break_frac))))
    # Make original axes invisible
    axes.set_xticks([])
    axes.set_yticks([])
    for loc, spine in axes.spines.iteritems():
        spine.set_color('none')
    return upper_axes, lower_axes

def prepare_efficiency(axes, lower_bound=0.69):
    """
    Set up an efficiency figure with breakmarks to indicate a suppressed zero.

    The y-axis limits are set to (lower_bound, 1.0), as appropriate for an
    efficiency plot, and autoscaling is turned off.
    """
    upper_axes, lower_axes = axes_broken_y(axes, upper_frac=0.97)
    lower_axes.set_yticks([])
    upper_axes.set_ylim(lower_bound, 1.)
    upper_axes.set_autoscaley_on(False)
    return upper_axes, lower_axes
## ##     def breakmarks(axes, position):
## ##         plt.axes(axes)
## ##         xwidth = 0.005 * (plt.xlim()[1] - plt.xlim()[0])
## ##         ywidth = 0.001
## ##         if position == 'bottom': j = 0
## ##         if position == 'top': j = 1
## ##         for i in range(2):
## ##             line = mpl.lines.Line2D(
## ##                 [plt.xlim()[i] - xwidth, plt.xlim()[i] + xwidth],
## ##                 [plt.ylim()[j] - ywidth, plt.ylim()[j] + ywidth],
## ##                 linewidth=1, color='black', clip_on=False)
## ##             axes.add_line(line)


if __name__ == "__main__":
    # no doctest stuff yet implemented; maybe in future it will be
    import doctest
    doctest.testmod()
