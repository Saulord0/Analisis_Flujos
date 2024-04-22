# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 23:53:54 2024

@author: gow_e
"""
import os
import sys
sys.path.append(os.getcwd()+'\\funciones')
from librerias import *

def fechas(tiempos):
    fechas=[]
    delta=datetime.timedelta(hours=6)
    for t in range(len(tiempos[:])):
        x=tiempos[:].data[t]
        decodificacion=[ch.decode('utrf-8') for ch in x]
        d=''.join(str(decodificacion))
        d=d.replace("[",'')
        d=d.replace("]",'')
        d=d.replace(',','')
        d=d.replace("'",'')
        d=d.replace(" ",'')
        d=d[:-6]
        anio=int(d[:4])
        mes=int(d[5:7])
        dia=int(d[-5:-3])
        hora=int(d[-2:])
        dd=datetime.datetime(anio,mes,dia,hora)
        fechas.append(dd)
    return fechas