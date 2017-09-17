import pygame, sys, os # Importe pygame para la creacion de la ventana
from PIL import Image #Importar para trabajar con modulo Image de (PIL)
from sys import argv # Importe para tabajar con argumentos
import math
import random
 
#Convierte la imagen en escala de grises
def escala_g():
    ima = argv[1]
    im = Image.open(ima)
    imagen=im.load()
    ancho, alto = im.size
    for i in range(ancho):
        for j in range(alto):
            (r,g,b)= im.getpixel((i,j))
            pix = (r + g + b)/3
            imagen[i,j]=(pix, pix, pix)
    nueva= 'nueva.png'
    im.save(nueva)
 
#aplicarumbral
def umb():
    ima2 = argv[1]
    im = Image.open(ima2)
    imagen2 = im.load()
    ancho, alto = im.size
    minim = random.randint(0,100)
    maxim = random.randint(101,255)
    print "Valor minimo: "+str(minim)
    print "Valor maximo: "+str(maxim) 
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = im.getpixel((i,j))
            bn= (r+g+b)/3
            if (bn < minim):
                bn = 0
                if (bn > maxim):
                    bn=255
            imagen2[i,j] = (bn, bn, bn)
    nueva = 'otra.png'
    im.save(nueva)

#def agujero():
  
def main():
 
    
    imagen = escala_g() # La imagen toma los nuevos valores
    imagen_umbral = umb()
     
if __name__ == "__main__":
    main()
