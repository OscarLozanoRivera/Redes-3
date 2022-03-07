from asyncio import sleep
from multiprocessing import Lock
from os import setgid
import time
import rrdtool
from consultas.getSNMP import consultaSNMP
from consultas.graphRRD import graficar
from datetime import datetime

def actualizar(agente,tiempos):
    unicast = 0
    paquetes = 0
    mensajes = 0
    segmentos = 0
    datagramas = 0
    alias=agente['alias']
    comunidad=agente['comunidad']
    ip=agente['ip']
    tiempoInicio=tiempos[0]
    tiempoFin=tiempos[1]
    while 1:
        if datetime.now().time().hour != tiempoInicio[0] and datetime.now().time().minute != tiempoInicio[1] :
            print("Esperando la hora")
            time.sleep(10)
        else:
            break
    while 1:
        if ip=='192.168.0.16':
            oid = '1.3.6.1.2.1.2.2.1.11.14'
        else:
            oid = '1.3.6.1.2.1.2.2.1.11.1'

        unicast = int(
            consultaSNMP(comunidad,ip,
                        oid).split()[2])
        paquetes = int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.4.3.0').split()[2])
        mensajes=int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.5.8.0').split()[2])
        segmentos=int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.6.10.0').split()[2])
        datagramas=int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.7.1.0').split()[2])

        valor = "N:" + str(unicast) + ':' + str(paquetes) + ':' + str(mensajes)+ ':' + str(segmentos) + ':' + str(datagramas)
        #print(valor)
        rrdtool.update(alias+"/"+alias+'.rrd', valor)
        rrdtool.dump(alias+"/"+alias+'.rrd',alias+"/"+alias+'.xml')
        time.sleep(1)

        def calcularTiempo():
            if tiempoFin[0] < tiempoInicio[0]:
                segundos=(tiempoFin[0]*3600+tiempoFin[1]*60)+((3600*24)-(tiempoInicio[0]*3600+tiempoInicio[1]*60))
            else:
                segundos=(tiempoFin[0]*3600+tiempoFin[1]*60)-(tiempoInicio[0]*3600+tiempoInicio[1]*60)
            print(segundos)
            return segundos
        if datetime.now().time().hour == tiempoFin[0] and datetime.now().time().minute == tiempoFin[1]:
            print("Tiempo Cumplido")
            
            graficar(alias,calcularTiempo())
            return

#actualizar({'alias':'Linux','comunidad':'comunidadASR','ip':'localhost'})