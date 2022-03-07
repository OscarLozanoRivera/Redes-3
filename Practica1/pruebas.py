#Crear json
"""
import json
data={}
data['agentes']=[]
data['agentes'].append({  
        "alias":"Linux",
        "ip":"localhost",
        "comunidad":"comunidadASR",
        "puerto":"161",
        "versionSNMP":"v1"
})

data['agentes'].append({  
        "alias":"Windows",
        "ip":"192.168.0.16",
        "comunidad":"comunidadASR",
        "puerto":"161",
        "versionSNMP":"v1"
})

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)

for interfaz in range(1,2+1):
    print(interfaz)


palabra="536f667477617265204c6f6f706261636b20496e7465726661636520"

print(bytes.fromhex(palabra).decode("ASCII"))

from datetime import datetime
horaA=str(datetime.now().time()).split(':')
print(horaA) 


dictc={"uno":1}
print('uno' in dictc)
print(1 in dictc)

if 1 in dictc:
    del dictc[1]
else:
    print(dictc)

import json
with open('data.json') as file:    data = json.load(file)

dataAMandar={}
dataAMandar['agentes']=[]

for agente in data['agentes']:
    if agente['alias']=='Linux':
        print("Se va linux")
    else:
        dataAMandar['agentes'].append(agente)        
print(dataAMandar)




from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
w , h=A4
#print(type(dimensiones))
#print(dimensiones[0])
c = canvas.Canvas("HolaMundo.pdf",pagesize=A4)

img = ImageReader("Practica1/logoWindows.png")
imgW,imgH = img.getSize()
c.drawImage(img, 50 , h-50-100, width=104, height=100)
#c.drawString(50,dimensiones[1]-50,"¡Hola Mundo!")



def separarParrafos(palabra, limite):
    lineas=[]
    lineas.append(palabra[:limite])
    for i in range(int(len(palabra)/limite)):
        lineas.append(palabra[limite*(i+1):limite*(i+2)])
    return lineas
enca="Windows, version 10, para estudiantes y alumnos, especialmente los de ESCOM, a ver si no"
lineas=separarParrafos(enca,38)
print(lineas)
encabezados=[]
for i,linea in enumerate(lineas):
    encabezado = c.beginText(170, h-70-(i+1)*25)
    encabezado.setFont("Helvetica",20)
    encabezado.textLine(linea)
    encabezados.append(encabezado)
for encab in encabezados:
    c.drawText(encab)
encabezados=[]



textos={ 
    'numInterfaces' : 44,
    'tiempoAct': 20,
    'comunidad' : "comunidadASR",
    'ip' : "192.168.0.16"
}

lineas=[]
for i,linea in enumerate(textos):
    parrafo=linea + ": " + str(textos[linea])
    lin = c.beginText(50, h-200-(i*25))
    lin.setFont("Helvetica",16)
    lin.textLine(parrafo)
    lineas.append(lin)
for line in lineas:
    c.drawText(line)

c.save()

from datetime import datetime

print(datetime.now().time().hour)
print(datetime.now().time().minute)

import time


print(int(time.time()))
"""
import platform
import subprocess
import time

def myping(host):
    parameter = '-n' if platform.system().lower()=='windows' else '-c'

    while True:
        command = ['ping', parameter, '1', host]
        response = subprocess.call(command)
        time.sleep(1)

myping("192.168.0.14")
