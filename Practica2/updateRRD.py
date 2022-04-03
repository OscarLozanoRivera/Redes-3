from asyncio import sleep
from multiprocessing import Lock
from os import setgid
import time
import rrdtool
from getSNMP import consultaSNMP
from datetime import datetime

def actualizar(cliente,agente,comunidad):
    while 1:
        segmentosIn = 0
        segmentosOut = 0
        segmentosIn=int(
            consultaSNMP(comunidad,agente,
                        '1.3.6.1.2.1.6.10.0').split()[2])
        segmentosOut=int(
            consultaSNMP(comunidad,agente,
                        '1.3.6.1.2.1.6.11.0').split()[2])

        valor = "N:" + str(segmentosIn) + ':' + str(segmentosOut)
        print(valor)
        rrdtool.update(cliente+'.rrd', valor)
        rrdtool.dump(cliente+'.rrd',cliente+'.xml')
        time.sleep(1)


actualizar('practica2','192.168.0.112','comunidadASR')

