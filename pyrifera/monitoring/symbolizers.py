from settings import MEDIA_URL


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
            print ratio
            print record.mean
            scale = self.minScale + ((self.maxScale - self.minScale) * ratio)
            z = self.max_z - ((self.maxScale - self.minScale) * (ratio))
            print "z", z
            print scale
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
    

class ScaledImageSymbolizer:

    def __init__(self, dataset, sites=None, minScale=0.2, maxScale=2):
        self.dataset = dataset
        self.sites = sites
        self.minScale = minScale
        self.maxScale = maxScale

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
            print ratio
            print record.mean
            scale = self.minScale + ((self.maxScale - self.minScale) * ratio)
            print scale
            image = MEDIA_URL + "images/prop_circle.png"
            if record.mean > 0:
                color = 'aa2DF7FF'
            if record.mean <= 0:
                color = 'aa1111ff'
                scale = self.minScale
            marks.append("""
                <Placemark>
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
                    <name>%s - %s %s</name>
                    <description><![CDATA[
                        %s - %s (%s)
                        <script type="text/javascript">
                            console.log('hi there');
                        </script>
                        <script type="text/javascript" src="http://localhost/~cburt/pyrifera-media/protovis-3.2/protovis-r3.2.js"></script> 
                        <script type="text/javascript+protovis"> 
                        console.log('hi');
                        var data = pv.range(0, 10, .1).map(function(x) {
                            return {x: x, y: Math.sin(x) + Math.random() * .5 + 2};
                          });
                        /* Sizing and scales. */
                        var w = 400,
                            h = 200,
                            x = pv.Scale.linear(data, function(d) d.x).range(0, w),
                            y = pv.Scale.linear(0, 4).range(0, h);
                        /* The root panel. */
                        var vis = new pv.Panel()
                            .width(w)
                            .height(h)
                            .bottom(20)
                            .left(20)
                            .right(10)
                            .top(5);

                        /* Y-axis and ticks. */
                        vis.add(pv.Rule)
                            .data(y.ticks(5))
                            .bottom(y)
                            .strokeStyle(function(d) d ? "#eee" : "#000")
                          .anchor("left").add(pv.Label)
                            .text(y.tickFormat);

                        /* X-axis and ticks. */
                        vis.add(pv.Rule)
                            .data(x.ticks())
                            .visible(function(d) d)
                            .left(x)
                            .bottom(-5)
                            .height(5)
                          .anchor("bottom").add(pv.Label)
                            .text(x.tickFormat);

                        /* The area with top line. */
                        vis.add(pv.Area)
                            .data(data)
                            .bottom(1)
                            .left(function(d) x(d.x))
                            .height(function(d) y(d.y))
                            .fillStyle("rgb(121,173,210)")
                          .anchor("top").add(pv.Line)
                            .lineWidth(3);

                        vis.render();
                        console.log('blah');

                            </script>
                    ]]></description>
                    %s
                    <ExtendedData>                       
                      <Data name="string">
                        <displayName>key</displayName>    <!-- string -->
                        <value>blah</value>                <!-- string -->
                      </Data>
                    </ExtendedData>
                </Placemark>
            """ % ( record.year, record.year,
                scale,
                color,
                site.name, record.mean, record.protocol.unit.suffix,
                site.name, taxon.name(), record.year,
                site.point.kml,
            ))
        return marks
