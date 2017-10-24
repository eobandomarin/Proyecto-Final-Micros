#Captura video
#!/usr/bin/python

import time
import picamera
 
with picamera.PiCamera() as picx:
	picx.start_preview()
	picx.start_recording('mi_video.h264') #h264 es la extenson del archivo
        picx.wait_recording(20)               #20 son los segundos que graba
        picx.stop_recording()
	picx.stop_preview()
	picx.close()
