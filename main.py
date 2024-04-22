# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 20:49:36 2024

@author: gow_e
"""
import os
import sys
sys.path.append(os.getcwd()+'\\funciones')
from librerias import *
#importa las funciones creadas para analizar los datos
from barras_colores import barra
from funciones_LU import *
from flujos import flujos24h, flujosPeriodo
from graficas import *
#from datos_estaciones import series_estaciones


# Definición de fecha, rutas a archivos (netcdf, shapefiles, barras de colores, salidas de grafica)
fecha='2022-05-02_00'
anio=fecha[:4]
mes=fecha[5:7]
dia=fecha[8:10]
hora=fecha[-2:]
dominio='d02'

#nombre de la carpeta de salidas WRF del operativo IOA
meses={'01':'enero','02':'febrero','03':'marzo','04':'abril','05':'mayo','06':'junio',
       '07':'julio','08':'agosto','09':'septiembre','10':'octubre','11':'noviembre','12':'diciembre'}

# definición de rutas según sistema operativo y/o equipo

ruta_base=os.getcwd()
if 'LUSTRE' in ruta_base:
    linux=True
else:
    linux=False
if 'gow_e' in ruta_base:
    lap='ioa'
else:
    lap='home'

fecha_prueba=date.today().strftime("%m%d%y")

if linux:
    rutas={'Prueba':'/LUSTRE/OPERATIVO/OPERATIVO2/SAULO/Prueba_wrf45/WRF/test/em_real/',
           'operativo':'/LUSTRE/OPERATIVO/OPERATIVO2/EXTERNO-salidas/WRF/'+anio+'/'+mes+'_'+meses[mes]+'/',
           'guardar':f'/LUSTRE/OPERATIVO/OPERATIVO2/SAULO/reporte/salidas_{fecha_prueba}',
           'correcciones':'/LUSTRE/OPERATIVO/OPERATIVO2/correccion_por_sesgo/Matrices_corr_sesgo_horaria_'+dominio.replace('0','')+'/',
           'shapes':'~/Saulo/ShapeFiles_ZMVM/'}
else:
    if lap=='ioa':
        rutas={'Prueba':'C:\\Users\\gow_e\\Documents\\trabajo\\ICayCC\\Reporte_SECTEI_2024\\DatosBienGFS\\salidas\\',
               'operativo':'C:\\Users\\gow_e\\Documents\\trabajo\\ICayCC\\Reporte_SECTEI_2024\\DatosBienGFS\\salidas\\operativo\\',
               'guarda':f'C:\\Users\\gow_e\\Documents\\trabajo\\ICayCC\\Reporte_SECTEI_2024\\salidas_{fecha_prueba}\\',
               'correcciones':'C:\\Users\\gow_e\\Documents\\trabajo\\ICayCC\\DatosBienGFS\\correccion_por_sesgo\\Matrices_corr_sesgo_horaria_'+dominio.replace('0','')+'\\',
               'shapes':'C:\\Users\\gow_e\\Documents\\trabajo\\ICayCC\\Reporte_SECTEI_2024\\DatosBienGFS\\ShapeFiles_ZMVM\\'
               }
        #sys.path.append('C:\\Users\\gow_e\\Documents\\trabajo\\ICayCC\\Reporte_SECTEI_2024\\funciones\\')
    else:
        rutas={'Prueba':'D:\\Documents\\Trabajo\\ICAyCC\\OZONO\\Analisis_Ozono\\DatosBienGFS\\salidas\\',
               'operativo':'D:\\Documents\\Trabajo\\ICAyCC\\OZONO\\Analisis_Ozono\\DatosBienGFS\\salidas\\operativo\\',
               'guarda':f'D:\\Documents\\Trabajo\\ICAyCC\\Reporte_SECTEI_2024\\salidas_{fecha_prueba}\\',
               'correcciones':'D:\\Documents\\Trabajo\\ICAyCC\\OZONO\\Analisis_Ozono\\DatosBienGFS\\correccion_por_sesgo\\Matrices_corr_sesgo_horaria_'+dominio.replace('0','')+'\\',
               'shapes':'D:\\Documents\\Trabajo\\ICAyCC\\OZONO\\Analisis_Ozono\\DatosBienGFS\\ShapeFiles_ZMVM\\'
               }
        #sys.path.append('D:\\Documents\\Trabajo\\ICAyCC\\Reporte_SECTEI_2024\\')

archivos={'operativo':{'Operativo421_s6_d02':'wrfout_d02_2022-05-02_00.nc'},
          'Prueba':{'Operativo451_s6_d03':'WRF451_2022050200_d03_INE6_0_15N.nc',
                    'Operativo451_s7_d03_urbano':'WRF451_2022050200_d03_INE7_2_15N.nc',
                    'Operativo451_s7_d03_urbano_albmod':'WRF451_2022050200_d03_INE7_2_50I.nc'}
          }

shapes={'entidades':'Entidades_ZMVM_WGS84.shp','ZMVM':'ZMVM_poligono_WGS84_B.shp','municipios':'Municipios_ZMVM_WGS84.shp'}

entidades=gpd.read_file(rutas['shapes']+shapes['entidades'])
ZMVM=gpd.read_file(rutas['shapes']+shapes['ZMVM'])
municipios=gpd.read_file(rutas['shapes']+shapes['municipios'])

#crea directorio para guardar graficas
if os.path.exists(rutas['guarda']):
    print(rutas['guarda'], 'existe ')
else:
    os.mkdir(rutas['guarda'])

#Lee variables de los archivos netcdf
variables=['TSK','HGT','XLAT','XLONG','T2','ALBEDO','LU_INDEX','HFX','LH','GLW','SWDOWN','Times']

data_b={}
for datos in archivos.keys():
    for descrip,archivo in archivos[datos].items():
        #print(rutas[datos]+archivo)
        data_b[descrip]=leeVariables(rutas[datos]+archivo,variables)

data_ajuste_b={}
for datos in archivos.keys():
    for descrip,archivo in archivos[datos].items():
        #print(rutas[datos]+archivo)
        data_ajuste_b[descrip]=leeVariables(rutas[datos]+archivo,variables,True)

d2='Operativo421_s6_d02'
d3='Operativo451_s6_d03'

x,y=shapeToList(ZMVM)
x2,y2=shapeToList(entidades)
x3=[]
y3=[]
p=0
while p <len(municipios.boundary.geometry.values):
    ff=municipios.boundary.geometry.values[p]
    try:
        ff2=ff.xy
        x3.append(ff2[0])
        y3.append(ff2[1])
        p+=1
    except:
        p+=1

limites=delimitaZona(ZMVM)
indicesd2=limites_shape(ZMVM,entidades,data_b[d2]['XLONG'],data_b[d2]['XLAT'])
indicesd3=limites_shape(ZMVM,entidades,data_b[d3]['XLONG'],data_b[d3]['XLAT'])


data={}
data_ajuste={}
for descrip in data_b.keys():
    if 's7' in descrip:
        serie='Serie7'
    else:
        serie='Serie6'
    if 'd02' in descrip:
        dominio='d02'
        indices=indicesd2
    else:
        dominio='d03'
        indices=indicesd3
    print(serie+'_'+dominio)
    data[descrip]={}
    data_ajuste[descrip]={}
    for var in data_b[descrip].keys():
        if var=='XLONG' or var=='XLAT':
            data[descrip][var]=data_b[descrip][var][indices[2]:indices[3],indices[0]:indices[1]]
            data_ajuste[descrip][var]=data_ajuste_b[descrip][var][indices[2]:indices[3],indices[0]:indices[1]]
        elif not var=='Times':
            data[descrip][var]=data_b[descrip][var][:,indices[2]:indices[3],indices[0]:indices[1]]
            data_ajuste[descrip][var]=data_ajuste_b[descrip][var][:,indices[2]:indices[3],indices[0]:indices[1]]
        elif var=='Times':
            data[descrip][var]=data_b[descrip][var][:]
            data_ajuste[descrip][var]=data_ajuste_b[descrip][var][:]
del data_b



## ploteo de LULC con dos mapas
for descrip in data.keys():
    if 's7' in descrip:
        serie='Serie7'
    else:
        serie='Serie6'
    if 'd02' in descrip:
        dominio='d02'
        indices=indicesd2
    else:
        dominio='d03'
        indices=indicesd3
    LULC1D(data[descrip],serie,dominio,x,y,x2,y2,limites,rutas['guarda'],False)
    #grafica1D(flujos[descrip],descrip,serie,'latente','d03',x,y,x2,y2,limites,rutas['guarda'],indices)
    
        
doms=['Operativo421_s6_d02','Operativo451_s6_d03','Operativo451_s7_d03_urbano','Operativo451_s7_d03_urbano_albmod']
LULC2D(data['Operativo451_s6_d03'],'Serie6',data['Operativo451_s7_d03_urbano'],'Serie7','d03',x,y,x2,y2,limites,rutas['guarda'])

flujos_24h={}
for descrip in data.keys():
    flujos_24h[descrip]=flujos24h(data[descrip])

flujos={}
for descrip in data.keys():
    flujos[descrip]=flujosPeriodo(data[descrip])


mascara={}
for descrip in flujos.keys():
    mascara[descrip]={}
    for var in flujos[descrip].keys():
        mascara[descrip][var]=mascaraLU(data[descrip]['LU_INDEX'],flujos[descrip],var)


mascara_24h={}
for descrip in flujos.keys():
    mascara_24h[descrip]={}
    for var in flujos_24h[descrip].keys():
        mascara_24h[descrip][var]=mascaraLU(data[descrip]['LU_INDEX'],flujos_24h[descrip],var)



serie={}
variables=['rad_OL','rad_OC','T2','sensible','latente','albedo','TSK','balance_energia']
for descrip in mascara.keys():
    serie[descrip]={}
    for var in variables:
        serie[descrip][var]={}
        for hora in range(24):
            indices_horas=[d for d in range(len(flujos[descrip]['Times'])) if flujos[descrip]['Times'][d].hour==hora]
            serie[descrip][var][hora]=np.nanmean(flujos[descrip][var][indices_horas])

serie_LU={}
variables=['rad_OL','rad_OC','T2','sensible','latente','albedo','TSK','balance_energia']
for descrip in mascara.keys():
    serie_LU[descrip]={}
    for var in variables:
        serie_LU[descrip][var]={}
        for uso in mascara[descrip][var].keys():
            serie_LU[descrip][var][uso]={}
            for hora in range(24):
                indices_horas=[d for d in range(len(mascara[descrip]['Times'][uso])) if mascara[descrip]['Times'][uso][d].hour==hora]
            serie_LU[descrip][var][uso][hora]=np.nanmean(mascara[descrip][var][uso][indices_horas])

