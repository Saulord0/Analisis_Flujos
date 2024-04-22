# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 15:22:11 2024

@author: gow_e
"""

import os
import sys
sys.path.append(os.getcwd()+'\\funciones')
from librerias import *
from barras_colores import barra

barra_flujos,leyenda_flujos=barra('flujos')
barra_LULC,leyenda_LULC=barra('lulc')
barra_albedo=barra('albedo')
barra_temp=barra('temp')

def LULC1D(datos,serie,dominio,xx,xy,xx2,xy2,limites,ruta,indices=False):
    if indices:
        LU=datos['LU_INDEX'][0,indices[2]:indices[3],indices[0]:indices[1]]
        x=datos['XLONG'][indices[2]:indices[3],indices[0]:indices[1]]
        y=datos['XLAT'][indices[2]:indices[3],indices[0]:indices[1]]
    else:
        LU=datos['LU_INDEX'][0]
        x=datos['XLONG']
        y=datos['XLAT']
    
    vmin,vmax=[1,24]
    fig,ax=plt.subplots(figsize=(10,10),layout='constrained')
    norm=plt.Normalize(vmin=vmin,vmax=vmax)
    mp=ax.pcolor(x,y,LU,cmap=barra_LULC,norm=norm)
    ax.set_title('Uso de suelo\n'+serie[:-1]+' '+serie[-1],fontsize=30)
    ax.set_aspect(1)
    ax.tick_params(labelsize=20)
    ticks=np.linspace(vmin+0.5,vmax-0.5,num=24,endpoint=True)
    #cbar=plt.colorbar(mp,ax=ax)
    cbar=fig.colorbar(mp,ax=ax,shrink=0.6)
    cbar.set_ticks(ticks=ticks,labels=leyenda_LULC,fontsize=10)
    for p in range(len(xx)):
        ax.plot(list(xx)[p],list(xy)[p],'--k')
    for p in range(len(xx2)):
        ax.plot(list(xx2)[p],list(xy2)[p],'k')
    ax.set_xlim(min(min(xx))-0.2,max(max(xx))+0.2)
    ax.set_ylim(min(min(xy))-0.2,max(max(xy))+0.2)
    #fig.tight_layout()
    plt.savefig(ruta+'LULC'+serie+dominio+'.png',dpi=300)

def LULC2D(datosA,serieA,datosB,serieB,dominio,xx,xy,xx2,xy2,limites,ruta,indices=False):
    if indices:
        LUA=datosA['LU_INDEX'][0,indices[2]:indices[3],indices[0]:indices[1]]
        xA=datosA['XLONG'][indices[2]:indices[3],indices[0]:indices[1]]
        yA=datosA['XLAT'][indices[2]:indices[3],indices[0]:indices[1]]
        LUB=datosB['LU_INDEX'][0,indices[2]:indices[3],indices[0]:indices[1]]
        xB=datosB['XLONG'][indices[2]:indices[3],indices[0]:indices[1]]
        yB=datosB['XLAT'][indices[2]:indices[3],indices[0]:indices[1]]
    else:
        LUA=datosA['LU_INDEX'][0]
        xA=datosA['XLONG']
        yA=datosA['XLAT']
        LUB=datosB['LU_INDEX'][0]
        xB=datosB['XLONG']
        yB=datosB['XLAT']
    vmin,vmax=[1,24]
    fig,ax=plt.subplots(1,3,figsize=(20,10))#,layout='constrained')
    fig.suptitle('Uso de suelo',fontsize=45)
    norm=plt.Normalize(vmin=vmin,vmax=vmax)
    mpA=ax[0].pcolor(xA,yA,LUA,cmap=barra_LULC,norm=norm)
    ax[0].set_title(serieA[:-1]+' '+serieA[-1],fontsize=30)
    ax[0].set_aspect(1)
    ax[0].tick_params(left=False,labelleft=None,labelsize=20)

    mpB=ax[1].pcolor(xB,yB,LUB,cmap=barra_LULC,norm=norm)
    ax[1].set_title(serieB[:-1]+' '+serieB[-1],fontsize=30)
    ax[1].set_aspect(1)
    ax[1].tick_params(labelsize=20)
    ticks=np.linspace(vmin+0.5,vmax-0.5,num=24,endpoint=True)
    cbar=fig.colorbar(mpA,ax=ax[2])
    cbar.set_ticks(ticks=ticks,labels=leyenda_LULC,fontsize=20)
    for t in range(len(xx)):
        ax[0].plot(list(xx[t]),list(xy[t]),'--k')
        ax[1].plot(list(xx[t]),list(xy[t]),'--k')
    for t in range(len(xx2)):
        ax[0].plot(list(xx2[t]),list(xy2[t]),'k')
        ax[1].plot(list(xx2[t]),list(xy2[t]),'k')
    ax[0].set_xlim(min(min(xx))-0.2,max(max(xx))+0.2)
    ax[0].set_ylim(min(min(xy))-0.2,max(max(xy))+0.2)
    ax[1].set_xlim(min(min(xx))-0.2,max(max(xx))+0.2)
    ax[1].set_ylim(min(min(xy))-0.2,max(max(xy))+0.2)
    fig.delaxes(ax[2])
    fig.tight_layout()
    plt.savefig(ruta+'LULC'+serieA+'_'+serieB+dominio+'.png',dpi=300)


def grafica1D(datos,nombre,serie,variable,dominio,xx,xy,xx2,xy2,limites,ruta,indices=False):
    flujos=['latente','sensible','balance_energia']
    if 'indices' in locals():
        var=datos[variable][:,indices[2]:indices[3],indices[0]:indices[1]]
        x=datos['XLONG'][indices[2]:indices[3],indices[0]:indices[1]]
        y=datos['XLAT'][indices[2]:indices[3],indices[0]:indices[1]]
    else:
        var=datos[variable][:]
        x=datos['XLONG']
        y=datos['XLAT']
    
    if variable.lower() in flujos:
        vmin,vmax=[-150,400]
        barra_colores,leyenda=barra('flujos')
        num=len(leyenda)
        titulo='Flujo de calor '+variable
    elif variable.lower()=='albedo':
        vmin,vmax=[0,0.3]
        barra_bolores=barra('albedo')
        num=6
        titulo='Albedo'
    elif variable.lower()=='tsk' or variable.lower()=='t2':
        vmin,vmax=[-5,40]
        barra_colores=barra('temp')
        num=10
        if variable.lower()=='tsk':
            titulo='Temperatura en superficie'
        else:
            titulo='Temperatura a 2m'
    
    for t in range(var.shape[0]):
        fig,ax=plt.subplots(figsize=(10,10),layout='constrained')
        norm=plt.Normalize(vmin=vmin,vmax=vmax)
        mp=ax.pcolor(x,y,var[t],cmap=barra_colores,norm=norm)
        ax.set_title(titulo+'\n'+serie[:-1]+' '+serie[-1],fontsize=30)
        ax.set_aspect(1)
        ax.tick_params(labelsize=20)
        ticks=np.linspace(vmin+0.5,vmax-0.5,num=num,endpoint=True)
        cbar=fig.colorbar(mp,ax=ax)
        if 'leyenda' in locals():
            cbar.set_ticks(ticks=ticks,labels=leyenda,fontsize=20)
        else:
            leyenda=alb_str=[str(ti) for ti in ticks ]
            cbar.set_ticks(ticks=ticks,labels=leyenda,fontsize=20)
        for p in range(len(xx)):
            ax.plot(list(xx)[p],list(xy)[p],'--k')
        for p in range(len(xx2)):
            ax.plot(list(xx2)[p],list(xy2)[p],'k')
        ax.set_xlim(min(min(xx))-0.2,max(max(xx))+0.2)
        ax.set_ylim(min(min(xy))-0.2,max(max(xy))+0.2)
        #fig.tight_layout()
        plt.savefig(f'{ruta}{variable}_{nombre}_{serie}_{dominio}_{t}.png',dpi=300)

def grafica2D(datosA,serieA,datosB,serieB,variable,dominio,xx,xy,xx2,xy2,limites,ruta,descripcion):
    flujos=['latente','sensible','balance_energia']
    varA=datosA[variable]
    xA=datosA['XLONG']
    yA=datosA['XLAT']
    varB=datosB[variable]
    xB=datosB['XLONG']
    yB=datosB['XLAT']
     
    if variable.lower() in flujos:
        vmin,vmax=[-150,400]
        barra_colores,leyenda=barra('flujos')
        num=len(leyenda)
        titulo='Flujo de calor '+variable
    elif variable.lower()=='albedo':
        vmin,vmax=[0,0.3]
        barra_bolores=barra('albedo')
        num=6
        titulo='Albedo'
    elif variable.lower()=='tsk' or variable.lower()=='t2':
        vmin,vmax=[-5,40]
        barra_colores=barra('temp')
        num=10
        if variable.lower()=='tsk':
            titulo='Temperatura en superficie'
        else:
            titulo='Temperatura a 2m'
    
    for t in range(varA.shape[0]):
        fig,ax=plt.subplots(1,3,figsize=(20,10))#,layout='constrained')
        fig.suptitle(titulo,fontsize=45)
        norm=plt.Normalize(vmin=vmin,vmax=vmax)
        mpA=ax[0].pcolor(xA,yA,varA[t],cmap=barra_colores,norm=norm)
        ax[0].set_title(serieA[:-1]+' '+serieA[-1],fontsize=30)
        ax[0].set_aspect(1)
        ax[0].tick_params(left=False,labelleft=None,labelsize=20)

        mpB=ax[1].pcolor(xB,yB,varB[t],cmap=barra_LULC,norm=norm)
        ax[1].set_title(serieB[:-1]+' '+serieB[-1],fontsize=30)
        ax[1].set_aspect(1)
        ax[1].tick_params(labelsize=20)
        ticks=np.linspace(vmin+0.5,vmax-0.5,num=num,endpoint=True)
        cbar=fig.colorbar(mpA,ax=ax[2])
        if 'leyenda' in locals():
            cbar.set_ticks(ticks=ticks,labels=leyenda,fontsize=20)
        else:
            leyenda=alb_str=[str(ti) for ti in ticks ]
            cbar.set_ticks(ticks=ticks,labels=leyenda,fontsize=20)
        for t in range(len(xx)):
            ax[0].plot(list(xx[t]),list(xy[t]),'--k')
            ax[1].plot(list(xx[t]),list(xy[t]),'--k')
        for t in range(len(xx2)):
            ax[0].plot(list(xx2[t]),list(xy2[t]),'k')
            ax[1].plot(list(xx2[t]),list(xy2[t]),'k')
        ax[0].set_xlim(min(min(xx))-0.2,max(max(xx))+0.2)
        ax[0].set_ylim(min(min(xy))-0.2,max(max(xy))+0.2)
        ax[1].set_xlim(min(min(xx))-0.2,max(max(xx))+0.2)
        ax[1].set_ylim(min(min(xy))-0.2,max(max(xy))+0.2)
        fig.delaxes(ax[2])
        fig.tight_layout()
        plt.savefig(f'{ruta}{variable}_{descripcion}_{nombre}_{serie}_{dominio}_{t}.png',dpi=300)

def grafSerie(datos):
    fig,ax=plt.subplots(figsize=(20,10),layout='constrained')
    for var in datos.keys():
        #grafica flujos_latentes_series
        lin1,=ax.plot(datos[var],'-ob',linewidth=3,label='Serie 6')
    lin2,=ax.plot(flujos_latentes_series[list(flujos_latentes_series.keys())[1]],'-.r',linewidth=3,label='Serie 7')
    ax.set_xticks(list(horas.index))
    ax.set_xticklabels(horas[0],fontsize=30)
    ax.tick_params(axis='y',labelsize=30)
    ax.set_xlabel('Hora local',fontsize=30)
    fig.suptitle("Flujo de calor latente  [$\mathregular{W m^{-2}}$]",fontsize=40)
    ax.grid()
    fig.legend(handles=[lin1,lin2],loc='center right',fontsize=20)
    plt.savefig(rutas['guarda']+'Serie_CalorLatente_d03_urbano_s7_s6.png', dpi=300)
