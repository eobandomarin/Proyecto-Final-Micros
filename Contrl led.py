#Control led camara
#!/usr/bin/python
 
import time
import picamera
 
with picamera.PiCamera() as picam:
    picam.led= False                #Se apaga el led
    picam.start_preview()
    time.sleep(3)
    picam.stop_preview()
    picam.close()
