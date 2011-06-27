import functools
import cPickle
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis
import math

def memoized(fctn):
        memory = {}
        @functools.wraps(fctn)
        def memo(*args,**kwargs):
                haxh = cPickle.dumps((args, sorted(kwargs.iteritems())))

                if haxh not in memory:
                        memory[haxh] = fctn(*args,**kwargs)

                return memory[haxh]
        if memo.__doc__:
            memo.__doc__ = "\n".join([memo.__doc__,"This function is memoized."])
        return memo
        
        
def taxonLineChart(taxon, site, max_y=None, label_record=None):
    
    min_y = 0
    
    records = taxon.mean_densities.filter(site=site).order_by('year')
    years = [ record.year for record in records ]
    means = [ record.mean for record in records ]
    
    # Set the vertical range from 0 to 100
    max_y = max_y or max(means)
    span = max_y - min_y
    if span == 0:
        max_y = 1
        

    step = pow(10, round(math.log(max_y) / math.log(10)) - 1)
    ticks = frange(min_y, max_y + (step * 1), step)

    chart = SimpleLineChart(300, 100, y_range=[0, max_y])

    # Add the chart data
    chart.add_data(means)

    # Set the line colour to blue
    chart.set_colours(['76A4FB'])
    
    # limit number of ticks to around 4
    n = len(ticks) / 3

    # The Y axis labels contains 0 to 100 skipping every 25, but remove the
    # first number because it's obvious and gets in the way of the first X
    # label.
    ticks = ticks[::n]
    ticks[0] = ''
    chart.set_axis_labels(Axis.LEFT, ticks)

    # X axis labels
    chart.set_axis_labels(Axis.BOTTOM, years[::4])
    
    url = chart.get_url()
    url.replace('lc', 'ls')
    url += '&chm=B,C3D9FF,0,0,0'
    if label_record:
        url += ('|@a,3366CC,0,%f:%f,4' % (float(years.index(label_record.year)) / float(len(years)), (label_record.mean+(max_y * 0.05))/max_y))
    print url
    return url
    
    
import math
def frange(limit1, limit2 = None, increment = 1.):
    """
    Range function that accepts floats (and integers).

    Usage:
    frange(-2, 2, 0.1)
    frange(10)
    frange(10, increment = 0.5)

    The returned value is an iterator.  Use list(frange) for a list.
    """

    if limit2 is None:
        limit2, limit1 = limit1, 0.
    else:
        limit1 = float(limit1)

    count = int(math.ceil(limit2 - limit1)/increment)
    return list((limit1 + n*increment for n in range(count)))