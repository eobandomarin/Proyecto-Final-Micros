import argparse
import imutils
import cv2
import time
import multiprocessing
import RPi.GPIO as GPIO
import os
import datetime
import fileinput

# ESTABLECIMIENTO DE VARIABLES Y CONFIGURACION INICIAL 
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
##GPIO.add_event_detect(23, GPIO.RISING)

camera_port = 0 
ramp_frames = 30

#ENCENDIDO DE CAMARA
time.sleep(2)
camera = cv2.VideoCapture(camera_port) #Se inicializa el objeto de captura de video indexado al puerto de la camara
grab, frame = camera.read()

if (grab==0):
    time.sleep(10)
    camera = cv2.VideoCapture(camera_port) #Se inicializa el objeto de captura de video indexado al puerto de la camara
grab, frame = camera.read()


#FUNCIONES DEL SISTEMA

#TOMA DE FOTO
def get_image():
    retval, im = camera.read() #Obtener imagen
    return im

#PROCESO DE DETECCION
def motion(d,camera):
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--min-area", type=int, default=900, help ="minimum area size")
    args = vars(ap.parse_args())

    firstFrame = None
    un = 1

    while True:
        
        (grabbed, frame) = camera.read()

        if (un == 1):
            text="Unoccupied"
            d[0] = 'Unoccupied'
        else:
            text = "Occupied"
            d[0] = 'Occupied'

        un = 1

        if not grabbed:
            break
        frame = imutils.resize(frame,width=500)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21,21),0)

        if firstFrame is None:
             firstFrame = gray
             continue

        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta,50,255,cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh,None,iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            if cv2.contourArea(c) < args["min_area"]:
                continue
            (x,y,w,h) = cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            text="Occupied"
            d[0] = 'Occupied'
            un = 0
            


        cv2.putText(frame,"Room Status: {}".format(text),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0.255),1)

        cv2.imshow("Security Feed",frame)
        cv2.imshow("Thresh",thresh)
        cv2.imshow("Frame Delta",frameDelta)

        key= cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


    
#Instanciado de eventos y subprocesos


mgr = multiprocessing.Manager()
d=mgr.dict()
p= multiprocessing.Process(target=motion, args=(d,camera))
p.start()

#_________________MAIN______________________#

while True:
    
    if (GPIO.input(23) == True):
        #Regitstro de hora de llegada y creacion de archivo si no existiese
        
        h_inicial=datetime.datetime.now()
        register= open('%s.%s.%s.txt' %(h_inicial.day,h_inicial.month,h_inicial.year),'a')
        register.write('')
        register.close()

        #Toma de foto
        ramp_frames = 30
        print("Tomando foto...")
        
        for i in xrange(ramp_frames): #Permite obtener mejor calidad en la imagen
            temp = get_image()
        camera_capture = get_image() #Se toma la imagen
        file = "test_image.jpg" #Ruta, nombre y extension
        cv2.imwrite(file, camera_capture) #Se guarda la imagen

        print ("Listo!")

        #Espera a respuesta de usuario
        #Respuesta - Ejecucion
        print("Atendiendo Visitante")
        time.sleep(5)
        #Espera a la salida del visitante
        while True:
            if ('Unoccupied' in d.values()):
                print 'El visitante se ha ido.'
                h_final=datetime.datetime.now()
                break
        
        #Registro de evento
        f= fileinput.input(files=('%s.%s.%s.txt' %(h_inicial.day,h_inicial.month,h_inicial.year)))
        linenumber= fileinput.filelineno() + 1
        for line in f:
            linenumber= fileinput.filelineno() + 1
            
        f.close()



        register= open('%s.%s.%s.txt' %(h_inicial.day,h_inicial.month,h_inicial.year),'a')
        register.write('%s.Llegada: %s || Salida: %s \n' % (str(linenumber),h_inicial,h_final))

        register.close()

##GPIO.add_event_callback(23, my_callback)



