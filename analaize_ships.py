__author__ = 'Idan'
import pandas as pa
import numpy as np
import matplotlib.pyplot as plt
import config.configuration as cfg
import models.ship as ship

def get_docking_locations():
    '''

    :return:
    docks: list of all lo
    '''
    df= pa.read_csv(cfg.FILENAME,parse_dates=[0],dayfirst=False)

    mmsis = set(df['MMSI'])


    # a list of all MMSI'd ship instances
    ships = []
    for mmsi in mmsis:
        # ships.append( ship.ship(df[df['MMSI'] == df['MMSI'][0]]) )
        a =df[ df['MMSI'] == mmsi ]
        ships.append( ship.ship( a, verbose=False ))
        # ships.append( ship.ship(df[df['MMSI'] == mmsi ] ) )

    c_acc=0
    s_acc=0
    big_acc = 0
    docks = []
    for shp in ships:
        if not shp.is_consistant: c_acc +=1
        if not shp.is_well_measured: s_acc +=1
        if shp.size  > cfg.SHIP_MINIMAL_SIZE and shp.is_well_measured and shp.is_consistant : big_acc +=1
        # docks += shp.get_docking_locations()

    print c_acc,' ships has metadata consistancy problem'
    print s_acc,' ships are not well measured'
    print big_acc,' ships are bigger then ',cfg.SHIP_MINIMAL_SIZE,' m'

    cl = cfg.CLASSES
    el = cfg.ELUMINATE


    def retreave_docks_from_ships(ships):

        # res = []
        docks = []
        str_out = "["
        for shp in ships:
            # if True:# shp.is_consistant and shp.size > 200 : # filtered: 2149  points were found, not filtered: 3360  points were found
            if cl[shp.clas] not in el and shp.is_consistant and shp.is_well_measured and shp.size >= cfg.SHIP_MINIMAL_SIZE : # filtered: 2149 consistant points were found, not filtered: 3360  points were found :  well measurend: 1612  points were found
                # res.append(shp.stops)
                ships_docks = shp.get_docking_locations()[0]
                docks += ships_docks
                dock_string_haha =""
                for dock in ships_docks: dock_string_haha += str(dock[:-1]) +'\n'
                str_out += '{MMSI:' +str( shp.mmsi )  +",Docks:\n" +dock_string_haha + '},'
                # Mmsis[ len( docks ) ] = shp.mmsi
            str_out += ']'
        return docks, str_out

    docks, str2 = retreave_docks_from_ships(ships)
    print len(docks), ' points were found'

    # ar_points = np.array(docks)[:, [1, 2, 3]]
    # BINS = 2000
    # plt.hist(ar_points[:, 0], bins=BINS)
    # histo = np.histogram(ar_points, bins=BINS)
    # plt.show()
    # plt.hist(ar_points[:, 2]%180, bins=BINS)
    open(cfg.DOCKING_LOCATION_RESULT, 'w').write(str2)
    print 'end'

    return docks, ships, str2

# from sklearn.cluster import KMeans
#
# km = KMeans(n_clusters = 500)
# # km = sk.cluster.Kmeans(n_clusters = 500)
# model = km.fit(ar_points)
