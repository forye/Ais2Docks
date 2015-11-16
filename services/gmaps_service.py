__author__ = 'Idan'


'''
#
# Copyright 2014 Google Inc. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
'''
import  googlemaps as gmaps
import config.configuration as cfg
import datetime



def elevation( locations , client = None):
    """
    Provides elevation data for locations provided on the surface of the
    earth, including depth locations on the ocean floor (which return negative
    values)
    :param locations: List of latitude/longitude values from which you wish
        to calculate elevation data.
    :type locations: a single location, or a list of locations, where a
        location is a string, dict, list, or tuple
    :rtype: list of elevation data responses

    """
    if not client: client = get_client(cfg.test_key)
    params = {"locations": gmaps.convert.location_list(locations)}
    return client._get("/maps/api/elevation/json", params)["results"]


def elevation_along_path(client, path, samples):
    """
    Provides elevation data sampled along a path on the surface of the earth.
    :param path: An encoded polyline string, or a list of latitude/longitude
        values from which you wish to calculate elevation data.
    :type path: string, dict, list, or tuple
    :param samples: The number of sample points along a path for which to
        return elevation data.
    :type samples: int
    :rtype: list of elevation data responses
    """

    if type(path) is str:
        path = "enc:%s" % path
    else:
        path = gmaps.convert.location_list(path)

    params = {
        "path": path,
        "samples": samples
    }

    return client._get("/maps/api/elevation/json", params)["results"]


def get_client(_key = None):
   '''returns a gmaps, a client instance for google maps given the app api key '''
   if not _key : _key = cfg.test_key
   return gmaps.Client(key=_key)



def reverse_geocode(_key , loc = (40.714224, -73.961452)):
   '''# Look up an address with reverse geocoding
   loc- tuple -> location to discriptive name using maps geolocation'''
   if not _key: return None
   client = gmaps.Client(key=_key)
   if loc is not None: return client.reverse_geocode(loc)


def arb_req():
   lat = str(39.7391536)
   long = str (-104.9847034)
   return 'https://maps.googleapis.com/maps/api/elevation/json?locations='+lat+','+long +'&key=' + cfg.test_key



def get_mpa_image_url( zoom = None):
    if not zoom: zoom = cfg.ZOOM
    api_req = 'https://maps.googleapis.com/maps/api/staticmap?size=' \
              +'400x400' \
              +'&zoom='\
              +str(zoom)\
              +'&path=weight:3' \
               '%7Ccolor:orange' \
               '%7Cenc:polyline_data&'' \
              '+'key=AIzaSyDyx9OWBojxVdhsfWn6SzJsWp0xMi-i9Zs'



def do_stuff(loc):

   # Geocoding and address
   geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

   # Look up an address with reverse geocoding
   reverse_geocode_result = gmaps.reverse_geocode(loc)

   # Request directions via public transit
   now = datetime.now()
   directions_result = gmaps.directions("Sydney Town Hall",
                                        "Parramatta, NSW",
                                        mode="transit",
                                        departure_time=now)



'''

    https://github.com/googlemaps/google-maps-services-python
    https://github.com/googlemaps/google-maps-services-python/tree/master/test
    https://googlemaps.github.io/google-maps-services-python/docs/2.2/


https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key=AIzaSyBI9iHDggub9qAOoNDOQGhqul3YPZMqepw
{
   "results" : [
      {
         "elevation" : 1608.637939453125,
         "location" : {
            "lat" : 39.7391536,
            "lng" : -104.9847034
         },
         "resolution" : 4.771975994110107
      }
   ],
   "status" : "OK"
}
'''


'''
import datetime

   # Geocoding and address
   geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

   # Look up an address with reverse geocoding
   reverse_geocode_result = gmaps.reverse_geocode(loc)

   # Request directions via public transit
   now = datetime.now()
   directions_result = gmaps.directions("Sydney Town Hall",
                                        "Parramatta, NSW",
                                        mode="transit",
                                        departure_time=now)


# https://github.com/googlemaps/google-maps-services-python

'''