import imp
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from datetime import datetime

def generarPDF(ag,tiempo):
    while 1:
        if datetime.now().time().hour == tiempo[0] and datetime.now().time().minute == tiempo[1]:
                break
        else:
            #print("Esperando para PDF")
            time.sleep(20)
    print("Generando PDF")
    alias=ag[0]
    enca=ag[1]
    lista=ag[2]
    def separarParrafos(palabra, limite):
        lineas=[]
        lineas.append(palabra[:limite])
        for i in range(int(len(palabra)/limite)):
            lineas.append(palabra[limite*(i+1):limite*(i+2)])
        return lineas

    w , h = A4
    c = canvas.Canvas(alias+"/"+alias+".pdf",pagesize=A4)
    if alias=='Linux':
        img = ImageReader("logoUbuntu.png")
    else:
        img = ImageReader("logoWindows.png")
    c.drawImage(img, 50 , h-50-100, width=104, height=100)

    lineas=separarParrafos(enca,38)
    #print(lineas)
    encabezados=[]
    for i,linea in enumerate(lineas):
        encabezado = c.beginText(170, h-70-(i+1)*25)
        encabezado.setFont("Helvetica",20)
        encabezado.textLine(linea)
        encabezados.append(encabezado)
    for encab in encabezados:
        c.drawText(encab)
    encabezados=[]

    lineas=[]
    for i,linea in enumerate(lista):
        parrafo=linea + ": " + str(lista[linea])
        lin = c.beginText(50, h-200-(i*25))
        lin.setFont("Helvetica",16)
        lin.textLine(parrafo)
        lineas.append(lin)
    for line in lineas:
        c.drawText(line)

    #nombres=['datagrama','unicast','paquetes','segmentos','mensajes']
    ancho= 248.5
    alto= 84

    c.drawImage(alias+"/"+'datagrama'+".png", 50 , h-250- (alto) -50, width = ancho, height = alto)
    c.drawImage(alias+"/"+'unicast'+".png"  , 50 , h-250-(alto*2)-50, width = ancho, height = alto)
    c.drawImage(alias+"/"+'paquetes'+".png" , 50 , h-250-(alto*3)-50, width = ancho, height = alto)
    c.drawImage(alias+"/"+'segmentos'+".png", 50 , h-250-(alto*4)-50, width = ancho, height = alto)
    c.drawImage(alias+"/"+'mensajes'+".png" , 50 , h-250-(alto*5)-50, width = ancho, height = alto)
    c.save()
    #print("Generado")