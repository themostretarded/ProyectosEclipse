from PIL import Image
from math import floor
import numpy as np
from sys import argv



def hacer_gris(imagen_original):
    """pone la foto en escala de grises
    toma el valor maximo del rgb de cada pixel
    """
    x, y = imagen_original.size
    imagen_gris = Image.new("RGB", (x,y))
    pixeles = []
    for a in range(y):
        for b in range(x):
            r, g, b = imagen_original.getpixel((b, a))
            rgb = (r, g, b)
                #se elige el valor mas grande
            maximo = max(rgb)
            data = (maximo, maximo, maximo)
            pixeles.append(data)
    imagen_gris.putdata(pixeles)
    imagen_gris.save("imagen_gris.png")
    return imagen_gris


def aumenta_dism(antes, ((ancho, alto))):
	prom_ancho = (x * 1.0)/ancho
	prom_alto = (y * 1.0)/alto
	imagen = np.zeros((alto,ancho,3))
	
	for a in range(alto):
		for b in range(ancho):
			mueve_x = floor(a * prom_alto)
			mueve_y = floor(b * prom_ancho)
			imagen[a,b] = antes[int(mueve_x),int(mueve_y)] 
	return imagen

im = Image.open("miyagi.jpg").convert('RGB')
(x,y) = im.size
print 'Tamano original:', x,y
imagen = np.array(im)	
toma_ancho = int(argv[1])
toma_alto = int(argv[2])
imagen = aumenta_dism(imagen, (toma_ancho,toma_alto))
print "Nuevo tamano: ", toma_ancho,toma_alto
im = Image.fromarray(np.uint8(imagen))	
im.save("redimencionada.png")
#return im



