#!/usr/bin/env python

import rrdtool
import os
def crearRRD(alias):
    if os.path.exists(alias+"/"+alias+".rrd") == False:
        try:
            os.makedirs(alias)
        except OSError as e:
            print(f"Error:{e.strerror}")
        ret = rrdtool.create(alias+"/"+alias+".rrd",
                            "--start",'N',
                            "--step",'20',
                            "DS:segmentosUnicast:COUNTER:40:U:U",
                            "DS:paquetesIPv4:COUNTER:40:U:U",
                            "DS:mensajesICMP:COUNTER:40:U:U",
                            "DS:segmentosRecibidos:COUNTER:40:U:U",
                            "DS:datagramasEntrega:COUNTER:40:U:U",            
                            "RRA:AVERAGE:0.5:1:20")
        if ret:
            print (rrdtool.error())
    
crearRRD('Windows')
