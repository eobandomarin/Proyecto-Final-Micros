#Otros ajustes
#!/usr/bin/python
 
import time
import picamera
 
with picamera.PiCamera() as picam:
    picam.start_preview()
    picam.brightness= 60
    picam.ISO =100 
    time.sleep(3) 
    picam.image_effect = 'negative'
    picam.shutter_speed= 300000 
    picam.capture('foto.jpg',resize=(1024,768)) 
    picam.stop_preview() 
    picam.close()
