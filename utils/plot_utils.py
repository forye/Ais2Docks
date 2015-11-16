import matplotlib.pyplot as plt
import math
import config.configuration as cfg
import urllib, cStringIO
import motionless as mo
from scipy.misc import imread
import numpy as np


def get_center_dock_rect(ang =25,size = 200. ,width = 50.,center = (0,0), col = 'y' , alp = 0.5 ):
    r = 0.5 * math.sqrt(width**2 + size**2)
    ang0 = math.asin(0.5 * width / r)
    ang1 = math.pi * 2 *( ang ) / 360
    x = r * ( math.cos(ang0) - math.sin(ang0 + ang1))
    y = r * ( math.cos(ang0) - math.cos(ang0 + ang1))
    print 'x,y,ang',x,y,ang
    x =  center[0] #  + x
    y =  center[1] #  + y
    print 'x,y',x,y
    v= (x ,  y)
    # return rect = plt.Rectangle(v, size,width ,alpha = alp,angle = -ang+90, fc = col)
    return plt.Rectangle(v, width, size ,alpha =alp, angle = ang, fc = col)

def get_center_dock_circ(center =(0,0),r = 10, col = 'r' , alp = 0.8):
    return plt.Circle(center,radius=r ,alpha =alp, fc = col)

def get_arrow(center=(0,0),ang = 0, r = 100, w = 40, col = 'w' , alp = 0.5):
    dy = r * math.sin(math.pi * 2 *( ang + 90) / 360 )
    dx = r * math.cos(math.pi * 2 *( ang + 90) / 360)
    return plt.Arrow(center[0],center[1],dx,dy,width=w, fc=col, alpha=alp)
#plot_center_dock_rect()


    
#circle = plt.Circle((0, 0), radius=120, fc='r')

def get_dock_image(dock, zoom = None,SIZE_X = 640, SIZE_Y= 400):
    if not zoom: zoom = cfg.ZOOM
    MAP_TYPE = 'satellite'
    cmap =mo.CenterMap(lat=dock.lat, lon=dock.lon, maptype=MAP_TYPE, size_x=SIZE_X, size_y=SIZE_Y, zoom =zoom )
    cmap.check_parameters()
    image_path = cmap.generate_url()
    image_file = cStringIO.StringIO(urllib.urlopen(image_path).read())
    img1 = imread(image_file)
    return  img1, image_path


def plot_dock(mdock, idx =None):
    img1,_ = get_dock_image(mdock,SIZE_X=640, SIZE_Y=400)
    plt.imshow(img1, zorder=0) #  matplotlib.image.AxesImage object
    circ =get_center_dock_circ(center =(320, 200))
    plt.gca().add_patch(circ)
    arrow = get_arrow(center=(320,200),ang= mdock.heading  )
    plt.gca().add_patch(arrow)
    plt.xlim((0, 640))
    plt.ylim((0, 400))
    _title = 'Longitude:{0} Latitude:{1}  Heading:{2} Elevation:{3}\nDocked Ships Count: {4}' \
             ' size: {5} to {6}m  width: {7} to {8} \n Classes: {9}'.format(mdock.lon,
                                                mdock.lat, mdock.heading, mdock.depth, len(mdock.Mmsis),
                                                np.nanmin(mdock.size),np.nanmax(mdock.size),np.nanmin(mdock.width),np.nanmax(mdock.width),
                                                [cfg.CLASSES[i] for i in mdock.ships_classes])
    plt.title(_title)
    if idx is not None: plt.savefig(cfg.FIG_G_NAME.format(1+idx))
    else: plt.show()
    plt.close()
