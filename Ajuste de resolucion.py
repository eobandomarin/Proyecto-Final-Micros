#Ajuste de resolucion de la camara
#!/usr/bin/python
 
import time
import picamera
 
with picamera.PiCamera() as picam:
    picam.resolution = (2592, 1944)  #Resolucion de la camara, no puede superar la resolucion maxima
    picam.start_preview()
    time.sleep(3)
    picam.capture('foto.jpg')
    picam.stop_preview()
    picam.close()
