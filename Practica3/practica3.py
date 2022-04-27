from time import sleep
from trendCPU import actualizarGrafica

while 1:
    if not actualizarGrafica():
        sleep(300)
    else:
        sleep(60)

