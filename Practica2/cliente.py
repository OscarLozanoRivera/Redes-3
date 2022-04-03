import smtplib
import email.utils
from email.mime.text import MIMEText
from grpc import server

def enviarMensaje(direccion,mensaje,correoEmisor,correoDestino):
    pass

#Creando el mensaje
msg=MIMEText("Este es el cuerpo del mensaje")
msg['Subject'] = 'Mensaje de texto simple'

server =smtplib.SMTP('192.168.0.112',2525)
try:
    server.sendmail('author@example.com',
                    ['recipient@example.com'],
                    msg.as_string())
finally:
    server.quit()



