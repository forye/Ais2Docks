__author__ = 'Idan'


FILENAME = 'res/data.csv'

test_project = 'wordAp'  # 'wordtest'
test_key = 'AIzaSyBI9iHDggub9qAOoNDOQGhqul3YPZMqepw'

projec = 'wordapp'
server_key = 'AIzaSyANaT6tKle3aOytgYtGnvuWZjEVr12Ijjs'

Browser_key = 'AIzaSyDyx9OWBojxVdhsfWn6SzJsWp0xMi-i9Zs'

AIS_CONSTITANCY_TEST = ['MMSI','Class', 'Size', 'DistanceToBow', 'DistanceToStern', 'DistanceToPort', 'DistanceToStarboard']

CLASSES = ['Unknown','Cargo','Tanker','Fishing','High Speed Craft','Service Vessel','Military Or Law','Passenger','Pleasure','Other','Rig' ]

ELUMINATE = ['High Speed Craft', 'Military Or Law', 'Fishing', 'Passenger', 'Pleasure']

DOCK_FIELDS = ['Time', 'Latitude', 'Longitude', 'Heading']
SHIP_MINIMAL_SIZE = 250

SHIP_MINIMAL_DOCKING_TIME_IN_HOURS =4

R_EARTH = 6367443.155

DOCKING_LOCATION_RESULT = 'docking_locations.json'
DOCKING_LOCATION_RESULT2 = 'docks_locations.json'


lat_lim = 52.010829999999999, 51.844949999999997
long_lim = 4.5812230000000005, 3.9503330000000001
Center = (lat_lim[0] + lat_lim[1]) / 2, (long_lim[0] + long_lim[1]) / 2

A, LY, LX = 55566.424, 40007860, 40075016

MINIMAL_METRIC_RESOLUTION = 300 # 500?
ZOOM = 16 # 12
ZOOM_SCALE = 2 ** ZOOM
ANG_RES = MINIMAL_METRIC_RESOLUTION / (A * ZOOM_SCALE) # deg /
MIN_HEADING_ERROR = 36.0  # degs

ADMIN_SCALE =  2 * 10.0**4

FIG_G_NAME = 'res\\docks\\doc_figure_{0}.png'