import simplejson
from geopy import geocoders
from geopy.geocoders.google import GQueryError

from zope.interface import implements
from Products.Five.browser import BrowserView

from collective.geo.geographer.interfaces import IGeoCoder


class GeoCoder(object):
    """Wrapper class for geopy"""
    implements(IGeoCoder)

    def __init__(self, context):
        self.context = context

    def retrieve(self, address = None, google_api = None):
        if google_api:
            self.geocoder = geocoders.Google(str(google_api),
                                           output_format='json')
        else:
            self.geocoder = geocoders.Google(output_format='json')

        if not address:
            raise GQueryError

        return self.geocoder.geocode(address, exactly_one=False)


class GeoCoderView(BrowserView):
    """A simple view which provides a json
    output from geopy query"""

    def __init__(self, context, request):
        super(GeoCoderView, self).__init__(context, request)
        self.geocoder = IGeoCoder(self.context)

    def __call__(self, address = None, google_api = None):
        try:
            locations = self.geocoder.retrieve(address)
        except GQueryError:
            return 'null'
        return simplejson.dumps([loc for loc in locations])
