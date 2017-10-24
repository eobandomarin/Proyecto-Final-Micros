#Captura fotrografia
	
#!/usr/bin/python
import time
import picamera
 
with picamera.PiCamera() as picx:
    picx.start_preview()
    time.sleep(5)
    picx.capture('mifoto.jpg')
    picx.stop_preview()
    picx.close()
