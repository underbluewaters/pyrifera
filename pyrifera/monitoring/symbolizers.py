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
            """ % ( record.year, record.year, 1,
                site.name, taxon.name(), record.year,
                site.name, taxon.name(), record.year,
                site.point.kml,
                site.point.x,
                site.point.y,
                scale, scale,
                z,
                model,
            ))
        return marks
    