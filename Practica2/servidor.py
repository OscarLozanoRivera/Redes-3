import smtpd
import asyncore

class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self,peer,mailfrom,rcpttos,data,mail_options=None,rcpt_options=None):
        print('Recibiendo mensaje de:',peer)
        print('Mensaje enviado por:  ',mailfrom)
        print('Mensaje enviado a:    ',rcpttos)
        print('Tamaño del mensaje:   ',len(data))

    def listen(self, num: int) -> None:
        print("El servidor SMTP está listo para recibir mensajes")
        return super().listen(num)
        

server = CustomSMTPServer(('192.168.0.112',2525),None)
#server = smtpd.DebuggingServer(('192.168.0.112',2525),None)

asyncore.loop()

print("Servidor escuchando:")