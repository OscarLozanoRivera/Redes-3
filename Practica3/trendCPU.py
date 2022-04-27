import sys
import rrdtool
import time
from Notify import send_alert_attached
rrdpath = 'BD/'
imgpath = 'IMG/'

def actualizarGrafica():
    ultima_lectura = int(rrdtool.last(rrdpath+"trend.rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 3600

    ret = rrdtool.graphv( imgpath+"deteccion.png",
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "--vertical-label=Cpu load",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        "--title=Uso del CPU del agente Usando SNMP y RRDtools \n Detección de umbrales",

                        "DEF:cargaCPU="+rrdpath+"trend.rrd:CPUload:AVERAGE",

                        "VDEF:cargaMAX=cargaCPU,MAXIMUM",
                        "VDEF:cargaMIN=cargaCPU,MINIMUM",
                        "VDEF:cargaSTDEV=cargaCPU,STDEV",
                        "VDEF:cargaLAST=cargaCPU,LAST",

                        "CDEF:umbral50=cargaCPU,50,LT,0,cargaCPU,IF",
                        "CDEF:umbral65=cargaCPU,65,LT,0,cargaCPU,IF",
                        "CDEF:umbral80=cargaCPU,80,LT,0,cargaCPU,IF",
                        "AREA:cargaCPU#00FF00:Carga del CPU",
                        "AREA:umbral50#FFB000:Carga CPU mayor que 50",
                        "AREA:umbral65#FF9F9F:Carga CPU mayor que 65",
                        "AREA:umbral80#FF0000:Carga CPU mayor que 80",
                        "HRULE:80#FF0000:Umbral 80%",
                        "HRULE:65#0040FF:Umbral 65%",
                        "HRULE:50#FFFF90:Umbral 50%",

                        "PRINT:cargaLAST:%6.2lf" )

    #print (ret)

    ultimo_valor=float(ret['print[0]'])
    if ultimo_valor<50:
        print("Funcionamiento Normal")
        return False 
    elif ultimo_valor>50 and ultimo_valor<65:
        print("Funcionamiento Anormal")
        send_alert_attached("Sobrepasa Umbral Bajo",ultimo_valor)
    elif ultimo_valor>65 and ultimo_valor<80:
        print("Funcionamiento Alto")
        send_alert_attached("Sobrepasa Umbral Alto",ultimo_valor)
    elif ultimo_valor>80:
        print("Funcionamiento Crítico")
        send_alert_attached("Sobrepasa Umbral Crítico",ultimo_valor)
    return True



#    send_alert_attached("Sobrepasa Umbral línea base")
#    print("Sobrepasa Umbral línea base")