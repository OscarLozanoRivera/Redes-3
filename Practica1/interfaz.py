import os
import shutil
import tkinter as tk
from tkinter import ANCHOR, BOTTOM, DISABLED, SUNKEN, W, Frame, BooleanVar, Entry, Image, StringVar, Tk, PhotoImage, messagebox, Label , Text , END, IntVar,NORMAL
from tkinter.constants import INSERT, TOP
import tkinter.ttk as ttk
from tkinter.ttk import Label, Radiobutton 
from pysnmp.hlapi import *
from consultas.reportePDF import generarPDF
from consultas.createRRD import crearRRD
from consultas.updateRRD import actualizar
from consultas.getSNMP import consultaSNMP
from datetime import datetime  
import json
import threading

NOMBRE="Oscar"
NUMJUGADOR=1
root = Tk()
# Icono Aplicación
ancho_ventana = 1000
alto_ventana = 900
x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
posicion = str(ancho_ventana) + "x" + str(alto_ventana) + \
        "+" + str(x_ventana) + "+" + str(y_ventana)
root.geometry(posicion)
root.resizable(False, False)

root.title("Practica 1  -  "+NOMBRE)

numRow=0
def masRow():
        global numRow
        numRow+=1

def actualizarResumen():
        global lblMonitor

        with open('data.json') as file:
                data = json.load(file)

        monitor='Monitoreando '+str(len(data['agentes']))+' agentes'
        lblMonitor.config(text=monitor)

        resumen=[]
        #Alias
        for i,agente in enumerate(data['agentes']):
                resumen.append([])
                resumen[i].append('Alias:\n')
                resumen[i].append(agente['alias']+'\n')
        #Consulta Estado
        for i,agente in enumerate(data['agentes']):
                resumen[i].append('Estado:\n')
                #print(agente['ip'])
                if(consultaSNMP(agente['comunidad'],agente['ip'],'1.3.6.1.2.1.1.1.0')) == None:
                        resumen[i].append('\tSin conexión\n')
                else:
                        resumen[i].append('\tConectado\n')
        #Consulta Número Interfaces
        for i,agente in enumerate(data['agentes']):
                resumen[i].append('Número de interfaces:\n')
                #print(agente['ip'])
                respuesta=consultaSNMP(agente['comunidad'],agente['ip'],'1.3.6.1.2.1.2.1.0')
                if respuesta == None:
                        resumen[i].append('\t---\n')
                else:
                        resumen[i].append(respuesta.split()[2:])
                        resumen[i].append('\n')
        #resumen.append(consultaSNMP(agente['comunidad'],agente['ip'],'1.3.6.1.2.1.1.1.0').split()[2:])

        #Consulta Estado Administrativo y Descripción de Interfaces
        for i,agente in enumerate(data['agentes']):
                e=0
                if(consultaSNMP(agente['comunidad'],agente['ip'],'1.3.6.1.2.1.1.1.0')) != None:
                        num=int(consultaSNMP(agente['comunidad'],agente['ip'],'1.3.6.1.2.1.2.1.0').split()[2])
                        for interfaz in range(1,num+1):
                                e+=1
                                if e==15:
                                        break
                                resumen[i].append('\nInterfaz '+str(interfaz)+'\n')

                                resumen[i].append('Estado:\n')
                                estado=int(consultaSNMP(agente['comunidad'],agente['ip'],'1.3.6.1.2.1.2.2.1.7.'+str(interfaz)).split()[2])
                                if estado== 1: #Up
                                        resumen[i].append('\tListo para pasar paquetes\n')
                                elif estado==2: #Down
                                        resumen[i].append('\tDesconectado\n')
                                else: #Test
                                        resumen[i].append('\tEn pruebas\n')
                                
                                resumen[i].append('Descripción:\n')
                                descripcion=consultaSNMP(agente['comunidad'],agente['ip'],'1.3.6.1.2.1.2.2.1.2.'+str(interfaz))
                                descripcion=descripcion.split()[2:]
                                paraEnviar=[]
                                for des in descripcion:
                                        if des[:2] == "0x":
                                                des=des[2:]
                                                des=bytes.fromhex(des).decode("ASCII")
                                        paraEnviar.append(des)
                                for des in paraEnviar:
                                        resumen[i].append(des+" ") 
                                resumen[i].append("\n--------------------")
                else:
                        resumen[i].append("\nSin acceso a las interfaces")

        panelAgente1.config(state=NORMAL)
        panelAgente2.config(state=NORMAL)
        panelAgente1.delete("1.0",END)
        panelAgente2.delete("1.0",END)
        if len(resumen) > 0 :
                for lineas in resumen[0]:
                        panelAgente1.insert(END,lineas)
        if len(resumen) > 1 :
                for lineas in resumen[1]:
                        panelAgente2.insert(END,lineas)
        panelAgente1.config(state=DISABLED)
        panelAgente2.config(state=DISABLED)


# Frame Principal
Frame1 = Frame(root).grid(sticky="nesw")

# Indicaciones
Label(Frame1, text="Resumen:").grid(row=numRow, column=0, sticky="nesw", padx=30,pady=10)
masRow()
lblMonitor=Label(Frame1)
lblMonitor.grid(row=numRow, column=0, sticky="nesw", padx=30,pady=10)
masRow()

# Panel Agente 1
panelAgente1 = tk.Text(Frame1, relief="groove",width=45)
panelAgente1.grid(row=numRow, column=0, columnspan=3, sticky="ew" , padx=25, pady=30)

#texto=consultaSNMP('comunidadASR','localhost','1.3.6.1.2.1.1.1.0')
#print(texto.split()[2:])
#texto=consultaSNMP('comunidadASR','192.168.0.16','1.3.6.1.2.1.1.1.0')
#print(texto.split()[2:])

# Panel Agente 2
panelAgente2 = tk.Text(Frame1, relief="groove",width=45)
panelAgente2.grid(row=numRow, column=4, columnspan=3, sticky="ew" , padx=25, pady=30)

actualizarResumen()

masRow()
#Radiobutton Agregar
opcion = IntVar()
opcion.set(None)
radiosEliminar=[]
radiosReporte=[]

def mostarFrame():
        global opcion
        global FrameAgregar
        global FrameEliminar
        global FrameReporte
        global agenteEli
        global agente
        global radiosEliminar
        global radiosReporte
        global btnFinal
        global btnActualizar
        btnFinal.grid_remove()
        btnActualizar.grid_remove()

        with open('data.json') as file:
                data = json.load(file)
        if opcion.get()==0:     #Agregar
                FrameEliminar.grid_remove()
                FrameReporte.grid_remove()
                FrameAgregar.grid(sticky="nesw", pady=30)
        elif opcion.get()==1:   #Eliminar
                FrameEliminar.grid(sticky="nesw", pady=30)
                for radio in radiosEliminar:
                        radio.grid_remove()
                for i,nombre in enumerate(data['agentes']):
                        rbtn=Radiobutton(FrameEliminar, text=nombre['alias'], variable=agenteEli, value=nombre['alias'])
                        rbtn.grid(row=numRow+i,column=0, padx=30)
                        radiosEliminar.append(rbtn)
                btnEliminar.grid(row=numRow+i+1, column=0,padx=30  ,pady=30)
                FrameReporte.grid_remove()
                FrameAgregar.grid_remove()
        else:                   #Reporte
                FrameEliminar.grid_remove()
                FrameReporte.grid(sticky="nesw", pady=30)
                for radio in radiosReporte:
                        radio.grid_remove()
                for i,nombre in enumerate(data['agentes']):
                        rbtn=Radiobutton(FrameReporte, text=nombre['alias'], variable=agente, value=nombre['alias'])
                        rbtn.grid(row=numRow+i,column=0, padx=30)
                        radiosReporte.append(rbtn)
                Label(FrameReporte,text="Hora:Minuto   Inicio").grid(row=numRow+3,padx=20, pady=20)
                horaInicio.grid(row=numRow+3, column=1, columnspan=2,sticky="e")
                minutoInicio.grid(row=numRow+3, column=3, columnspan=2,sticky="w")
                Label(FrameReporte,text="Hora:Minuto   Fin").grid(row=numRow+4)
                horaFin.grid(row=numRow+4, column=1, columnspan=2,sticky="e")
                minutoFin.grid(row=numRow+4, column=3, columnspan=2,sticky="w")
                reiniciarHora()
                btnReporte.grid(row=numRow+5, column=0,padx=30  ,pady=30)
                btnReiniciar.grid(row=numRow+5, column=1,columnspan=2,pady=30)
                FrameAgregar.grid_remove()
        btnFinal.grid(row=numRow+1,column=3,columnspan=2)
        btnActualizar.grid(row=numRow+1,column=0,columnspan=2)

Radiobutton(root, text="Agregar Agente", variable=opcion, value=0,
                    command=mostarFrame).grid(row=numRow, columnspan=2,column=0, padx=30)
btnAgregar= tk.Button(Frame1,relief="groove",text="Agregar agente")        
#btnAgregar.grid(row=2, columnspan=2,column=0, padx=30)

#btn Eliminar
Radiobutton(root, text="Eliminar Agente", variable=opcion, value=1,
                    command=mostarFrame).grid(row=numRow, columnspan=2,column=2, padx=30)
btnEliminar= tk.Button(Frame1,relief="groove",text="Eliminar agente")        
#btnEliminar.grid(row=2, columnspan=2,column=2, padx=30)
#btn Reporte
Radiobutton(root, text="Generar Reporte", variable=opcion, value=2,
                    command=mostarFrame).grid(row=numRow, columnspan=2,column=4, padx=30)
btnReporte= tk.Button(Frame1,relief="groove",text="Generar reporte")        
#btnReporte.grid(row=2, columnspan=2,column=4, padx=30)

masRow()

def agregarAgente():
	if aliasAgente.get() == "" or ipAgente.get() == "" or comunidadAgente.get() == "" or versionAgente.get() == "":
		messagebox.showerror(message="Se necesita la información completa",title="Error al tratar de Agregar Agente")
		return
	with open('data.json') as file:
		data = json.load(file)
	data['agentes'].append({  
        "alias":aliasAgente.get(),
        "ip":ipAgente.get(),
        "comunidad":comunidadAgente.get(),
        "puerto":"161",
        "versionSNMP":versionAgente.get()
    })
	with open('data.json', 'w') as file:
		json.dump(data, file, indent=4)
	actualizarResumen()
	crearRRD(aliasAgente.get())
	

        

#Frame Agregar
FrameAgregar = Frame(Frame1,padx=10)

tk.Label(FrameAgregar,text="Alias:").grid(row=numRow, column=0, sticky="ew" ,  pady=10)
aliasAgente=Entry(FrameAgregar,width=15)
aliasAgente.grid(row=numRow, column=2,columnspan=3,sticky="ew",pady=5)

tk.Label(FrameAgregar,text="IP Agente:").grid(row=numRow+1, column=0, sticky="ew" ,  pady=10)
ipAgente=Entry(FrameAgregar,width=15)
ipAgente.grid(row=numRow+1, column=2,columnspan=3,sticky="ew",pady=5)

tk.Label(FrameAgregar, text="Comunidad:").grid(row=numRow+2, column=0, sticky="ew" , pady=10)
comunidadAgente=Entry(FrameAgregar,width=15)
comunidadAgente.grid(row=numRow+2, column=2,columnspan=3,sticky="ew" ,pady=5)

tk.Label(FrameAgregar, text="Version SNMP:").grid(row=numRow+3, column=0, sticky="ew" ,  pady=10)
versionAgente=Entry(FrameAgregar,width=3)
versionAgente.grid(row=numRow+3, column=2,columnspan=3,sticky="ew" ,pady=5)

btnAgregar= tk.Button(FrameAgregar,relief="groove",text="Agregar")        
btnAgregar.grid(row=numRow+4, column=0, pady=10)
btnAgregar.config(command=agregarAgente)



def eliminarAgente():
	global agenteEli
	with open('data.json') as file:
		data = json.load(file)
	if agenteEli.get() == "":
		messagebox.showerror(message="Selecciona un Agente",title="Error al tratar de Eliminar Agente")
		return
	dataAMandar={}
	dataAMandar['agentes']=[]
	for agente in data['agentes']:
		if agente['alias']!=agenteEli.get():
			dataAMandar['agentes'].append(agente)        
	with open('data.json', 'w') as file:
		json.dump(dataAMandar, file, indent=4)
	mostarFrame()
	actualizarResumen()
	try:
		shutil.rmtree(agenteEli.get())
	except OSError as e: 
		#print(f"Error:{e.strerror}")
                print(" ")
	


#Frame Eliminar
FrameEliminar = Frame(root)
agenteEli= StringVar()
btnEliminar= tk.Button(FrameEliminar,relief="groove",text="Eliminar")        
btnEliminar.config(command=eliminarAgente)



def generarReporte():
    global agente
    if agente.get() == "":
            messagebox.showerror(message="Selecciona un Agente a Supervisar "
							,title="Error al tratar de Generar Reporte")
            return
    with open('data.json') as file:
        data = json.load(file)
    nombre=agente.get()
    for a in data['agentes']:
        if a['alias']==nombre:
            ag=a
            break
    crearRRD(a['alias'])
    tiempos=[[int(horaInicio.get()),int(minutoInicio.get())],[int(horaFin.get()),int(minutoFin.get())]]
    t1 = threading.Thread(name='Actualizando '+a['alias'], target=actualizar,args=(a,tiempos))
    t1.start()
    consulta=consultaSNMP(ag['comunidad'],ag['ip'],'1.3.6.1.2.1.1.1.0').split()[2:]
    encabezado=""
    for palabra in consulta:
        encabezado=encabezado+" "+palabra   
    lista={
        'numInterfaces' : int(consultaSNMP(ag['comunidad'],ag['ip'],'1.3.6.1.2.1.2.1.0').split()[2]),  #numInterfaces
        'tiempoAct': consultaSNMP(ag['comunidad'],ag['ip'],'1.3.6.1.2.1.1.3.0').split()[2],  #tiempoActividad
        'comunidad' : ag['comunidad'], #comunidad
        'ip' : ag['ip']               #ip
    }
    
    t2 = threading.Thread(name='Generando '+a['alias'], target=generarPDF,args=([nombre,encabezado,lista],tiempos[1]))
    t2.start()

        

#Frame Reporte
FrameReporte = Frame(root)
agente= StringVar()

def reiniciarHora():
        horaActual=str(datetime.now().time()).split(":")
        horaAprox=horaActual[0]        
        if int(horaActual[1]) > 54:
                minAprox="0"+str(-60+int(horaActual[1])+5)
                if int(horaActual[0]) == 23:
                        horaAprox=str(0).format({00})
                else:
                        if int(horaActual[0])< 9:
                                horaAprox="0"+str(int(horaActual[0])+1)
                        else:
                                horaAprox=str(int(horaActual[0])+1)
        else:
                if int(horaActual[1]) < 5:
                        minAprox="0"+str(int(horaActual[1])+5)
                else:
                        minAprox=str(int(horaActual[1])+5)
        horaInicio.delete("0",END)
        minutoInicio.delete("0",END)
        horaFin.delete("0",END)
        minutoFin.delete("0",END)

        horaInicio.insert(END,horaActual[0])
        minutoInicio.insert(END,horaActual[1])
        horaFin.insert(END,horaAprox)
        minutoFin.insert(END,minAprox)

horaInicio=ttk.Spinbox(FrameReporte,width=2,from_=0,to=23,increment=1)
minutoInicio=ttk.Spinbox(FrameReporte,width=2,from_=0,to=59,increment=1)

horaFin=ttk.Spinbox(FrameReporte,width=2,from_=0,to=23,increment=1)
minutoFin=ttk.Spinbox(FrameReporte,width=2,from_=0,to=59,increment=1)



btnReporte= tk.Button(FrameReporte,relief="groove",text="Generar")        
btnReporte.config(command=generarReporte)

btnReiniciar= tk.Button(FrameReporte,relief="groove",text="Reiniciar Hora")        
btnReiniciar.config(command=reiniciarHora)

masRow()
#statusbar

btnActualizar= tk.Button(root,relief="groove",text="Actualizar Monitoreo")
btnActualizar.grid(row=numRow,column=0,columnspan=2,pady=15)
btnActualizar.config(command=actualizarResumen)
btnFinal= tk.Button(root,relief="groove",text="Terminar Monitoreo")
btnFinal.grid(row=numRow,column=3,columnspan=2,pady=15)
btnFinal.config(command=root.destroy)

root.mainloop()
