# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 21:14:58 2024

@author: gow_e

funciones_LU

limites_shape(shapefile1,shapefile2,longitude,latitude)
shapefile1: archivo shapefile de la zona de interés principal
shapefile2: archivo shapefile de las entidades que conforman zona de interes principal
longitude: arreglo 2D de coordenadas XLONG del netcdf
latitude: arreglo 2D de coordenadas XLAT del netcdf
"""
import os
import sys
sys.path.append(os.getcwd()+'\\funciones')
from librerias import *

def shapeToList(shapefile):
    xx=[]
    yy=[]
    for p in range(len(shapefile.boundary.geometry.values)):
        f=shapefile.boundary.geometry.values[p]
        f2=f.xy
        xx.append(f2[0])
        yy.append(f2[1])
    return xx,yy

def delimitaZona(shapefile):
    limite=shapefile.bounds
    xmin=limite.minx[0]-0.5
    xmax=limite.maxx[0]+0.5
    ymin=limite.miny[0]-0.5
    ymax=limite.maxy[0]+0.5
    
    return xmin,xmax,ymin,ymax
def calculaIndices(limites,long,lat):
    ind=[]
    for i in range(len(limites)):
        if i<=1:
            dif=list(abs(long[0,:]-limites[i]))
            x=list(np.where(dif==min(dif)))[0]
        else:
            dif=list(abs(lat[:,0]-limites[i]))
            x=list(np.where(dif==min(dif)))[0]
        ind.append(x[0])
    return ind
    

def limites_shape(shapefile1,shapefile2,longitude,latitude):
    x,y=shapeToList(shapefile1)
    x2,y2=shapeToList(shapefile2)
    limites=delimitaZona(shapefile1)
    indices=calculaIndices(limites,longitude,latitude)
    
    return indices

def fechasTime(tiempos):
    fechas=[]
    delta=datetime.timedelta(hours=6)
    for t in range(len(tiempos[:])):
        x=tiempos[:].data[t]
        d=''.join(str([ch.decode('utf-8') for ch in x ]))
        d=d.replace("[",'')
        d=d.replace("]",'')
        d=d.replace(',','')
        d=d.replace("'",'')
        d=d.replace(" ",'')
        d=d[:-6]
        '''
        print('d[:4]',d[:4])
        print('d[5:7]',d[5:7])
        print('d[-5:-3]',d[-5:-3])
        print('d[-2:]',d[-2:])'''
        dd=datetime.datetime(int(d[:4]),int(d[5:7]),int(d[-5:-3]),int(d[-2:]))
        #fechas.append(d[:-6])
        fechas.append(dd-delta)
    return fechas
   
def leeVariables(archivo,variables,ajuste=False):
    data={}
    data_b={}
    arch=nc.Dataset(archivo)
    for var in variables:
        if var=='T2':
            if ajuste:
                aj=arch['HGT'][0]*0.00652
                tem=arch[var][:]+aj
                data[var]=tem#-273.15
            else:
                data[var]=arch[var][:]#-273.15
        elif var in ['XLONG','XLAT']:
            data[var]=arch[var][0]
        else:
            data[var]=arch[var][:]
        if var=='Times':
            data[var]=fechasTime(arch[var][:])
    arch.close()
    return data

def mascaraLU(LU,datos,variable):
    salida={}
    for uso in np.unique(LU[0]).data:
        if variable != 'Times':
            d=np.full_like(datos[variable],np.nan)
            masc=np.ma.MaskedArray(LU[0]==uso)
            if variable=='XLONG' or variable=='XLAT':
                d=datos[variable]*masc
                d=np.where(d==0,np.nan,d)
            else:
                for t in range(datos[variable].shape[0]):
                    d[t,:,:]=datos[variable][t,:,:]*masc
                    d[t,:,:]=np.where(d[t,:,:]==0,np.nan,d[t,:,:])
            salida[int(uso)]=d
        else:
            salida[int(uso)]=datos['Times']
    return salida

