#Reescalado de imagenes

#!/usr/bin/python
 
import time
import picamera
 
with picamera.PiCamera() as picam:
    picam.resolution = (2592, 1944)   #Escala original
    picam.start_preview()
    time.sleep(3)
    picam.capture('foto.jpg',resize=(1024,768)) #Nueva escala
    picam.stop_preview()
    picam.close()
