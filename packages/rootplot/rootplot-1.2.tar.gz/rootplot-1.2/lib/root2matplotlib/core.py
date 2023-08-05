"""
Core implementation of the root2matplotlib module.
"""

__license__ = '''\
Copyright (c) 2009-2010 Jeff Klukas <klukas@wisc.edu>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

################ Import python libraries

import math
import ROOT
import re
import copy
import array


################ Define constants

_all_whitespace_string = re.compile(r'\s*$')


################ Define classes

class Hist2D(object):
    """A container to hold the paramters from a 2D ROOT histogram."""
    def __init__(self, hist, replace=None, label="__nolabel__", title=None,
                 xlabel=None, ylabel=None):
        try:
            if not hist.InheritsFrom("TH2"):
                raise TypeError("%s does not inherit from TH2" % hist)
        except:
            raise TypeError("%s is not a ROOT object" % hist)
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
        self.entries = hist.GetEntries()
        self.content = [[hist.GetBinContent(i, j) for i in range(1, nx + 1)]
                        for j in range(1, ny + 1)]
        self.xedges = [hist.GetXaxis().GetBinLowEdge(i)
                             for i in range(1, nx + 2)]
        self.yedges = [hist.GetYaxis().GetBinLowEdge(i)
                             for i in range(1, ny + 2)]
        self.x      = [(self.xedges[i+1] + self.xedges[i])/2
                             for i in range(nx)]
        self.y      = [(self.yedges[i+1] + self.yedges[i])/2
                             for i in range(ny)]
        self.title  = _parse_latex(title or hist.GetTitle(), replace)
        self.xlabel = _parse_latex(xlabel or hist.GetXaxis().GetTitle(),replace)
        self.ylabel = _parse_latex(ylabel or hist.GetYaxis().GetTitle(),replace)
        self.label  = _parse_latex(label, replace)
    def _flat_content(self):
        flatcontent = []
        for row in self.content:
            flatcontent += row
        return flatcontent
    def __getitem__(self, index):
        """Return contents of indexth bin: x.__getitem__(y) <==> x[y]"""
        return self._flat_content()[index]
    def __len__(self):
        """Return the number of bins: x.__len__() <==> len(x)"""
        return len(self._flat_content())
    def __iter__(self):
        """Iterate through bins: x.__iter__() <==> iter(x)"""
        return iter(self._flat_content())
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
        if maxvalue == 0:
            maxvalue = 1
        sizes = np.array(self.content).flatten() / maxvalue * maxsize
        plot = plt.scatter(x, y, sizes, marker='s', **kwargs)
        return plot
    def TH2F(self, name=""):
        """Return a ROOT.TH2F object with contents of this Hist2D."""
        th2f = ROOT.TH2F(name, "",
                         self.nbinsx, array.array('f', self.xedges),
                         self.nbinsy, array.array('f', self.yedges))
        th2f.SetTitle("%s;%s;%s" % (self.title, self.xlabel, self.ylabel))
        for ix in range(self.nbinsx):
            for iy in range(self.nbinsy):
                th2f.SetBinContent(ix + 1, iy + 1, self.content[iy][ix])
        return th2f

class Hist(object):
    """A container to hold the parameters from a ROOT histogram."""
    def __init__(self, hist, replace=None, label="__nolabel__", title=None,
                 xlabel=None, ylabel=None):
        try:
            hist.GetNbinsX()
            self.__init_TH1(hist)
        except AttributeError:
            try:
                hist.GetN()
                self.__init_TGraph(hist)
            except AttributeError:
                raise TypeError("%s is not a 1D histogram or TGraph" % hist)
        self.input_class = hist.ClassName()
        self.title  = _parse_latex(title or hist.GetTitle(), replace)
        self.xlabel = _parse_latex(xlabel or hist.GetXaxis().GetTitle(),replace)
        self.ylabel = _parse_latex(ylabel or hist.GetYaxis().GetTitle(),replace)
        self.label  = _parse_latex(label, replace)
    def __init_TH1(self, hist):
        self.nbins = n = hist.GetNbinsX()
        self.binlabels = _process_bin_labels([hist.GetXaxis().GetBinLabel(i)
                                              for i in range(1, n + 1)])
        if self.binlabels and '' in self.binlabels:
            # Get rid of extra non-labeled bins
            self.nbins = n = self.binlabels.index('')
            self.binlabels = self.binlabels[:n]
        self.entries = hist.GetEntries()
        self.xedges = [hist.GetBinLowEdge(i) for i in range(1, n + 2)]
        self.x      = [(self.xedges[i+1] + self.xedges[i])/2 for i in range(n)]
        self.xerr   = [(self.xedges[i+1] - self.xedges[i])/2 for i in range(n)]
        self.xerr   = [self.xerr[:], self.xerr[:]]
        self.width  = [(self.xedges[i+1] - self.xedges[i])   for i in range(n)]
        self.y      = [hist.GetBinContent(i) for i in range(1, n + 1)]
        self.yerr   = [hist.GetBinError(  i) for i in range(1, n + 1)]
        self.yerr   = [self.yerr[:], self.yerr[:]]
        self.underflow = hist.GetBinContent(0)
        self.overflow  = hist.GetBinContent(self.nbins + 1)
    def __init_TGraph(self, hist):
        self.nbins = n = hist.GetN()
        self.x, self.y = [], []
        x, y = ROOT.Double(0), ROOT.Double(0)
        for i in range(n):
            hist.GetPoint(i, x, y)
            self.x.append(copy.copy(x))
            self.y.append(copy.copy(y))
        lower = [max(0, hist.GetErrorXlow(i))  for i in xrange(n)]
        upper = [max(0, hist.GetErrorXhigh(i)) for i in xrange(n)]
        self.xerr = [lower[:], upper[:]]
        lower = [max(0, hist.GetErrorYlow(i))  for i in xrange(n)]
        upper = [max(0, hist.GetErrorYhigh(i)) for i in xrange(n)]
        self.yerr = [lower[:], upper[:]]
        self.xedges = [self.x[i] - self.xerr[0][i] for i in xrange(n)]
        self.xedges.append(self.x[n - 1] + self.xerr[1][n - 1])
        self.width = [self.xedges[i + 1] - self.xedges[i] for i in range(n)]
        self.underflow, self.overflow = 0, 0
        self.binlabels = None
        self.entries = n
    def __getitem__(self, index):
        """Return contents of indexth bin: x.__getitem__(y) <==> x[y]"""
        return self.y[index]
    def __setitem__(self, index, value):
        """Set contents of indexth bin: x.__setitem__(i, y) <==> x[i]=y"""
        self.y[index] = value
    def __len__(self):
        """Return the number of bins: x.__len__() <==> len(x)"""
        return self.nbins
    def __iter__(self):
        """Iterate through bins: x.__iter__() <==> iter(x)"""
        return iter(self.y)
    def min(self, threshold = None):
        """Return the y-value of the bottom tip of the lowest errorbar."""
        lower_errors = self.yerr[0]
        vals = [self.y[i] - lower_errors[i] for i in range(self.nbins)
                if (self.y[i] - lower_errors[i]) > threshold]
        if vals:
            return min(vals)
        else:
            return threshold
    def _av_yerr(self):
        """Return average between the upper and lower xerr."""
        return [(self.xerr[0][i] + self.xerr[1][i]) / 2
                for i in range(self.nbins)]
    def _av_yerr(self):
        """Return average between the upper and lower yerr."""
        return [(self.yerr[0][i] + self.yerr[1][i]) / 2
                for i in range(self.nbins)]
    def _prepare_xaxis(self, rotation=0, alignment='center'):
        """Apply bounds and text labels on x axis."""
        if self.binlabels is not None:
            binwidth = (self.xedges[-1] - self.xedges[0]) / self.nbins
            plt.xticks(self.x, self.binlabels,
                       rotation=rotation, ha=alignment)
        plt.xlim(self.xedges[0], self.xedges[-1])

    def _prepare_yaxis(self, rotation=0, alignment='center'):
        """Apply bound and text labels on y axis."""
        if self.binlabels is not None:
            binwidth = (self.xedges[-1] - self.xedges[0]) / self.nbins
            plt.yticks(self.x, self.binlabels,
                       rotation=rotation, va=alignment)
        plt.ylim(self.xedges[0], self.xedges[-1])

    def scale(self, factor):
        """
        Scale contents, errors, and over/underflow by the given scale factor.
        """
        self.y = [x * factor for x in self.y]
        self.yerr[0] = [x * factor for x in self.yerr[0]]
        self.yerr[1] = [x * factor for x in self.yerr[1]]
        self.overflow *= factor
        self.underflow *= factor
    def show_titles(self):
        """Add the titles defined in the ROOT histogram to the figure."""
        _load_pyplot()
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
    def delete_bin(self, index):
        """
        Delete a the contents of a bin, sliding all the other data one bin to
        the left.  This can be useful for histograms with labeled bins.
        """
        self.nbins -= 1
        self.xedges.pop()
        self.x.pop()
        self.width.pop()
        self.y.pop(index)
        self.xerr[0].pop(index)
        self.xerr[1].pop(index)
        self.yerr[0].pop(index)
        self.yerr[1].pop(index)
        if self.binlabels:
            self.binlabels.pop(index)
    def hist(self, label_rotation=0, label_alignment='center', **kwargs):
        """
        Generate a matplotlib hist figure.

        All additional keyword arguments will be passed to pyplot.hist.
        """
        kwargs.pop('fmt', None)
        _load_pyplot()
        plot = plt.hist(self.x, weights=self.y, bins=self.xedges,
                        label=self.label, **kwargs)
        self._prepare_xaxis(label_rotation, label_alignment)
        return plot
    def errorbar(self, xerr=False, yerr=False, label_rotation=0,
                 label_alignment='center', **kwargs):
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
        self._prepare_xaxis(label_rotation, label_alignment)
        return errorbar
    def errorbarh(self, xerr=False, yerr=False, label_rotation=0,
                  label_alignment='center', **kwargs):
        """
        Generate a horizontal matplotlib errorbar figure.

        All additional keyword arguments will be passed to pyplot.errorbar.
        """
        if xerr: kwargs['xerr'] = self.yerr
        if yerr: kwargs['yerr'] = self.xerr
        _load_pyplot()
        errorbar = plt.errorbar(self.y, self.x, label=self.label, **kwargs)
        self._prepare_yaxis(label_rotation, label_alignment)
        return errorbar
    def bar(self, xerr=False, yerr=False, label_rotation=0,
            label_alignment='center', **kwargs):
        """
        Generate a matplotlib bar figure.

        All additional keyword arguments will be passed to pyplot.bar.
        """
        kwargs.pop('fmt', None)
        if xerr: kwargs['xerr'] = self.xerr
        if yerr: kwargs['yerr'] = self.yerr
        _load_pyplot()
        bar = plt.bar(self.xedges[0:-1], self.y, self.width, label=self.label,
                      **kwargs)
        self._prepare_xaxis(label_rotation, label_alignment)
        return bar
    def barh(self, xerr=False, yerr=False, yoffset=0., width=0.8,
             label_rotation=0, label_alignment='center', **kwargs):
        """
        Generate a horizontal matplotlib bar figure.

        All additional keyword arguments will be passed to pyplot.barh.
        """
        kwargs.pop('fmt', None)
        if xerr: kwargs['xerr'] = self.yerr
        if yerr: kwargs['yerr'] = self.xerr
        _load_pyplot()
        xcontent = [self.xedges[i] + self.width[i] * yoffset
                    for i in range(len(self.xedges) - 1)]
        width = [x * width for x in self.width]
        barh = plt.barh(xcontent, self.y, width, label=self.label,
                       **kwargs)
        self._prepare_yaxis(label_rotation, label_alignment)
        return barh
    def TH1F(self, name=""):
        """Return a ROOT.TH1F object with contents of this Hist"""
        th1f = ROOT.TH1F(name, "", self.nbins, array.array('f', self.xedges))
        th1f.SetTitle("%s;%s;%s" % (self.title, self.xlabel, self.ylabel))
        for i in range(self.nbins):
            th1f.SetBinContent(i + 1, self.y[i])
            try:
                th1f.SetBinError(i + 1, (self.yerr[0][i] + self.yerr[1][i]) / 2)
            except TypeError:
                th1f.SetBinError(i + 1, self.yerr[i])
        return th1f
    def TGraph(self, name=""):
        """Return a ROOT.TGraphAsymmErrors object with contents of this Hist"""
        x = array.array('f', self.x)
        y = array.array('f', self.y)
        xl = array.array('f', self.xerr[0])
        xh = array.array('f', self.xerr[1])
        yl = array.array('f', self.yerr[0])
        yh = array.array('f', self.yerr[1])
        tgraph = ROOT.TGraphAsymmErrors(self.nbins, x, y, xl, xh, yl, yh)
        tgraph.SetTitle('%s;%s;%s' % (self.title, self.xlabel, self.ylabel))
        return tgraph
    def divide(self, denominator):
        """
        Return the simple quotient with errors added in quadrature.

        This function is called by the division operator:
            hist3 = hist1.divide_wilson(hist2) <--> hist3 = hist1 / hist2
        """
        quotient = copy.deepcopy(self)
        num_yerr = self._av_yerr()
        den_yerr = denominator._av_yerr()
        quotient.yerr = [0. for i in range(self.nbins)]
        for i in range(self.nbins):
            if denominator[i] == 0 or self[i] == 0:
                quotient.y[i] = 0.
            else:
                quotient.y[i] = self[i] / denominator[i]
                quotient.yerr[i] = quotient[i]
                quotient.yerr[i] *= math.sqrt((num_yerr[i] / self[i]) ** 2 +
                                       (den_yerr[i] / denominator[i]) ** 2)
            if quotient.yerr[i] > quotient[i]:
                quotient.yerr[i] = quotient[i]
        quotient.yerr = [quotient.yerr, quotient.yerr]
        return quotient
    def divide_wilson(self, denominator):
        """Return an efficiency plot with Wilson score interval errors."""
        eff, upper_err, lower_err = wilson_interval(self.y, denominator.y)
        quotient = copy.deepcopy(self)
        quotient.y = eff
        quotient.yerr = [lower_err, upper_err]
        return quotient
    def __div__(self, denominator):
        return self.divide(denominator)

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
        """Return indexth hist: x.__getitem__(y) <==> x[y]"""
        return self.hists[index]
    def __setitem__(self, index, value):
        """Replace indexth hist with value: x.__setitem__(i, y) <==> x[i]=y"""
        self.hists[index] = value
    def __len__(self):
        """Return the number of hists in the stack: x.__len__() <==> len(x)"""
        return len(self.hists)
    def __iter__(self):
        """Iterate through hists in the stack: x.__iter__() <==> iter(x)"""
        return iter(self.hists)
    def max(self):
        """Return the value of the highest bin of all hists in the stack."""
        maxes = [max(x) for x in self.hists]
        return max(maxes)
    def min(self, threshold=None):
        """
        Return the value of the lowest bin of all hists in the stack.

        If threshold is specified, only values above the threshold will be
        considered.
        """
        mins = [x.min(threshold) for x in self.hists]
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
    def hist(self, label_rotation=0, **kwargs):
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
    def get(self, object_name, path=None):
        """Return a Hist object from the given path within this file."""
        if path:
            roothist = self.file.GetDirectory(path).Get(object_name)
        else:
            roothist = self.file.Get(object_name)
        try:
            return Hist2D(roothist)
        except TypeError:
            return Hist(roothist)

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
    global plt, transforms, np
    import matplotlib.pyplot as plt
    import matplotlib.transforms as transforms
    import numpy as np
    import matplotlib as mpl

def _parse_latex(string, replacements):
    """
    Modify a string based on a list of patterns and substitutions.

    replacements should be a list of two-entry tuples, the first entry giving
    a string to search for and the second entry giving the string with which
    to replace it.  If replacements includes a pattern entry containing
    'use_regexp', then all patterns will be treated as regular expressions
    using re.sub.
    """
    if not replacements:
        return string
    if 'use_regexp' in [x for x,y in replacements]:
        for pattern, repl in [x for x in replacements
                              if x[0] != 'use_regexp']:
            string = re.sub(pattern, repl, string)
    else:
        for pattern, repl in replacements:
            string = string.replace(pattern, repl)
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
        try:
            p = float(n) / d
            s = math.sqrt(p * (1 - p) / d + 1 / (4 * d * d))
            t = p + 1 / (2 * d)
            eff.append(p)
            upper_err.append(-p + 1/(1 + 1/d) * (t + s))
            lower_err.append(+p - 1/(1 + 1/d) * (t - s))
        except ZeroDivisionError:
            eff.append(0)
            upper_err.append(0)
            lower_err.append(0)
    return eff, upper_err, lower_err

if __name__ == "__main__":
    # no doctest stuff yet implemented; maybe in future it will be
    import doctest
    doctest.testmod()
