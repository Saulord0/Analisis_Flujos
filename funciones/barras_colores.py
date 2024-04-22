# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 02:15:36 2024

@author: gow_e
"""

import os
import sys
sys.path.append(os.getcwd()+'\\funciones')
from librerias import *
import json

ruta=os.getcwd()+'\\barras\\'
#ruta='C:\\Users\\gow_e\\Documents\\trabajo\\ICayCC\\Reporte_SECTEI_2024\\barras\\'
#ruta='D:\\Documents\\Trabajo\\ICAyCC\\Reporte_SECTEI_2024\\barras\\''
with open(ruta+'barras_B.json','r') as archivo:
    data=json.load(archivo)
def barra(variable):
    bar=[]
    leyenda=[]
    if variable=='lulc':
        variable='LULC'
    for k,d in data[variable].items():
        if variable.lower()=='lulc' :
            leyenda.append(d[0])
            bar.append(tuple(d[1]))
        elif variable.lower()=='flujos':
            if d[0]=='':
                leyenda.append('')
            else:
                 leyenda.append(int(d[0]))
            bar.append(tuple(d[1]))
        else:
            bar.append(tuple(d[1]))
    if variable=='flujos':
        bar=np.flipud(bar)
        leyenda=np.flipud(leyenda)
    newcmp=ListedColormap(bar)
    
    if variable.lower()=='lulc' or variable.lower()=='flujos':
        return newcmp, leyenda
    else:
        return newcmp

    
