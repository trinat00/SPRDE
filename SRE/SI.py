from __future__ import absolute_import, division, print_function, unicode_literals
###
import cv2
import numpy as np
import tensorflow as tf
from tensorflow  import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
###
from multiprocessing.sharedctypes import Value
from PIL import ImageChops #Importar partes de librería PIL
import PIL.Image
###
import tkinter
from tkinter import *
from tkinter import filedialog
###


raiz=Tk()
raiz.title("Sistema para la revisión de exámenes")


def abrirArchivo():
    archivo = filedialog.askopenfilename(title="abrir", initialdir="C:/", filetypes=(("Archivos JPG", "*.jpg"),("Archivos PNG", "*.png"),("Archivos JPEG", "*.jpeg"),("Todos los archivos", "*.*")))
    print(archivo)
    im = PIL.Image.open(archivo) #Abriendo imagen escaneada de hoja de respuestas
    im = im.resize((2481,3506)) #Redimencionamiento de imagen para evitar errores
    imv = ImageChops.invert(im) #Invercion de colores de la imagen

    t, b, l, r, x, x2 = (475, 550, 567, 2138, 0, 0) #Coordenadas iniciales y X para nombre de img. de cortes horizontales
    l2, t2, r2, b2, y, reboot = (0, 0, 75, 75, 100, 0) #Coordenadas iniciales y X2 para nombre de img. de cortes verticales

    ##### Corte Horizontal #####
    for i in range(10): #Para i en un rango de 10 realiza:
        im1 = imv.crop((l, t, r, b)) #Corte de imagen invertida y guardada en variable im1
        #im1.show() #Mostrar im1 en pantalla
        t = t + 262 #Suma de coordenadas para corte superior
        b = b + 262 #Suma de coordenadas para corte inferior
        x = x +1 #Suma de valor x para asignación de nombre .jpeg
        im1.save(str(x)+".jpeg") #Guardado de imagen cambiando nombre con variable x

        ##### Corte Vertical #####
    for s in range(10): #Ciclo para pasar por las 10 imágenes recortadas de rangos de 5 recuadros (imagen 1x5)
        x2 = x2 + 1 #Variable que cambia el nombre de la imagen
        for u in range(5): #Ciclo para pasar por cada recuadro de la imagen 1x5
            if reboot == 5: #Cuando la variable llega a 5 se reinician los puntos de recorte
                l2, t2, r2, b2 = (0, 0, 75, 75) #Puntos de recorte
                reboot = 0 #Variable de reinicio
            imh = PIL.Image.open(str(x2)+".jpeg") #Se abre la imagen de los cortes horizontales
            im2 = imh.crop((l2, t2, r2, b2))  #Se genera el corte y se guarda en la variable im2
            #im2.show() #Se muestra el corte
            l2 = l2 + 375 #Suma de píxeles para ir cambiando de recuadro en recuadro
            r2 = r2 + 375 #Suma de píxeles para ir cambiando de recuadro en recuadro
            y = y + 1 # Se genera la suma para cambiar el nombre de la imagen guardada, imagen de recuadro recortado
            reboot = reboot + 1 #Se suma una vuelta al ciclo para el reinicio y posterior cambio de imagen 1x5
            im2.save("RL/"+str(y)+".jpeg") # Se guarda el recorte de la imagen de un recuadro de un solo número (imagen 1x1)
            #print("Recorte num: ",y, " de imagen h num: ",x,", r2 es: ",r2, " y l2 es: ",l2)

    ### ESPECIFICACIONES ###
    # La imagen debe ser escaneada, no una foto pasada por una aplicación de "escaneo"
    # Se recomienda una calidad de 200 PPP (Píxeles por pulgada)
    # Para mejores resultados se recomienda:
    # - Escribir los números grandes centrados y dentro del recuadro
    # - Números legibles
    # - Números obscuros para facilitar el reconocimiento al sistema


    NDP = int(input("¿Cuántas preguntas tendrá? ")) # NDP = Número de preguntas

    PCRC ={} # PCRC = Preguntas con respuestas correctas
    for n in range(1,NDP+1):
        PCRC[n] = int(input("Respuesta a pregunta número {}: ".format(n)))

    print(PCRC)

    NRR = 100
    RERNAO = []

    tf.keras.backend.clear_session()  # Para restablecer fácilmente el estado del portátil.

    model = keras.models.load_model('modelo_entrenado.h5')
    for i2 in range(NDP):
        NRR = NRR + 1
        img = cv2.imread("RL/"+str(NRR)+".jpeg")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (28,28),interpolation = cv2.INTER_AREA)
        resized.shape
        newimg = tf.keras.utils.normalize (resized, axis = 1)
        IMG_SIZE=28
        newimg = np.array(newimg).reshape(-1, IMG_SIZE, IMG_SIZE,1)
        newimg.shape
        predictions = model.predict(newimg)
        # print (np.argmax(predictions))  #Resultado de RNA x1
        RERNAO.append(np.argmax(predictions))
    print("\nRespuestas procesadas en RNA:",RERNAO,"\n")
    

    TRC,TRIC,TDE = (0,0,0)
    for i in range(1,NDP+1):

        if RERNAO[i-1] == PCRC.get(i):
            print('Respuesta {} correcta'.format(i))
            TRC = TRC + 1
        else:
            print('Respuesta {} incorrecta'.format(i))
            TRIC = TRIC + 1
            imri = PIL.Image.open("RL/"+str(i+100)+".jpeg")
            imri.show()


    TDE = 100*TRC/NDP
    print("\nRespuestas correctas: ",TRC)
    print("Respuestas incorrectas: ",TRIC)
    print("\nCalificación: ",TDE,"%")
    
Button(raiz, text="Abrir Archivo",command=abrirArchivo).grid(row=1,column=1, sticky=W+E)
Label(raiz, text=("Al seleccionar la imagen, continúe el proceso en la terminal")).grid(row=2,column=1, sticky=W+E)

raiz.mainloop()