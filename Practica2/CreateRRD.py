#!/usr/bin/env python

import rrdtool
ret = rrdtool.create("practica2.rrd",
                     "--start",'N',
                     "--step",'20',
                     "DS:segmentosIn:GAUGE:120:U:U",
                     "DS:segmentosOut:GAUGE:120:U:U",
                     "RRA:AVERAGE:0.5:1:100")

if ret:
    print (rrdtool.error())
