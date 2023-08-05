import ConfigParser, StringIO
from genshi.template import MarkupTemplate
from tw.api import JSLink, JSSource
from tg import config, url
import urllib, urllib2
from libacr.lib import gmap_js
import tw.forms as twf

class MapRenderer(object):
    def __init__(self):
        self.name = 'map'
        self.exposed = True
        self.form_fields = [twf.TextField('location', label_text="Address:",
                                                      validator=twf.validators.String(not_empty=True, strip=True)),
                            twf.TextField('zoom', label_text="Zoom:", default=13,
                                                  validator=twf.validators.Int(not_empty=True, strip=True)),
                            twf.TextField('size', label_text="Size:")]

    def to_dict(self, data):
        config = ConfigParser.ConfigParser({'zoom':13, 'size':''})
        config.readfp(StringIO.StringIO(data))

        d = {'location' : config.get('map', 'location'),
                 'zoom' : config.get('map', 'zoom'),
                 'size' : config.get('map', 'size')}

        return d

    def from_dict(self, dic):
        config = ConfigParser.ConfigParser()
        config.add_section('map')
        config.set('map', 'location', dic['location'])
        config.set('map', 'zoom', dic.get('zoom', 13))
        if dic.get('size'):
            config.set('map', 'size', dic['size'])

        s = StringIO.StringIO()
        config.write(s)
        return s.getvalue()
        
    def _get_geocode(self, api_key, addr):
        root_url = "http://maps.google.com/maps/geo?"
        gkey = api_key

        geodat = [0]
        if addr:
            values = {'q' : addr, 'output':'csv', 'key':gkey}
            data = urllib.urlencode(values)
            url = root_url+data
            req = urllib2.Request(url)
        
            response = urllib2.urlopen(req)
            geodat = response.read().split(',')
            response.close()
        
        code = geodat[0]
        if code == '200':
            code,precision,lat,lng = geodat
            return {'code':code,'precision':precision,'lat':lat,'lng':lng}
        else:
            return {'code':code,'lat':0, 'lng':0}
        
    def _parse_conf(self, data):
        config = ConfigParser.ConfigParser({'zoom':'13', 'size':''})
        config.readfp(StringIO.StringIO(data))
        
        self.zoom = int(config.get('map', 'zoom'))
        self.size = config.get('map', 'size')
        self.location = config.get('map', 'location')
        
        if self.size:
            self.size_x, self.size_y = self.size.split('x')
    
    def render(self, page, slice, data):
        api_key = config.get('gmap_api_key')
        if not api_key:
            raise Exception('Google Maps API key missing inside configuration file, please specify one')
        
        self._parse_conf(data)
            
        gmap_api = JSLink(modname=__name__, link="http://maps.google.com/maps?file=api&amp;v=2.x&amp;key="+api_key)
        
        gmap_api.inject()
        gmap_js.inject()
        
        style = ""
        if self.size:
            style = 'style="width:%spx; height:%spx"' % (self.size_x, self.size_y)
        div = '<div class="acr_gmap" id="acr_gmap_%s" %s></div>' % (slice.uid, style)
        gmap_call = 'acr_create_gmap("acr_gmap_%s", "%s", %s);' % (slice.uid, self.location, str(self.zoom))
        
        result = div
        result += MarkupTemplate(JSSource(src=gmap_call).display()).generate().render('xhtml')
        return result
    
    def preview(self, page, slice, data):
        api_key = config.get('gmap_api_key')
        if not api_key:
            raise Exception('Google Maps API key missing inside configuration file, please specify one')
        
        self._parse_conf(data)
        
        location = self._get_geocode(api_key, self.location)
        
        size = self.size
        if not size:
            size = "200x200"
        
        link = url('http://maps.google.com/maps', ll='%s,%s' % (location['lat'], location['lng']), z=self.zoom)
        uri = url('http://maps.google.com/staticmap', center='%s,%s' % (location['lat'], location['lng']),
                                                      zoom=self.zoom, size=size, format='jpg',
                                                      markers='%s,%s,redc' % (location['lat'], location['lng']),
                                                      key=api_key, sensor='false')
        
        return '<a class="acr_gmap_preview" href="%s"><img src="%s"/></a>' % (link, uri)
    