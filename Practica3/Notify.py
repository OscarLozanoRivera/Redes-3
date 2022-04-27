from email.mime.text import MIMEText
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
# Define params
rrdpath = 'BD/'
imgpath = 'IMG/'
fname = 'trend.rrd'

mailsender = "anstudioprueba@gmail.com"
mailreceip = "anstudioprueba@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'prueba2021android'

def send_alert_attached(subject,porcentaje):
    """ Envía un correo electrónico adjuntando la imagen en IMG
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(imgpath+'IMGdeteccion.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    msg.attach(MIMEText("Porcentaj de ocupación del procesador: "+str(porcentaje)+"%"))
    s = smtplib.SMTP(mailserver)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, mailreceip, msg.as_string())
    s.quit()