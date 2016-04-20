#!/usr/bin/env python
# Lunch-Bytes Seminar, Apr 6 2016
# Basic geographic/cartographic plotting for geophysical applications in Python

# The different 'import' calls of Basemap and matplotlib you can use

import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap,interp
from mpl_toolkits.basemap import cm
from netCDF4 import Dataset
from scipy.ndimage.filters import minimum_filter, maximum_filter
import urllib

# Map projections and orientation

## Polar region view 

plt.figure(num=1,figsize=(6,6))
m = Basemap(projection = 'nplaea', boundinglat=10,lon_0 = 270,resolution='l')
m.drawcoastlines()
m.drawparallels(np.arange(-80, 81, 20),labels=[1,0,0,0],fontsize=10)
m.drawmeridians(np.arange(-180, 181, 20),labels=[0,0,0,1],fontsize=10)
m.drawcountries()
dataRetrieve = urllib.URLopener(); 
data_url = 'ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis.dailyavgs/pressure/air.2014.nc'; data_file = 'air.2014.nc'; 
os.chdir('/home/disk/manta9/awsmith/lunch-bytes/'); 
data = dataRetrieve.retrieve(data_url,data_file);
datafile = Dataset(data[0],'r');
lon = datafile.variables['lon'][:]; 
lat = datafile.variables['lat'][:]; 
[lon,lat] = np.meshgrid(lon,lat); 
X,Y = m(lon,lat); 
t850 = datafile.variables['air'][5,2,:,:];  
plt.contourf(X,Y,t850-273.15,np.arange(-15,26,1),cmap = 'jet')
plt.hold(True)
m.contour(X,Y,t850-273.15,levels=[0.0],colors='black',linestyles='-',linewidths=3)
plt.title('850-hPa Temperature, January 6, 2014 Polar Vortex Event',fontsize=10)

## Midlatitude regions

plt.figure(num=2,figsize=(6,6))
m = Basemap(llcrnrlon=0,llcrnrlat=-80,urcrnrlon=360,urcrnrlat=80,projection='mill',resolution='l')
m.drawcoastlines()
m.drawparallels(np.arange(-40,41,10),labels=[1,1,0,0],fontsize=10)
m.drawmeridians(np.arange(0,360,60),labels=[0,0,0,1],fontsize=10)
m.drawcountries()

data_url = 'ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis.dailyavgs/pressure/hgt.2014.nc'; data_file = 'hgt.2014.nc';  
os.chdir('/home/disk/manta9/awsmith/lunch-bytes/'); 
data = dataRetrieve.retrieve(data_url,data_file);
datafileGPHT = Dataset(data[0],'r');

data_url = 'ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis.dailyavgs/pressure/uwnd.2014.nc'; data_file = 'uwnd.2014.nc';  
os.chdir('/home/disk/manta9/awsmith/lunch-bytes/'); 
data = dataRetrieve.retrieve(data_url,data_file);
datafileU = Dataset(data[0],'r');

data_url = 'ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis.dailyavgs/pressure/vwnd.2014.nc'; data_file = 'vwnd.2014.nc';
os.chdir('/home/disk/manta9/awsmith/lunch-bytes/');
data = dataRetrieve.retrieve(data_url,data_file);
datafileV = Dataset(data[0],'r');

lon = datafileU.variables['lon'][:];
lat = datafileU.variables['lat'][:];
[lon,lat] = np.meshgrid(lon,lat);

X,Y = m(lon,lat); 

u1000 = datafileU.variables['uwnd'][5,2,:,:];
v1000 = datafileV.variables['vwnd'][5,2,:,:]; 
gpht500 = datafileGPHT.variables['hgt'][5,5,:,:];
h1 = m.contour(X,Y,gpht500,levels=np.arange(np.min(gpht500),np.max(gpht500)+100,100),colors='black',linewidths=2)
plt.clabel(h1, inline=1, fontsize=8)
h1 = m.quiver(X,Y,u1000,v1000,edgecolor = 'k',facecolor='blue',pivot='mid')
QK = plt.quiverkey(h1,0.95,1.05,25, '25 m/s', labelpos='E', fontproperties={'weight':'bold'})
plt.title('1000-hPa (500-hPa) Wind & Geo Ht, January 6, 2014 Polar Vortex Event',fontsize=10)

## Tropical regions

plt.figure(num=3,figsize=(6,6))
m = Basemap(lat_0=15,lon_0=100,projection='ortho',resolution='l')
m.drawcoastlines()
m.drawparallels(np.arange(-25,30,5))
m.drawmeridians(np.arange(60,160,20))
m.drawcountries()
dataRetrieve = urllib.URLopener();
data_url = 'ftp://ftp.cdc.noaa.gov/Datasets/gpcp/precip.mon.mean.nc'; data_file = 'precip.mon.mean.nc';
os.chdir('/home/disk/manta9/awsmith/lunch-bytes/');
data = dataRetrieve.retrieve(data_url,data_file);
datafilePRCP = Dataset(data[0],'r');

lon = datafilePRCP.variables['lon'][:];
lat = datafilePRCP.variables['lat'][:];
lat_trop = np.where((lat >= -25) & (lat <= 25)); 
lat_tband = lat[lat_trop];
timevec = datafilePRCP.variables['time'][:];
import datetime

d = datetime.date(2014,1,1); 
indx = np.where(timevec == (d.toordinal()/11))[0][0];
[lon,lat_tband] = np.meshgrid(lon,lat_tband);

X,Y = m(lon,lat_tband);
prcpsfc = datafilePRCP.variables['precip'][indx,:,:];
clevs = [0,0.1,0.25,0.5,0.75,1,1.5,2.0,3.0,4.0,5.0,7.0,10.0,15.0,20.0,25.0,30.0]

import matplotlib.colors
cm_prcp = ((254,254,254),(9,45,187),(18,125,202),(5,170,158),(0,237,41),(180,225,45),(240,242,51),(248,186,47),(215,157,34),(246,120,40),(248,40,25),(216,67,156),(213,69,240),(252,137,174),(254,254,254));

cm_prcp = np.divide(cm_prcp,255.0);
cm_prcp = tuple(cm_prcp);

cmap_prcp = matplotlib.colors.ListedColormap(cm_prcp,'cmap_prcp');

h2 = m.contourf(X,Y,np.squeeze(prcpsfc[lat_trop,:]),32,cmap=cmap_prcp) #cm.s3pcpn)
cbar = m.colorbar(h2,ticks=np.arange(0,35,5),location='right',pad="2%")
cbar.set_label('mm')
plt.title('January 2014 Monthly Average Surface Precipitation, Tropical Band',fontsize=10) 

## Others

# Plotting barbs, masking fields (land, ocean) and alpha-transparency

plt.figure(num=4,figsize=(6,6))
m = Basemap(llcrnrlon=-95.,llcrnrlat=20.,urcrnrlon=-80.,urcrnrlat=35.,projection='lcc',lat_1=20.,lat_2=40.,lon_0=-60.,resolution ='l',area_thresh=1000.)
m.drawcoastlines()
m.drawcountries()
m.drawparallels(np.arange(20,36,2),labels=[1,0,0,0])
m.drawmeridians(np.arange(-95,-78,2),labels=[0,0,0,1])

os.chdir('/home/disk/manta14/awsmith/umcm/umcm_runs/katrina_awo_gfs10')
file = Dataset('wrfout_d01_2005-08-29_12:00:00','r'); 
U = np.squeeze(file.variables['U10'][:,:]);
V = np.squeeze(file.variables['V10'][:,:]);
REFD = np.squeeze(file.variables['REFD'][:,:]); 
lon = np.squeeze(file.variables['XLONG'][:,:]);
lat = np.squeeze(file.variables['XLAT'][:,:]);

U,V = np.multiply(U,1.94384449),np.multiply(V,1.94384449); 
XA,YA = m(lon,lat); 

os.chdir('/home/disk/manta14/awsmith/umcm/umcm_runs/katrina_awo_gfs10/output/')
file = Dataset('umwmout_2005-08-29_12:00:00.nc','r'); 
SWH = np.squeeze(file.variables['swh'][:,:]);
lonw = np.squeeze(file.variables['lon'][:,:]); 
latw = np.squeeze(file.variables['lat'][:,:]); 

XW,YW = m(lonw,latw); 

m.contourf(XW,YW,SWH,np.arange(0,31,1),cmap='jet')
m.barbs(XA[0:-1:8,0:-1:8],YA[0:-1:8,0:-1:8],U[0:-1:8,0:-1:8],V[0:-1:8,0:-1:8],barbcolor='k',flagcolor='r',linewidth=0.5)
plt.title('Hurricane Katrina (2005) SWH (m) & Surface Winds (kt), August 29 1200 UTC',fontsize=8)
## Add land mask over 
m.fillcontinents(color='w')
m.drawcountries()
m.drawstates()

## Add ocean mask over
plt.figure(num=5,figsize=(6,6))
m = Basemap(llcrnrlon=-95.,llcrnrlat=20.,urcrnrlon=-80.,urcrnrlat=35.,projection='lcc',lat_1=20.,lat_2=40.,lon_0=-60.,resolution ='l',area_thresh=1000.)
m.drawcoastlines()
m.drawcountries()
m.drawparallels(np.arange(20,36,2),labels=[1,0,0,0])
m.drawmeridians(np.arange(-95,-78,2),labels=[0,0,0,1])
import mpl_toolkits.basemap
REFD_OM = mpl_toolkits.basemap.maskoceans(lon,lat,REFD,'True','l');

## Use another custom colormap

cm_refd = ((255,255,255),(240,240,240),(204,204,204),(157,218,219),(152,205,249),(54,152,251),(0,120,255),(0,102,202),(1,180,16),(6,218,45),(201,255,154),(255,255,102),(255,151,16),(249,72,5),(232,0,2),(174,0,0),(121,0,170),(203,0,204),(255,150,255),(251,222,250),(255,255,255));

cm_refd = np.divide(cm_refd,255.0);
cm_refd = tuple(cm_refd);

cmap_refd = matplotlib.colors.ListedColormap(cm_refd,'cmap_refd');

h3 = m.contourf(XA,YA,REFD_OM,np.arange(1,54,3),cmap=cmap_refd)
cbar = m.colorbar(h3,ticks=np.arange(0,65,5),location='right',pad="2%")
cbar.set_label('dBZ')
plt.title('Hurricane Katrina (2005) RR (dBZ), August 29 1200 UTC (Ocean Masked)',fontsize=8)

# Basic map overlays for terrain, Blue Marble, etc

plt.figure(num=6,figsize=(12,6))
from netCDF4 import Dataset, num2date
import time, calendar, datetime, numpy
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import urllib, os
# data downloaded from the form at
# http://coastwatch.pfeg.noaa.gov/erddap/tabledap/apdrcArgoAll.html
filename, headers = urllib.urlretrieve('http://coastwatch.pfeg.noaa.gov/erddap/tabledap/apdrcArgoAll.nc?longitude,latitude,time&longitude>=0&longitude<=360&latitude>=-90&latitude<=90&time>=2010-01-01&time<=2010-01-08&distinct()')
dset = Dataset(filename)
lats = dset.variables['latitude'][:]
lons = dset.variables['longitude'][:]
time = dset.variables['time']
times = time[:]
t1 = times.min(); t2 = times.max()
date1 = num2date(t1, units=time.units)
date2 = num2date(t2, units=time.units)
dset.close()
os.remove(filename)
# draw map with markers for float locations
m = Basemap(projection='hammer',lon_0=180)
x, y = m(lons,lats)
m.shadedrelief(alpha = 0.6)
m.scatter(x,y,3,marker='o',color='k')
plt.title('Locations of %s ARGO floats active between %s and %s' %\
        (len(lats),date1,date2),fontsize=8)
plt.show()

plt.figure(num=7,figsize=(12,6))
m = Basemap(projection='hammer',lon_0=180)
x, y = m(lons,lats)
m.etopo()
m.scatter(x,y,3,marker='o',color='k')
plt.title('Locations of %s ARGO floats active between %s and %s' %\
        (len(lats),date1,date2),fontsize=8)
plt.show()

plt.figure(num=8,figsize=(12,6))
m = Basemap(projection='hammer',lon_0=180)
x, y = m(lons,lats)
m.bluemarble()
m.scatter(x,y,3,marker='o',color='r')
plt.title('Locations of %s ARGO floats active between %s and %s' %\
        (len(lats),date1,date2),fontsize=8)
plt.show()

# Streamplotting applications - courtesy Brandon Kerns

os.chdir('/home/disk/manta9/awsmith/lunch-bytes')
run slp_winds_refl

# Inset maps - hurricane track application

plt.figure(num=9,figsize=(12,12))
ax = plt.subplot(111)
m = Basemap(llcrnrlon=-95.,llcrnrlat=20.,urcrnrlon=-80.,urcrnrlat=35.,projection='lcc',lat_1=20.,lat_2=40.,lon_0=-60.,resolution ='l',area_thresh=1000.)
m.drawcoastlines()
m.drawcountries()
m.drawparallels(np.arange(20,36,2),labels=[1,0,0,0])
m.drawmeridians(np.arange(-95,-78,2),labels=[0,0,0,1])

## Load d01 winds
os.chdir('/home/disk/manta14/awsmith/umcm/umcm_runs/katrina_awo_gfs10')
file = Dataset('wrfout_d01_2005-08-29_12:00:00','r');
U = np.squeeze(file.variables['U10'][:,:]);
V = np.squeeze(file.variables['V10'][:,:]);
REFD = np.squeeze(file.variables['REFD'][:,:]);
lon = np.squeeze(file.variables['XLONG'][:,:]);
lat = np.squeeze(file.variables['XLAT'][:,:]);

U,V = np.multiply(U,1.94384449),np.multiply(V,1.94384449);
XA,YA = m(lon,lat);
WND = np.sqrt(U**2 + V**2); 

## Load wind colormap
cm_wspd = ((255,255,255),(210,189,254),(1,162,252),(0,240,255),(2,236,199),(4,214,125),(7,193,58),(37,189,8),(108,211,6),(179,234,8),(255,255,0),(255,228,0),(255,201,0),(255,171,4),(255,129,6),(255,80,0),(255,33,3),(237,3,12),(189,1,49),(139,0,96),(80,4,138));

cm_wspd = numpy.divide(cm_wspd,255.0);
cm_wspd = tuple(cm_wspd);

cmap_wspd = matplotlib.colors.ListedColormap(cm_wspd,'cmap_wspd');

## Load Katrina's track 
katrinaTrack = np.load('/home/disk/manta9/awsmith/vt/af_gfs10_katrina_test2.npy'); 
katrinaLons,katrinaLats = katrinaTrack[:,0,0,0,1],katrinaTrack[:,0,0,0,0]; 
XK,YK = m(katrinaLons,katrinaLats); 

h5 = m.contourf(XA,YA,WND,np.arange(0,165,5),cmap=cmap_wspd);
h6 = m.plot(XK[0:-1:6],YK[0:-1:6],color='black',marker='o',markersize=8,linewidth=2,label="Katrina (2005)"); 

cbar = m.colorbar(h5,ticks=np.arange(0,165,5),location='right',pad="2%")
cbar.set_label('kt')
plt.title('Hurricane Katrina (2005) Surface Winds (kt), August 29 1200 UTC',fontsize=11)
plt.legend(loc=1,fancybox=True,shadow=True)

## Set up inset mapping
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid.anchored_artists import AnchoredSizeBar

xins1,yins1 = m(-90.0,28.5);
xins2,yins2 = m(-88,30.5);

m.drawparallels(np.arange(28.5,32.5,2),linewidth=3)
m.drawmeridians(np.arange(-90,-86,2),linewidth=3)

#m.plot([xins1,xins1],[yins1,yins2],color='black',linewidth=2)
#m.plot([xins1,xins2],[yins2,yins2],color='black',linewidth=2)
#m.plot([xins2,xins2],[yins2,yins1],color='black',linewidth=2)
#m.plot([xins2,xins1],[yins1,yins1],color='black',linewidth=2)

axins = zoomed_inset_axes(ax, 3, loc=4)
xins1,yins1 = m(-90.0,28.5);
xins2,yins2 = m(-88,30.5);

axins.set_xlim(xins1,xins2);
axins.set_ylim(yins1,yins2);
plt.xticks(visible=False)
plt.yticks(visible=False)

m2 = Basemap(projection='stere',lon_0 = -89.0,lat_0 = 29.50,llcrnrlat=28.5,urcrnrlat=30.5,llcrnrlon=-90.0,urcrnrlon=-88.0,rsphere=6371200.,resolution='h',area_thresh=10000,ax=axins)
m2.drawcoastlines()
m2.drawcountries()
m2.drawstates()

parallels = numpy.arange(28.4,30.6,0.5)
m2.drawparallels(parallels)
meridians = numpy.arange(-90.1,-87.9,0.5)
m2.drawmeridians(meridians)
XZM,YZM = m2(lon,lat); 

m2.contourf(XZM,YZM,WND,np.arange(0,165,5),cmap=cmap_wspd);

plt.title('Lk Ponchartrain/Bay St. Louis',fontsize=10,fontweight='bold')

