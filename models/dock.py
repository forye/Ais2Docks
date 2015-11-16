__author__ = 'Idan'

import config.configuration as cfg
import numpy as np
from scipy.stats import mode

class dock:

    lat = None  # between -90 to 90
    lon = None  # between -180 to 180
    heading = None  # between 0 to 180
    depth = None
    image_uri = None
    resolution = None
    ships = []
    Mmsis = []
    min_ship_size = None
    a =None  # scale the resolution here

    ships_classes = []
    size = []
    # max_size = None
    # min_size = None
    width = []
    max_width = None
    min_width = None
    def __init__(self , lat, lon, heading, mmsi=None):
        self.lon = lon
        self.lat = lat
        self.a = cfg.ADMIN_SCALE
        self.heading = heading
        if mmsi:
            # self.ships.append([mmsi,lat,lon, heading])
            self.Mmsis.append(mmsi)
        self.resolution = cfg.ANG_RES * self.a

    def process_df(self, df , ships):
        self.Mmsis = set ( df[df["Latitude"] - self.lat < self.resolution][df["Longitude"] - self.lon < self.resolution]["MMSI"] )
        dock_size=[]
        dock_width=[]
        dock_class=[]
        for shp in ships:
            if shp.mmsi in self.Mmsis:
                dock_class.append( shp.clas )
                dock_size.append( shp.size )
                dock_width.append(shp.dist_2_starboard + shp.dist_2_port)
        dock_class.sort()
        self.ships_classes = set(dock_class)

    def is_equals(self, doc):  #  , heading = None, mmsi = None):
        # if mmsi , adds if equals
        if abs(self.lon - doc.lon) > self.resolution:
            return False
        if abs(self.lat - doc.lat) > self.resolution:
            return False
        return True

    def is_in_dock(self, lon,lat):  #  , heading = None, mmsi = None):
        # if mmsi , adds if equals
        if abs(self.lon - lon) > self.resolution: return False
        if abs(self.lat - lat) > self.resolution: return False
        return True

    def refine_heading(self):
        if not self.ships: return None
        a = np.array(self.ships)[:, 3] % 180
        self.heading = mode(a)[0][0]
        return self.heading
        #get the mode of all mmsi s heading while docking


# def is_eq(self, lat, lon,heading, mmsi):  #  , heading = None, mmsi = None):
    #     # if mmsi , adds if equals
    #     if abs(self.lon - lon) > self.resolution: return False
    #     if abs(self.lat - lat) > self.resolution: return False
    #     if mmsi not in self.Mmsis:
    #         self.add_ship(mmsi,lat,long,heading)
    #             # if heading: self.ships.append((mmsi,lat,long, heading ))
    #             # else: self.ships.append((mmsi,lat,long ))
    #             # self.Mmsis.append(mmsi)
    #     return True
    # def add_ship(self, mmsi, lat, long, heading):
    #     self.ships.append([mmsi, lat, long, heading])
    #     self.Mmsis.append(mmsi)