import sys
import Image
from sys import argv
from math import*
import numpy
import time
import math

def main():
    ima,ancho,alto,vecino_n= pixel(argv[1])
    i_filtro = filtros(ima,ancho,alto,vecino_n)
    #screen = pygame.display.set_mode((ancho,alto))
    #pygame.display.set_caption('Imagenes')
    #img = pygame.image.load(i_filtro)
    #screen = pygame.display.get_surface()
    #while True:
    #    for eventos in pygame.event.get():
    #        if eventos.type == pygame.QUIT:
    #            sys.exit(0)
    #    screen.blit(img,(0,0))
    #    pygame.display.update()
    

def filtros(ima,ancho,alto,vecino_n):
    tiempo1 = time.time()
    imagen = ima.load()
    val_1 = [-1,0,1]
    for i in range(ancho):
        for j in range(alto):
            pm = vecinos(i,j,val_1,vecino_n)
            imagen[i,j] = (pm,pm,pm)
    nueva = 'filtro.png'
    i_filtro = ima.save(nueva)
    tiempo2 = time.time()
    print "Tiempo de procesamiento filtro"
    return nueva

#def conv(i_filtro, )

def vecinos(i,j,vec_1,vecino_n):
    pm = 0
    indice = 0
    for x in vec_1:
        for y in vec_1:
            sumav_1 = i+x # sumamos los vecinos
            sumav_2 = j+y # sumamos los vecinos
            try:
                if vecino_n[sumav_1,sumav_2]: #ciclo 
                    pm += vecino_n[sumav_1,sumav_2]
                    indice+=1
            except IndexError:
                pass
    try:
        pm=int(pm/indice)
        return pm
    except ZeroDivisionError:
        return 0

#Escala de grises    
def pixel(ima):
    ima = Image.open(ima)
    nueva = 'nueva.png'
    imagen = ima.load()
    ancho,alto = ima.size
    vecino_n = numpy.empty((ancho, alto))
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = ima.getpixel((i,j))
            pix = (r+g+b)/3
            imagen[i,j] = (pix,pix,pix)
            vecino_n[i,j] = int(pix)
    i_filtro = ima.copy()
    
    imagen = ima.save(nueva)
    return i_filtro,ancho,alto,vecino_n

if __name__ == "__main__":           
    main()
