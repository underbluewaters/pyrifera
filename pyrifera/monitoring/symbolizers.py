from settings import MEDIA_URL
from models import MeanDensity
from django.contrib.gis.geos import GeometryCollection, MultiPoint, Point
from django.contrib.gis.measure import Distance, D
from math import pi, sin, tan, sqrt, pow
from monitoring import taxonLineChart
from django.core.urlresolvers import reverse
from urllib import urlencode

class ColladaSymbolizer:
    
    def __init__(self, dataset, sites=None, minScale=0.2, maxScale=2, min_z=1, max_z=2):
        self.dataset = dataset
        self.sites = sites
        self.minScale = minScale
        self.maxScale = maxScale
        self.min_z = min_z
        self.max_z = max_z
    
    @property
    def placemarks(self):
        min = None
        max = None
        dataset = list(self.dataset)
        for record in dataset:
            if min is None or record.mean < min:
                min = record.mean
            if max is None or record.mean > max:
                max = record.mean
        marks = []
        for record in dataset:
            site = record.site
            taxon = record.taxon
            ratio = record.mean / max
            scale = self.minScale + ((self.maxScale - self.minScale) * ratio)
            z = self.max_z - ((self.maxScale - self.minScale) * (ratio))
            model = MEDIA_URL + "prop_circle_zero.dae"
            if record.mean > 0:
                model = MEDIA_URL + "prop_circle.dae"
            if record.mean <= 0:
                scale = self.minScale * .9
            marks.append("""
                <Placemark>
                    <TimeSpan>
                      <begin>%s-01-02</begin>
                      <end>%s-12-31</end>
                    </TimeSpan>
                    <Style>
            			<IconStyle>
            				<scale>%s</scale>
            			</IconStyle>
            		</Style>
                    <name>%s - %s (%s)</name>
                    <description>
                        %s - %s (%s)
                    </description>
                    %s
                    <Model>
                        <altitudeMode>relativeToGround</altitudeMode>
                        <Location>
                            <longitude>%s</longitude>
                            <latitude>%s</latitude>
                            <altitude>0</altitude>
                        </Location>
                        <Orientation>
                            <heading>0</heading>
                            <tilt>0</tilt>
                            <roll>0</roll>
                        </Orientation>
                        <Scale>
                            <x>%s</x>
                            <y>%s</y>
                            <z>%s</z>
                        </Scale>
                        <Link>
                            <href>%s</href>
                        </Link>
                    </Model>
                </Placemark>
                <Placemark>
            		<name>%s</name>
            		<styleUrl>#mouseover-only</styleUrl>
            		<Point>
            			<coordinates>%s,%s</coordinates>
            		</Point>
            		<TimeSpan>
                      <begin>%s-01-02</begin>
                      <end>%s-12-31</end>
                    </TimeSpan>
            	</Placemark>
            """ % ( record.year, record.year, 1,
                site.name, taxon.name(), record.year,
                site.name, taxon.name(), record.year,
                site.point.kml,
                site.point.x,
                site.point.y,
                scale, scale,
                z,
                model,
                record.mean,
                site.point.x,
                site.point.y,
                record.year, record.year,
            ))
        return marks
    

class ScaledImageGChartSymbolizer:

    def __init__(self, dataset, sites=None, minScale=0.2, maxScale=2):
        self.dataset = dataset
        self.sites = sites
        self.minScale = minScale
        self.maxScale = maxScale
        chtt = urlencode({'chtt': dataset[0].taxon.name()})
        self.overlay_src = "http://chart.apis.google.com/chart?chf=bg,s,67676700&chs=600x193&cht=ls&chds=-10,103.333&chd=t0:46.856,17.632,28.781,63.82,81.759&chdlp=b&chls=1&chma=5,5,5,25|4,4&chm=@o,FF0000,0,0.35:0.92,15.667|@t%%3D+None+Observed,FF0000,0,0.38:1,21,1|@tYellow+Circles+Scale+Proportionally+with+Quantity+Observed,FFFF88,0,0.1:0.5,22&%s&chts=E8F4F7,32" % (chtt, )

    def lookat(self):
        dataset = list(self.dataset)
        earliest = None
        for record in dataset:
            if earliest is None or record.year < earliest:
                earliest = record.year
        mp = MultiPoint([r.site.point for r in list(self.dataset)])
        timestamp = str(earliest) + "-01-15"
        kml = calclookat(mp.envelope, timestamp)
        return kml

    @property
    def placemarks(self):
        self.dataset = list(self.dataset)
        dataset = self.dataset
        means = [r.mean for r in dataset]
        min_y = min(means)
        max_y = max(means)
        marks = []
        for record in dataset:
            site = record.site
            taxon = record.taxon
            ratio = record.mean / max_y
            scale = self.minScale + ((self.maxScale - self.minScale) * ratio)
            data = ", ".join([m.json_string() for m in MeanDensity.objects.filter(site=site, taxon=taxon).order_by('year')])            
            image = MEDIA_URL + "images/prop_circle.png"
            if record.mean > 0:
                color = 'aa2DF7FF'
            if record.mean <= 0:
                color = 'aa1111ff'
                scale = self.minScale
            marks.append("""
                <Placemark id="%s">
                    <TimeSpan>
                      <begin>%s-01-05</begin>
                      <end>%s-12-31</end>
                    </TimeSpan>
                    <styleUrl>#scaledImage</styleUrl>
                    <Style>
            			<IconStyle>
            				<scale>%s</scale>
            				<color>%s</color>
            			</IconStyle>
            		</Style>
                    <name>%s</name>
                    <description><![CDATA[
                        <h3>$[name] <a href="%s" rel="sidebar">see site info</a></h3>
                        <h4>(%s) - %s %.3f %s</h4>
                        <img src="%s" width="300" height="100">
                    ]]></description>
                    %s
                </Placemark>
            """ % ( "%s-%s-%s" % (record.year, site.pk, taxon.pk ),
                record.year, record.year,
                scale,
                color,
                site.name, 
                reverse('monitoring.views.site', args=[site.pk]),
                record.year, taxon.name(), record.mean, record.protocol.unit.suffix,
                taxonLineChart(taxon, site, max_y=max_y, label_record=record),
                site.point.kml,
            ))
        return marks


class ScaledImageSymbolizer:

    def __init__(self, dataset, sites=None, minScale=0.2, maxScale=2):
        self.dataset = dataset
        self.sites = sites
        self.minScale = minScale
        self.maxScale = maxScale

    def lookat(self):
        dataset = list(self.dataset)
        earliest = None
        for record in dataset:
            if earliest is None or record.year < earliest:
                earliest = record.year
        mp = MultiPoint([r.site.point for r in list(self.dataset)])
        timestamp = str(earliest) + "-01-15"
        kml = calclookat(mp.envelope, timestamp)
        return kml

    @property
    def placemarks(self):
        min = None
        max = None
        self.dataset = list(self.dataset)
        dataset = self.dataset
        for record in dataset:
            if min is None or record.mean < min:
                min = record.mean
            if max is None or record.mean > max:
                max = record.mean
        marks = []
        for record in dataset:
            site = record.site
            taxon = record.taxon
            ratio = record.mean / max
            scale = self.minScale + ((self.maxScale - self.minScale) * ratio)
            data = ", ".join([m.json_string() for m in MeanDensity.objects.filter(site=site, taxon=taxon).order_by('year')])            
            image = MEDIA_URL + "images/prop_circle.png"
            if record.mean > 0:
                color = 'aa2DF7FF'
            if record.mean <= 0:
                color = 'aa1111ff'
                scale = self.minScale
            marks.append("""
                <Placemark id="%s">
                    <TimeSpan>
                      <begin>%s-01-05</begin>
                      <end>%s-12-31</end>
                    </TimeSpan>
                    <styleUrl>#scaledImage</styleUrl>
                    <Style>
            			<IconStyle>
            				<scale>%s</scale>
            				<color>%s</color>
            			</IconStyle>
            		</Style>
                    <name>%s - %s %s %s</name>
                    <description><![CDATA[
                        <html>
                        <head>
                        <script type="text/javascript" src="%sd3.js"></script>
                        <script type="text/javascript">
                            var data = [%s];
                            var site_name = "%s";
                            var unit = '%s';
                            var taxon_name = "%s";
                            var year = '%s';

                            var w = 280,
                                h = 90,
                                pt = 5,                         // padding top
                                pb = 5                          // bottom
                                pl = 5,                        // left
                                pr = 5,                         // right
                                yaxisw = 20,                    // y axis labels width
                                xaxish = 20,                    // x axis labels height
                                legendh = 0,                   // legend height
                                dw = w - (pr + pl + yaxisw),    // data range width in pixels
                                dh = h - (pt + pb + xaxish + legendh),  // data height in px
                                min = 0,
                                max = %s,
                                earliest = d3.min(data, function(d){return d.date}),
                                latest = d3.max(data, function(d){return d.date}),
                                x = d3.scale.linear().domain(
                                    [earliest, latest]).range([0, dw]),
                                y = d3.scale.linear().domain([min, max]).range([dh, 0]);

                            var years = [];
                			if(earliest.getDay() == 1 && earliest.getMonth() == 1){
                				years.push([new Date(earliest.getFullYear(), 0, 1, 1, 1, 1)]);				
                			}
                            var c = earliest;
                            while(c.getFullYear() < latest.getFullYear()){
                                c = new Date(c.getFullYear() + 1, 0, 1, 1, 1, 1);
                                years.push(new Date(c.getTime()));
                            }

                            var vis = d3.select('#container')
                                .append('svg:svg')
                                    .attr('id', 'panel')
                                    .attr('width', w)
                                    .attr('height', h)

                            var g = vis.append('svg:g')
                                .attr('transform', "translate("+(pl + yaxisw)+","+(pt + legendh)+")")

                            g.selectAll("svg:path")
                                .data([data]).enter()
                                .append('svg:path')
                              .attr("d", d3.svg.line()
                                .x(function(d) { return x(d.date); })
                                .y(function(d) { return y(d.mean)}))
                              .attr('style', 'stroke: steelblue; fill: none;')
                              .attr('class','line')

                            g.selectAll('line.error')
                                .data(data).enter()
                                .append('svg:line')
                                    .attr('class', 'error')
                                    .attr('x1', function(d){return x(d.date)})
                                    .attr('y1', function(d){return y(d.mean - d.stderror)})
                                    .attr('x2', function(d){return x(d.date)})
                                    .attr('y2', function(d){return y(d.mean + d.stderror)})
                                    .attr('style', 'stroke: red; fill: none;')


                            g.append("svg:line")
                                .attr('x1', 0)
                                .attr('y1', y(0))
                                .attr('x2', dw)
                                .attr('y2', y(0))
                                .attr('style', 'stroke:black; stroke-width:1px; opacity:0.4;')


                            // Determines how many year labels can fit on the x-axis
                  			var max_year_labels = dw / (21 + 25);

                  			var year_labels = g.selectAll('text.year_label')
                                .data(years).enter()
                                .append('svg:text')
                                .text(function(d){return d.getFullYear()})
                                .attr('x', function(d){return x(d)})
                                .attr('y', dh + 20)
                				.attr('opacity', function(d, i){ return i %% Math.round(years.length / max_year_labels) ? '0' : '1'})
                                .attr('style', 'font-size: 10px;text-anchor:middle;')

                            var year_tics = g.selectAll('line.year')
                                .data(years).enter()
                                .append('svg:line')
                                .attr('class', 'year')
                                .attr('x1', function(d){return x(d)})
                                .attr('y1', dh + 10)
                                .attr('x2', function(d){return x(d)})
                                .attr('y2', dh + 5)
                				.attr('style', 'stroke:black;stroke-width:1;')
                				.attr('opacity', function(d, i){ return i %% Math.round(years.length / max_year_labels) ? '1' : '0'})

                            var year_tics = g.selectAll('line.yeart')
                                .data(years).enter()
                                .append('svg:line')
                                .attr('class', 'yeart')
                                .attr('x1', function(d){return x(d)})
                                .attr('y1', dh + 10)
                                .attr('x2', function(d){return x(d)})
                                .attr('y2', dh + 3)
                				.attr('style', 'stroke:black;stroke-width:1.2;')
                				.attr('opacity', function(d, i){ return i %% Math.round(years.length / max_year_labels) ? '0' : '1'})

                        	var yaxis_labels = g.selectAll('text.mean')
                			    .data(y.ticks(4)).enter()
                			        .append('svg:text')
                			        .text(function(d){return (Math.round(d * 100) / 100).toString()})
                			        .attr('x', 8 - yaxisw)
                			        .attr('y', function(d){return y(d) + 2})
                			        .attr('style', 'font-size: 10px;text-anchor:end;')

                			var yaxis_ticks = g.selectAll('line.mean')
                			    .data(y.ticks(4)).enter()
                			        .append('svg:line')
                			        .attr('class', 'mean')
                                    .attr('x1', -3)
                                    .attr('y1', function(d){return y(d)})
                                    .attr('x2', -8)
                                    .attr('y2', function(d){return y(d)})
                    				.attr('style', 'stroke:black;stroke-width:1px;')

                			var yaxis_minor_ticks = g.selectAll('line.minor_mean')
                			    .data(y.ticks(10)).enter()
                			        .append('svg:line')
                			        .attr('class', 'minor_mean')
                                    .attr('x1', -3)
                                    .attr('y1', function(d){return y(d)})
                                    .attr('x2', -6)
                                    .attr('y2', function(d){return y(d)})
                    				.attr('style', 'stroke:black;stroke-width:1px;')


                        </script>
                        </head>
                        <body>
                        <div style="margin-left:auto;margin-right:auto;width:280px; height:90px;" id="container"> </div>
                        </body>
                        </html>
                    ]]></description>
                    %s
                    <ExtendedData>                       
                      <Data name="string">
                        <displayName>key</displayName>    <!-- string -->
                        <value>blah</value>                <!-- string -->
                      </Data>
                    </ExtendedData>
                </Placemark>
            """ % ( "%s-%s-%s" % (record.year, site.pk, taxon.pk ),
                record.year, record.year,
                scale,
                color,
                site.name, taxon.name(), record.mean, record.protocol.unit.suffix,
                MEDIA_URL,
                data,
                site.name, record.protocol.unit.suffix, taxon.name(), 
                record.year,
                max,
                site.point.kml,
            ))
        return marks


def toRadians(n):
    return n * pi / 180

EARTH_RADIUS = 6378135.0
DEFAULT_RANGE = 1000;

def calclookat(geom, timestamp):
    geom = geom.clone()
    # geom.transform(4326)
    center = geom.centroid;
    extent = geom.extent
    w = extent[0]
    s = extent[1]
    e = extent[2]
    n = extent[3]
    
    if w == e and n == s:
        w = w + 1
        n = n + 1

    distEW = (Point(center.x, w)).distance(Point(center.x, e))
    distNS = (Point(n, center.y)).distance(Point(s, center.y))

    aspectRatio = min(max(1.0, distEW / distNS), 1.0)

    alpha = toRadians((45.0 / (aspectRatio + 0.4) - 2.0))
    expandToDistance = max(distNS, distEW)
    beta = min(toRadians(90), alpha + expandToDistance / (2 * EARTH_RADIUS))
    lookAtRange = 1.5 * EARTH_RADIUS * (sin(beta) * sqrt(1 + 1 / pow(tan(alpha), 2)) - 1)

    meters = lookAtRange * 111.12 * 1000

    time = ''
    if timestamp:
        time = """
            <gx:TimeStamp>
                <when>%s</when>
            </gx:TimeStamp>
        """ % timestamp
    return """
        <LookAt>
            <latitude>%f</latitude>
            <longitude>%f</longitude>
            <range>%f</range>
            <tilt>%f</tilt>
            <heading>%f</heading>
            <altitudeMode>clampToGround</altitudeMode>
            %s
        </LookAt>
    """ % (center.y, center.x, meters, 0, 0, time, )
