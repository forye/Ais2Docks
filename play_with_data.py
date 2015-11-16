__author__ = 'Idan'


import pandas as pa
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread
import utils.motionless as mo

import config.configuration as cfg
import services.gmaps_service as gs

import urllib, cStringIO
# data = open(cfg.FILENAME).readlines()

data = pa.read_csv(cfg.FILENAME,parse_dates=[0],dayfirst=False)

df =data



import models.ship as ship

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
for shp in ships:
    if not shp.is_consistant: c_acc +=1
    if not shp.is_well_measured: s_acc +=1
    if shp.size  > 200 and shp.is_well_measured : big_acc +=1
print c_acc,' ships has metadata consistancy problem'
print s_acc,' ships are not well measured'
print big_acc,' ships are bigger the 200'


# df[ df['MMSI']== df['MMSI'][0] ]







lat = np.array(df.Latitude)
lon = np.array(df.Longitude)

# https://developers.google.com/maps/documentation/static-maps/intro
# https://developers.google.com/maps/documentation/javascript/maptypes#MapCoordinates
# world_map = mo.CenterMap(lat=0.0001,lon=0.0001, maptype = 'satellite', size_x=400, size_y=400, zoom =1 ).generate_url()
# get map
# ZOOM = 3  # Each succeeding zoom level doubles the precision in both horizontal and vertical dimensions.
ZOOM = 1
idx = 0
MAP_TYPE = 'satellite'
SIZE_Y = 400
SIZE_X = 640  # 400
SCALE = 2
X =np.array(  df['Latitude'] )
Y =np.array( df['Longitude'] )
# cmap =mo.CenterMap(lat=lat[idx], lon=lon[idx], maptype=MAP_TYPE, size_x=SIZE_X, size_y=SIZE_Y, zoom =ZOOM )
# cmap =mo.CenterMap(lat=0.0000001, lon=0.000001, maptype=MAP_TYPE, size_x=SIZE_X, size_y=SIZE_Y, zoom =ZOOM )
cmap =mo.CenterMap(lat=np.median(X), lon=np.median(Y), maptype=MAP_TYPE, size_x=SIZE_X, size_y=SIZE_Y, zoom =ZOOM )
cmap.check_parameters()
# map_url = cmap.generate_url()
image_path = cmap.generate_url()
    # print cmap.generate_url()
#read image



image_file = cStringIO.StringIO(urllib.urlopen(image_path).read())
img1 = imread(image_file)
# img2 = imread( cStringIO.StringIO(urllib.urlopen(image_path).read()) )

# the only datatype that Pillow can work with is uint8.
# Matplotlib plotting can handle float32 and uint8, but image reading/writing for any format other than PNG is limited to uint8 data
# For RGB and RGBA images, matplotlib supports float32 and uint8 data types. For grayscale, matplotlib supports only float32.
# If your array data does not meet one of these descriptions, you need to rescale it.

# fig1 = plt.figure(1)
# fig1.im


# ax = \
plt.imshow(img1, zorder=0) #  matplotlib.image.AxesImage object
# plt1 =df.plot(kind='scatter', x='Latitude', y='Longitude', zorder=1, xlim =lim[0], ylim=lim[1] )#, ax= ax)
# X =np.array(  df['Latitude'] )
# X =( X - np.mean(X) ) / #np.std(X)
# Y =np.array( df['Longitude'] )
# Y =( Y - np.mean(Y) ) / np.std(Y)

# X =np.array(  df['Latitude'] )
# Y =np.array( df['Longitude'] )
X =( X + 190) * SIZE_X / 360.0    #np.std(X)
# Y =( Y - np.mean(Y) ) / np.std(Y)
Y = (Y + 90 ) * SIZE_Y / 180.0
full_borders = np.array([[-180, 180], [-90, 90]])
lim = full_borders / ZOOM
plt.scatter(   X, Y, color='r' ) #, zorder=1,  xlim =lim[0], ylim=lim[1] )
# plt.axes(ax)

# df.plot(kind='scatter', x='Latitude', y='Longitude', zorder=1)#, ax= ax)
# plt.scatter(x,y,zorder=1)
# plt.show()
# plt.hold()
# ax.
# df.plot(kind='scatter', x='Latitude', y='Longitude', zorder=1)#, ax= ax)


plt.show()
print 'end'


img2 = imread('c:\color\stinkbug.png')

plt.imshow(img2)
# fig1 = plt.figure(1)


# ax = plt.axes((-90,90,-180,180))
# fig1.set_axes(ax)

# plot the routes

# df.plot(kind='scatter', x= 'Latitude' , y ='Longitude', zorder = 1,xlim= (-180,180), ylim = (-90,90))

# ax.set_xlim(-90,90)
# suspeceted_df = x[lambda x,y : occurences(x) > TH and occurences(y) > TH ]

# plt.show()
# port discovery:
# fig1.axes([-90,90],[-180,190])

# fig1.set_canvas(CANVAS)
# plt.axes()
# plt.figure(2)
df.Longitude.hist(bins=300 )



# plt.figure(3)
df.Latitude.hist(bins=1000)
ships = data.groupby(u'MMSI')


# plt.figure(4)
df.plot(kind='hexbin', x='Latitude', y='Longitude', gridsize=75)
# ships()
loc = (lon[0],lat[0])
print gs.elevation([ ( 90.000000000001,-170.000000000001)])
print gs.elevation([ loc ])
print data


'''
60]: ax = df.plot(kind='scatter', x='a', y='b',
   ....:              color='DarkBlue', label='Group 1');
   ....:

In [61]: df.plot(kind='scatter', x='c', y='d',
   ....:         color='DarkGreen', label='Group 2', ax=ax);

'''

'''
test data:
    speed - between 0 and 20
    time: 15 min diffrence , supperate/ mark connected
    Long = -180 to 180
    lat = -90 to 90
    size = dirst_to_bow + dist_to_stern

    for each mmsi , is there a change in the class, size, distances?

are there jumps?
x[n] > mean(x)*1.1 +2.2std(x) # 10% and 2.2srd?
 in time
 in lat/ long
 in heading (for direction indicator)



perhaps: test if moving direction

heading of ships ->  heading of the port! (can be + or -)0 -360- heading from north

first: clean the data:



diffrenciate tasks when time between samples is too large

algorithm:
models:
    ship -> port_List
    port -> ship_List
    relevent_port implements port

minimal_docing_time = 4 hours

depending speed??? weigheted time- distance

minimal_ship_size = 250-200 m
class_black list = a list of classes that 100% are not ships that can dock in the relevent port

occurencs th sugestion = %5 of the time, a ship is docking
th = mean( hist(loc) )- 2.2 std( hist(loc))

1. finding ports ->List of Ports
get the modes of the routes(long,lot) using TH
    the treshold can be docking time:
    test -> measure frequency stability
    4h -> f = 4 samples/h -> search 16 consecutive samples
     -> results tresh-hold to identify long,lat pair that was occupied at least 4 hours
    (from same MMSI or from all?)
.OR.
 search for places where speed is 0 there
 count consecutive points where speed==0
 measure the time between them. if >=4 h. its a doc!

2. filtering ports by class and size:

    for each ship that was in the port,
        if the ship class is in the class_black list:
            discard the port
        if the ships_size is >= minimal_ship_size:
            discard the port

2.5: refine:
    using directioning make sure that the ship has changed course going and returning from a port
    any ( Avg ( direction(before) ) dot Avg ( direction(after) ) < 0  )
    .or.
    measure_angle_of_change<-arccos( avg(dir(befoire) dot avg(dir(after)/ abs(avg(dir(befoire))times abs(avg(dir(after))  )

rate:

3. get list of ships that had fucked up their ais class - not tankers
   get list of ships that had fucked up their ais class - are tankers

4. get list of ships that had fucked up their ais size - not tankers
   get list of ships that had fucked up their ais size - are tankers



for ports that are in


reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))


.or.


mapp all the docs

measure the avarage size , maximal, minimal( without the lowest 5%)

ig this is smaller then 250 meters

drop it
is so, create a and iamage with a tectangular with avrange size/ max size
'''




'''
 data.info()
<class 'pandas.core.frame.DataFrame'>
Int64Index: 56057 entries, 0 to 56056
Data columns (total 12 columns):
Time                   56057 non-null datetime64[ns]
MMSI                   56057 non-null int64
Latitude               56057 non-null float64
Longitude              56057 non-null float64
Speed                  55880 non-null float64
Heading                56057 non-null int64
Class                  56057 non-null int64
Size                   56057 non-null int64
DistanceToBow          55999 non-null float64
DistanceToStern        55997 non-null float64
DistanceToPort         55997 non-null float64
DistanceToStarboard    55997 non-null float64
dtypes: datetime64[ns](1), float64(7), int64(4)
memory usage: 5.6 MB

 data.keys()
Out[11]:
Index([u'Time', u'MMSI', u'Latitude', u'Longitude', u'Speed', u'Heading',
       u'Class', u'Size', u'DistanceToBow', u'DistanceToStern',
       u'DistanceToPort', u'DistanceToStarboard'],
      dtype='object')

  http://pandas.pydata.org/pandas-docs/stable/10min.html
  http://pandas.pydata.org/pandas-docs/stable/

  http://geoffboeing.com/2014/08/visualizing-summer-travels-part-5-python-matplotlib/
  https://developers.google.com/maps/documentation/elevation/intro

        scatter hist
    http://matplotlib.org/examples/pylab_examples/custom_cmap.html
    http://stats.stackexchange.com/questions/31726/scatterplot-with-contour-heat-overlay


Define at least three docks and their properties:
Location
Direction/Angle
 Dimensions (maximum ship size, depth/draught, width and etc.)
 Any additional properties such as the oil type (crude oil/refined product oil),
commodity movement (import/export) and etc.




The variables Class, Size, DistanceToBow, DistanceToStern, DistanceToPort,
DistanceToStarboard are entered manually and may be incorrect also by the
damaged signal or in mistake or in purpose by the ship operator in order to
distort the ship profile.
'''


'''
a unique dock, designed for oil transportation
only and handles ships 250 meters long and larger. This dock will never
accommodate smaller ships, for reasons of economical inefficiency.
'''
# date_parser
#
# features = []
# for i,col in enumerate( data[0].split(',') ):
#     features.append(col)
#
#
# ships = []
# for i,row in enumerate(data[1:]):
#     ship = {}
#     for j , feature in row.split(','):
#         ship[features[j]] = feature
#
#
#
#
#
#
#



# df.plot(kind='scatter', x='Latitude', y='Longitude', zorder=1)#, ax= ax)