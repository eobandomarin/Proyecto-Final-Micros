# -*- coding: cp1252 -*-
#Con el módulo   picamera se visualiza la imagen en tiempo real de la camara. 
#!/usr/bin/python
import time
import picamera
 
with picamera.PiCamera() as picx:
    picx.start_preview()
    time.sleep(60)
    picx.stop_preview()
    picx.close()
