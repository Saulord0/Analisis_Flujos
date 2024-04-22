# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 22:59:05 2024

@author: gow_e
"""

import os
import sys
sys.path.append(os.getcwd()+'\\funciones')
from librerias import *

def temperatura(datos,k=6):
    dims=datos.shape
    a=np.zeros((4,dims[1],dims[2]))
    k=6
    while k<=dims[0]-20:
        b=np.zeros((dims[1],dims[2]))
        b2=np.zeros((dims[1],dims[2]))
        for t in range(25):
            variable=datos[k]-273.15
            b+=variable
            b2+=b
            k+=1
            if k==29:
                a[0,:,:]=b/24
                b2=np.zeros((dims[1],dims[2]))
            elif k==53:
                a[1,:,:]=b/24
                b2=np.zeros((dims[1],dims[2]))
            elif k==77:
                a[2,:,:]=b/24
                b2=np.zeros((dims[1],dims[2]))
            elif k==101:
                a[3,:,:]=b/24
                b2=np.zeros((dims[1],dims[2]))
    return a

def radOL(TSK,GLW,K=6):
    dims=GLW.shape
    a=np.zeros((4,dims[1],dims[2]))
    k=6
    while k<=dims[0]-20:
        b=np.zeros((dims[1],dims[2]))
        for t in range(25):
            tsk=TSK[k]
            glw=GLW[k]
            rad_emitida=0.0000000567*0.96*(tsk*tsk*tsk*tsk)
            rad_neta=glw-rad_emitida
            b+=rad_neta
            k+=1
            if k==29:
                a[0,:,:]=b/24
                b=np.zeros((dims[1],dims[2]))
            elif k==53:
                a[1,:,:]=b/24
                b=np.zeros((dims[1],dims[2]))
            elif k==77:
                a[2,:,:]=b/24
                b=np.zeros((dims[1],dims[2]))
            elif k==101:
                a[3,:,:]=b/24
                b=np.zeros((dims[1],dims[2]))
    return a
def tiempos(Tiempo,k=6):
    dim=len(Tiempo)
    a=[]
    k=6
    while k<=dim-20:
        for t in range(25):
            if k==29:
                a.append(Tiempo[k].strftime("%d-%b-%Y"))
            elif k==53:
                a.append(Tiempo[k].strftime("%d-%b-%Y"))
            elif k==77:
                a.append(Tiempo[k].strftime("%d-%b-%Y"))
            elif k==101:
                a.append(Tiempo[k].strftime("%d-%b-%Y"))
            k+=1
    return a
    
def radOC(SWDOWN,ALBEDO,k=6):
    dims=SWDOWN.shape
    a=np.zeros((4,dims[1],dims[2]))
    k=6
    while k<=dims[0]-20:
        b=np.zeros((dims[1],dims[2]))
        for t in range(25):
            swdown=SWDOWN[k]
            albedo=ALBEDO[k]
            rad_neta=swdown*(1-albedo)
            b+=rad_neta
            k+=1
            if k==29:
                a[0,:,:]=b/24
                b=np.zeros((dims[1],dims[2]))
            elif k==53:
                a[1,:,:]=b/24
                b=np.zeros((dims[1],dims[2]))
            elif k==77:
                a[2,:,:]=b/24
                b=np.zeros((dims[1],dims[2]))
            elif k==101:
                a[3,:,:]=b/24
                b=np.zeros((dims[1],dims[2]))
    return a

def albHeats(LH,k=6):
    dims=LH.shape
    a=np.zeros((4,dims[1],dims[2]))
    k=6
    while k<=dims[0]-20:
        b=np.zeros((dims[1],dims[2]))
        for t in range(25):
            lh=LH[k]
            b+=lh
            k+=1
            if k==29:
                a[0,:,:]=b/24
                b=np.zeros((dims[1],dims[2]))
            elif k==53:
                a[1,:,:]=b/24
                b=np.zeros((dims[1],dims[2]))
            elif k==77:
                a[2,:,:]=b/24
                b=np.zeros((dims[1],dims[2]))
            elif k==101:
                a[3,:,:]=b/24
                b=np.zeros((dims[1],dims[2]))
    return a           

def flujos24h(datos):
    data={}
    data['Times']=tiempos(datos['Times'])
    data['T2']=temperatura(datos['T2'])
    data['rad_OL']=radOL(datos['TSK'],datos['GLW'])
    data['rad_OC']=radOC(datos['SWDOWN'],datos['ALBEDO'])
    data['albedo']=albHeats(datos['ALBEDO'])
    data['sensible']=albHeats(datos['HFX'])
    data['latente']=albHeats(datos['LH'])
    data['XLONG']=datos['XLONG']
    data['XLAT']=datos['XLAT']
    
    
    balance_energia=np.full_like(data['rad_OC'], np.nan)
    for i in range(data['rad_OC'].shape[0]):
        balance_energia[i,:,:]=data['rad_OL'][i,:,:] + data['rad_OC'][i,:,:] - data['latente'][i,:,:] - data['sensible'][i,:,:]
    data['balance_energia']=balance_energia
    return data#rad_OL,rad_OC,latente,sensible,balance_energia,albedo,temp


def flujosPeriodo(datos):
    data={}
    dims=datos['T2'].shape
    data['XLONG']=datos['XLONG']
    data['XLAT']=datos['XLAT']
    data['Times']=datos['Times']
    for var in ['rad_OL','rad_OC','latente','sensible','albedo','TSK','T2']:
        a=np.zeros(dims)
        b=np.zeros(dims)
        if var=='rad_OL':
            for t in range(dims[0]):
                b[t]=0.0000000567*0.96*(datos['TSK'][t]*datos['TSK'][t]*datos['TSK'][t]*datos['TSK'][t])
                a[t]=datos['GLW'][t]-b[t]
        elif var=='rad_OC':
            for t in range(dims[0]):
                a[t]=datos['SWDOWN'][t]*(1-datos['ALBEDO'][t])
        elif var=='latente':
            for t in range(dims[0]):
                a[t]=datos['LH'][t]
        elif var=='sensible':
            for t in range(dims[0]):
                a[t]=datos['HFX'][t]
        elif var=='albedo':
            for t in range(dims[0]):
                a[t]=datos['ALBEDO'][t]
        elif var=='TSK':
            for t in range(dims[0]):
                a[t]=datos['TSK'][t]-273.15
        elif var=='T2':
            for t in range(dims[0]):
                a[t]=datos['T2'][t]-273.15
        data[var]=a
    a=np.zeros(dims)
    for t in range(dims[0]):
        a[t]=data['rad_OL'][t]+data['rad_OC'][t]-data['latente'][t]-data['sensible'][t]
    data['balance_energia']=a
    
    return data
    