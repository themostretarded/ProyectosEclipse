import sys,pygame
import Image
#from sys import argv
from math import*
import numpy
from time import*
import math

def main():
    pygame.init() # Inicializa pygame
    screen = pygame.display.set_mode((500, 327)) 
    pygame.display.set_caption('Imagenes') 
    imagen = conv()
    img = pygame.image.load(imagen) 
    screen = pygame.display.get_surface() 

    while True: # Ciclo para las acciones en la ventana

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.blit(img, (0,0)) # muestra la posicion de la imagen en x = 0 y y=0
        pygame.display.update()

#Aplicamos la mascara 
#def mascara():
    

def conv():
    tarda = time()
    ima = Image.open("pulmon.jpg")
    imagen = ima.load()
    ancho,alto = ima.size
    mat_x = ([-1,0,1],[-2,0,2],[-1,0,1])
    mat_y = ([1,2,1],[0,0,0],[-1,-2,-1]) 
    for i in range(ancho):
        for j in range(alto):
            sumx=0.0
            sumy = 0.0
            for m in range(len(mat_x[0])):
                for h in range(len(mat_y[0])):
                    try:
                        mul_x= mat_x[m][h] * imagen[i+m, j+h][0]
                        mul_y= mat_y[m][h] * imagen[i+m, j+h][0]
                    except:
                        mul_x=0
                        mul_y=0
                    sumx=mul_x+sumx
                    sumy=mul_y+sumy
            valorx = pow(sumx,2)
            valory = pow(sumy,2)
            grad = int(math.sqrt(valorx + valory))
            if grad <= 0:
                grad = 0
            elif grad >= 255:
                grad = 255
            imagen[i,j] = (grad, grad, grad)
    nueva = 'conv.png'
    otra = ima.save(nueva)
    t1 = time()
    t2 = t1 - tarda
    print "Tiempo que tardo el procesamiento = " +str(t2)+ " segundos"
    return nueva

if __name__ == "__main__":
    main()
