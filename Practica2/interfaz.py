from cgitb import text
import time
import tkinter
from tkinter.font import NORMAL
from tkinter.ttk import Button, Label, Spinbox
from tkinter import DISABLED, E, Text
from tkinter.constants import GROOVE, W, END
from datetime import datetime
from getSNMP import consultaSNMP  
import rrdtool

comunidad="comunidadASR"
ip="192.168.0.112"


def interfaz():

    reporte={
        'version' : '1',
        'dispositivo' : 'Servidor de Correo SMTP',
        'descripcion' : None,
        'fecha' : None,
        'defaultProtocol' : 'radius',
        'comentario1' : "#Direccion-IP",
        '5' : '192.168.0.112',
        'comentario2' : "#Puerto",
        '6' : '2525',
        'comentario3' : "#Nombre-Usuario",
        '7' : None,
        'comentario4' : "#Contacto-Mail",
        '8' : None,
        'comentario5' : "#Tiempo-Reporte",
        '9' : None,
        'comentario6' : "#Segmentos-TCP-Recibidos-Inicio",
        '10' : None,
        'comentario7' : "#Segmentos-TCP-Recibidos-Final",
        '11' : None,
        'comentario8' : "#Segmentos-TCP-Entregados-Inicio",
        '12' : None,
        'comentario9' : "#Segmentos-TCP-Entregados-Final",
        '13' : None,
        'comentario10' : "#Segmentos-TCP-Utilizados",
        '14' : None
    }

    def reiniciarHora():
        horaActual=str(datetime.now().time()).split(":")
        horaAprox=horaActual[0]        
        if int(horaActual[1]) < 5:
                minAprox=str(60+(int(horaActual[1])-5)).format({0})
                if int(horaActual[0]) == 0:
                        horaAprox=str(23)
                else:
                        if int(horaActual[0]) > 9:
                                horaAprox="0"+str(int(horaActual[0])+1)
                        else:
                                horaAprox=str(int(horaActual[0])+1)
        else:
                if int(horaActual[1]) > 5:
                        minAprox=str(int(horaActual[1])-5).format({00})
                else:
                        minAprox=str(int(horaActual[1])-5).format({00})
        horaInicio.delete("0",END)
        minutoInicio.delete("0",END)
        horaFin.delete("0",END)
        minutoFin.delete("0",END)

        horaInicio.insert(END,horaAprox)
        minutoInicio.insert(END,minAprox)
        horaFin.insert(END,horaActual[0])
        minutoFin.insert(END,horaActual[1])

    def generarReporte(tiempo):
        tiempo_actual = int(time.time())
        #Grafica desde el tiempo actual menos diez minutos
        tiempo_inicial = tiempo_actual - tiempo
        reporte['descripcion'] = consultaSNMP(comunidad,ip,'1.3.6.1.2.1.1.1.0')
        reporte['fecha'] = str(datetime.now())
        reporte['7'] = consultaSNMP(comunidad,ip,'1.3.6.1.2.1.1.5.0').split()[2]
        reporte['8'] = str(consultaSNMP(comunidad,ip,'1.3.6.1.2.1.1.4.0')).split()[2]
        reporte['9'] = str(tiempo)+' seg'
        ret = rrdtool.graphv( "segmentos.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Segmentos",
                     "--title=SegmentosEntrada unicas que ha recibido una interfaz",
                     "DEF:segIn=practica2.rrd:segmentosIn:AVERAGE",
                     "DEF:segOut=practica2.rrd:segmentosOut:AVERAGE",
                     "VDEF:segEntradaFIRST=segIn,FIRST",
                     "VDEF:segEntradaLAST=segIn,LAST",
                     "VDEF:segSalidaFIRST=segOut,FIRST",
                     "VDEF:segSalidaLAST=segOut,LAST",
                     "PRINT:segEntradaFIRST:%8.0lf",
                     "PRINT:segEntradaLAST:%8.0lf",
                     "PRINT:segSalidaFIRST:%8.0lf",
                     "PRINT:segSalidaLAST:%8.0lf",
                     )
        reporte['10'] = ret['print[0]']
        reporte['11'] = ret['print[1]']
        reporte['12'] = ret['print[2]']
        reporte['13'] = ret['print[3]']
        reporte['14'] = str(  ( int(ret['print[1]']) - int(ret['print[0]'])) + ( int(ret['print[3]']) - int(ret['print[2]']) ) )
        imprimirReporte()

    def imprimirReporte():
        monitorDatos.config(state=NORMAL)
        monitorDatos.delete("1.0",END)
        for rep in reporte:
            #print(rep+" : "+ reporte[rep])
            if rep[:10] == 'comentario':
                linea= reporte[rep]+"\n"
            else:
                linea= rep+" : "+ reporte[rep]+"\n"
            monitorDatos.insert(END,linea)
        monitorDatos.config(state=DISABLED)
        

    root = tkinter.Tk()         #Se inicia la ventana
    # Icono Aplicación
    ancho_ventana = 520         #Definir medidas de ventana
    alto_ventana = 520
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2  #Definir posición de laventana
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + \
        "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.resizable(False, False)    #La ventana no se puede alargar ni ensanchar

    root.title("Practica 2")      #Título de la ventana

    i=0

    #Definición y posicionamiento de los elementos de la interfaz gráfica

    Label(root, text="Selecciona un periodo de tiempo para generar el reporte").grid(row=0, column=0, columnspan=6,padx=15, pady=15)
    i+=1
    Label(root, text="Hora Inicio:").grid(row=i,column=0, pady=15,sticky=E)
    horaInicio=Spinbox(root,width=2,from_=0,to=23,increment=1)
    horaInicio.grid(row=i,column=1, pady=15,sticky=E)
    minutoInicio=Spinbox(root,width=2,from_=0,to=59,increment=1)
    minutoInicio.grid(row=i,column=2,sticky=W)
    Label(root, text="Hora Fin:").grid(row=i,column=3, pady=15,sticky=E)
    horaFin=Spinbox(root,width=2,from_=0,to=23,increment=1)
    horaFin.grid(row=i,column=4,sticky=E)
    minutoFin=Spinbox(root,width=2,from_=0,to=59,increment=1)
    minutoFin.grid(row=i,column=5,sticky=W)
    i+=1
    Button(root, text="Generar",command=lambda:generarReporte(600)).grid(row=i, column=0, columnspan=3, padx=15, pady=15)
    Button(root, text="Actualizar",command=reiniciarHora).grid(row=i, column=3, columnspan=3,padx=15, pady=15)
    i+=1
    monitorDatos = Text(root, height=20, width=60, relief=GROOVE)
    monitorDatos.grid(row=i, column=0, columnspan=6,sticky=W, padx=15, pady=5)
    reiniciarHora()
    root.mainloop()

if __name__ == "__main__":
    interfaz()


#sysName: 1.3.6.1.2.1.1.5.0
#sysContact: 1.3.6.1.2.1.1.4.0