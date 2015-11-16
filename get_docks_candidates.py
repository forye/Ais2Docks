__author__ = 'Idan'


import numpy as np
import pandas as pa
from scipy.stats import mode

import analaize_ships as an
import models.dock as dck
import models.ship as ship

import config.configuration as cfg
import services.gmaps_service as gm

import matplotlib.pyplot as plt
import utils.plot_utils as pu


def get_dock_elevation(dock):
    # from google api
    dock.depth = gm.elevation((dock.lat, dock.lon))[0]['elevation']
    return dock.depth

def update_new_docks(docks_list, new_docks, mmsi):
    '''

    :param docks_list: a list of already process docks
    :param new_docks: a list of new, to be process docks
    :return:
    porst: the updated docks list
    '''
    if not docks_list:
        docks_list = []
    for new_dock_prm in new_docks:
        new_dock = dck.dock(new_dock_prm[1], new_dock_prm[2], new_dock_prm[3], mmsi)
        exists = False
        if docks_list:
            for _dock in docks_list:
                if _dock.is_equals(new_dock):
                    exists = True
                    if mmsi not in _dock.Mmsis:
                        _dock.Mmsis.append( mmsi )
                    break
        if not exists:
            docks_list.append(new_dock)
    return docks_list



df= pa.read_csv(cfg.FILENAME,parse_dates=[0],dayfirst=False)
mmsis = set(df['MMSI'])  # a list of all MMSI'd ship instance
ships = []
for mmsi in mmsis:
    temp = ship.ship(df[df['MMSI'] == mmsi], verbose=False)
    ships.append(temp)

cl = cfg.CLASSES
el = cfg.ELUMINATE
docks = []
str2 = "["
for shp in ships:
    if cl[shp.clas] not in el and shp.is_consistant \
            and shp.is_well_measured and shp.size >= cfg.SHIP_MINIMAL_SIZE:                   # filtered: 2149 consistant points were found, not filtered: 3360  points were found :  well measurend: 1612  points were found
        #  docks, minimal_doc_time_idxs_list, stops_indexs = shp.get_docking_locations()
        ships_docking_history = shp.get_docking_locations()[0]
        for new_dock_prm in ships_docking_history:
            new_dock = dck.dock(new_dock_prm[1], new_dock_prm[2], new_dock_prm[3], shp.mmsi)
            exists = False
            if docks:
                for _dock in docks:
                    if _dock.is_equals(new_dock):
                        exists = True
                        # add_ship=True
                        # for ship1 in _dock.ships:
                        #     if ship1.mmsi == shp.mmsi:
                        #         add_ship = False
                        #         break
                        # if add_ship: _dock.ships.append(shp)

                        break
            if not exists:
                new_dock.ships.append(shp)
                docks.append(new_dock)


                # if _dock.ships:
                        #     if _dock
                        # if shp.mmsi not in _dock.Mmsis:
                        #     _dock.Mmsis.append(shp.mmsi)

        # docks = update_new_docks(docks, ships_docking_history, shp.mmsi)




for _dock in docks:
    _dock.Mmsis = set(_dock.Mmsis)  # ugly fix


str2= "["
for _dock in docks:
    # dock.refine_heading()
    str2 += '[' + str(( _dock.lat, _dock.lon, _dock.heading  )) + '],'
str2 += ']'
open(cfg.DOCKING_LOCATION_RESULT2, 'w').write(str2)


print 'total candidates: ', len(docks)
for n in range(len(docks)):
    mdock = docks[n]
    mdock.Mmsis = set ( df[df["Latitude"] - mdock.lat < mdock.resolution][df["Longitude"] - mdock.lon < mdock.resolution]["MMSI"] )
    # dock_size=[]
    # dock_width=[]
    dock_class=[]
    for shp in ships:
        if shp.mmsi in mdock.Mmsis:
            if cl[shp.clas] not in el and shp.is_consistant \
            and shp.is_well_measured and shp.size >= cfg.SHIP_MINIMAL_SIZE:
                dock_class.append( shp.clas )
                mdock.size.append( shp.size )
                mdock.width.append(shp.dist_2_starboard + shp.dist_2_port)
    dock_class.sort()
    mdock.ships_classes =list( set(dock_class))
    mdock.depth = get_dock_elevation(mdock)
    pu.plot_dock(mdock, n)



    # for shp in ships:
    #     if cl[shp.clas] not in el and shp.is_consistant \
    #             and shp.is_well_measured and shp.size >= cfg.SHIP_MINIMAL_SIZE:
    #

    # a = map(dd.is_in_dock, np.array( df['Latitude'],df['Longitude']) )
    # dd.is_in_dcok( df['Latitude'],df['Longitude'])
    # df[  ]

print "end"
