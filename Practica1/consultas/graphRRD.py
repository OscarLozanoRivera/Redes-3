import rrdtool
import time

def graficar(alias,segundos):
    #Grafica desde el tiempo actual menos diez minutos
    tiempoActual=int(time.time())
    tiempoInicio=tiempoActual - (segundos)

    ret = rrdtool.graph( alias+"/unicast.png",
                        "--start",str(tiempoInicio),
                        "--end","N",
                        "--vertical-label=Bytes/s",
                        "--title=Paquetes unicast que ha recibido una interfaz",
                        "DEF:segUnicast="+alias+"/"+alias+".rrd:segmentosUnicast:AVERAGE",
                        "CDEF:escalaIn=segUnicast,8,*",
                        "LINE3:escalaIn#00FF00:Segmentos unicast recibidos"
                        )

    ret = rrdtool.graph( alias+"/paquetes.png",
                        "--start",str(tiempoInicio),
                        "--end","N",
                        "--vertical-label=Bytes/s",
                        "--title=Paquetes recibidos a protocolos IPv4, incluyendo errores",
                        "DEF:paqipv4="+alias+"/"+alias+".rrd:paquetesIPv4:AVERAGE",
                        "CDEF:escalaIn=paqipv4,8,*",
                        "LINE3:escalaIn#FF0000:Paquetes de prot. IPv4"
                        )
                        
    ret = rrdtool.graph( alias+"/mensajes.png",
                        "--start",str(tiempoInicio),
                        "--end","N",
                        "--vertical-label=Bytes/s",
                        "--title=Mensajes ICMP echo que ha enviado el agente",
                        "DEF:menICMP="+alias+"/"+alias+".rrd:mensajesICMP:AVERAGE",
                        "CDEF:escalaIn=menICMP,8,*",
                        "LINE3:escalaIn#00FF00:Mensajes ICMP echo enviados"
                        )

    ret = rrdtool.graph( alias+"/segmentos.png",
                        "--start",str(tiempoInicio),
                        "--end","N",
                        "--vertical-label=Bytes/s",
                        "--title=Segmentos recibidos, incluyendo los errores",
                        "DEF:segRecibidos="+alias+"/"+alias+".rrd:segmentosRecibidos:AVERAGE",
                        "CDEF:escalaIn=segRecibidos,8,*",
                        "LINE3:escalaIn#00FF00:Segmentos Recibidos"
                        )



    ret = rrdtool.graph( alias+"/datagrama.png",
                        "--start",str(tiempoInicio),
                        "--end","N",
                        "--vertical-label=Bytes/s",
                        "--title=Datagramas entregados a usuarios UDP",
                        "DEF:datEntrega="+alias+"/"+alias+".rrd:datagramasEntrega:AVERAGE",
                        "CDEF:escalaIn=datEntrega,8,*",
                        "LINE3:escalaIn#00FF00:Datagramas Entregados",
                        )
