import Image
import math
import sys
from sys import argv 


def otro_gris(imagen_original):
    #escala de grises
    #toma el valor maximo del rgb de cada pixel
    print"estoy en escala"
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
    print"sali del gris"
    return imagen_gris

def esquina(imagen_original):
    
    print"estoy en esquina"

    x, y = imagen_original.size
    prueba = imagen_original.load()
    nueva_imagen = imagen_original.copy()
    print "voy al argv2"
    prueba_nueva = nueva_imagen.load() 
    minimo = int(argv[2])
    print"si pase argv2"
    #x es el ancho
    #y es la altura
    for i in range(x):
        for j in range(y):	
            pix = []
            for q in [-1, 0, 1]:
                for w in [-1, 0, 1]:
                    if 0 <= i+q  < x and 0 <= j+w  < y: 
                        pix.append(prueba[i+q,j+w][1])
            pix.sort()
            mediana= len(pix)/2
            
            if len(pix)%2 == 0:
		med=(pix[mediana]+pix[mediana-1])/2
            else:
		med=pix[mediana]  
            prueba_nueva[i,j] = (med,med,med)
    
    for i in range(x):
       for j in range(y):
           otro= prueba_nueva[i,j][1]-prueba[i,j][1]
           if otro < 0:
               otro = 0
           if otro > 255:
               otro = 255
           if otro > minimo:
               prueba[i,j]= (otro,otro,otro)
           else:
               prueba[i,j]=(0,0,0)
    lista = []

    for i in range(x):
        for j in range(y):
            if imagen_original.getpixel((i,j))!=(0,0,255) and imagen_original.getpixel((i,j))!=(0,0,0):
                lista.append(( imagen_original, (0,0,255)))
                for a in range(-2,3):
                    for b in range(-2,3):
                        if 0 <= i+a  < x and 0 <= j+b  < y:
                            prueba[i+a,j+b] = (0,0,255)
    print "ya voy a salir de esquina"
    imagen_original.save('esquina.png')	
    return imagen_original, lista



#def toma_pix(imagen_original):
 #   x, y = imagen_original.size
  #  prueba2 = imagen_original.load()
  #  nueva_imagen2 = Image.new("RGB", (x,y))
    
   # lista = []
   # for i in range(x):
    #    for j in range(y):
     #       if imagen_original.getpixel((i,j))!=(0,255,0) and imagen_original.getpixel((i,j))!=(0,0,0):
      #          lista.append(imagen_original, (0,255,0))
    #return lista, imagen_


def main():
    """funcion principal
    """
    try:
   	imagen_inicial = sys.argv[1]
    	#print imagen_inicial
    	imagen_original = Image.open("filtro.png")
    	imagen_original = imagen_original.convert('RGB')
    except:
    	return
    imagen_b = otro_gris(imagen_original)
    paraesquina = esquina(imagen_b)
    

if __name__ == "__main__":
    main()