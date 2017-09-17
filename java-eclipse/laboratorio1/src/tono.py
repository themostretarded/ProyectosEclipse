import sys,pygame 
import Image 
from sys import argv 
import numpy

def main():
    image= tono(argv[1])
 
def tono(image):
    imagen = Image.open(image)
    new_image = 'tono.png'
    pixels = imagen.load()
    #umbral = 0.8
    opcion = raw_input()
    ancho,alto = imagen.size
    #matriz = numpy.empty((ancho, alto))
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = pixels[i,j]
	#selecciona r, g o b para cambiar el tono
            if(opcion == "r"):
		pixels[i,j] = (r,0,0)
	    if(opcion == "g"):
		pixels[i,j] = (0,g,0)
	    if(opcion == "b"):
		pixels[i,j]=(0,0,b)

	
	    
            #pixels[i,j] = (,escala,escala)
            #matriz[i,j] = int(escala)
    #image_filtro = image.copy()

    imagen.save(new_image)
    imagen.show()
    return ancho,alto
           
main()

