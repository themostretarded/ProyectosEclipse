import Image #esto para trabajar con imagenes
import sys
import pygame
from math import pi, atan, sqrt, sin, cos, fabs
from time import *
import random
import ImageDraw
import math

#definimos

minimo = 127
maximo = 200

#cargamos y abrimos imagen
def imagen():
    img = Image.open("crucigrama.jpg")
    img2= Image.open("crucigrama.jpg")
    ancho,alto = img.size
    img = eg(img,ancho,alto,img2)
    return img, ancho, alto
    
def eg(img,ancho,alto,img2):
    pixeles = img.load()
    imageng = 'nueva.png'
    for i in range (ancho):
        for j in range(alto):
            (r,g,b)= img.getpixel((i,j))
            prom = int((r+g+b)/3)
            #Aqui agregamos umbrales
            pixeles[i,j] = (prom,prom,prom)
    img.save(imageng)
    filtro(img,ancho,alto)
    binarizacion(img2,ancho,alto)
    gx,gy=conv(img2,ancho,alto)
    #binarizacion(img2,ancho,alto)
    lineas(img2,ancho,alto,gx,gy)
    #ruido(img2,ancho,alto)
    #byeruido(img2,ancho,alto)
    #formas(img,ancho,alto)
    #convex(img,ancho,alto)
    return imageng

def filtro(img,ancho,alto):
    tiemp= time()
    pixel =img.load() 
    for i in range (ancho):
        for j in range(alto):
            c = 0
            prom = 0.0
            try:
                if(pixel[i+1,j]):
                    prom += pixel[i+1,j][0]
                    c +=1
            except:
                prom += 0
            try:
                if(pixel[i-1,j]):
                    prom += pixel[i-1,j][0]
                    c +=1
            except:
                prom += 0
            try:
                if(pixel[i,j+1]):
                    prom += pixel[i,j+1][0]
                    c+=1
            except:
                prom += 0
            try:
                if(pixel[i,j-1]):
                    prom += pixel[i,j-1][0]
                    c+=1
            except:
                prom += 0
            
            promt = int(prom/c)
            pixel[i,j] = (promt, promt, promt)
    im=img.save ('filtro.jpg')
    timei=time()
    timef= timei - tiemp
    print "Tiempo de ejecucion del filtro: "+str(timef)+"segundos"

def binarizacion(img2,ancho,alto):
    z= random.randint(0,100)
    pixel=img2.load()
    for i in range (ancho):
        for j in range(alto):
            (r,g,b)=img2.getpixel((i,j))
            prom = (r+g+b)/3
            if (prom > z):
                pixel[i,j]= (255,255,255)
            if(prom<z):
                pixel[i,j] = (0,0,0)
            #if(prom<130):
                #pixel[i,j]=(0,0,0)
            #else:
                #pixel[i,j]=(255,255,255)
    img2.save('binarizadat.jpg')

def conv(img2,ancho,alto):
    tiemp = time()
    pixels =img2.load()
    angulos = []
    gy = []
    gx = []
    matrizX =([-1,0,1],[-2,0,2],[-1,0,1])
    matrizY =([1,2,1],[0,0,0],[-1,-2,-1])
    
    for i in range(alto):
        gx.append([])
        gy.append([])
        for j in range(ancho):
            sumx = 0
            sumy = 0
            a=3
            for x in range(a):
                for y in range(a):
                    try:
                        sumx +=(pixels[j+y-1,i+x-1][0]*matrizX[x][y])
                        sumy +=(pixels[j+y-1,i+x-1][0]*matrizY[x][y])
                    except:
                        pass
            gx[i].append(sumx)
            gy[i].append(sumy)
    grad = math.sqrt(pow(sumx,2)+pow(sumy,2))
    grad = int(grad)
    pixels[j,i] = (grad,grad,grad)
    im= img2.save('conv.jpg')
    timei=time()
    timef= timei - tiemp
    print "Tiempo de ejecucion deteccion de bordes: "+str(timef)+"segundos"
    return gx, gy

def lineas(img2,ancho,alto,gx,gy):
    pixels=img2.load()
    cero = 0.0001
    angulos = []
    rho = 0.0
    rhos = []
    print len(gx)
    print alto
    for x in range(alto):
        rhos.append([])
        angulos.append([])
        for y in range(ancho):
            hor = gx[x][y]
            ver = gy[x][y]
            if fabs(hor) > 0:
                angulo = atan(ver/hor) #calculamos angulo 
            else:
                if fabs(ver)+fabs(hor)< cero:
                    angulo = None
                else:
                    angulo = pi
            if angulo is not None:
                rho =( ( (y-ancho/2)*cos(angulo) )+((ancho/2 -x)*sin(angulo)) )
                #rho 
                #rho = (y - ancho/2)*cos(angulo)+(x -alto/2)*sin(angulo)
                angulos[x].append(int(angulo))
                rhos[x].append(rho)
            else:
                angulos[x].append(None)
                rhos[x].append(None)

    hola=dict()
    for i in range(alto):
        for j in range(ancho):
            try:
                if pixels[i,j][0]==255:
                    dato = (int(rho[x][y]),(angulo[x][y]))
                    if dato in hola:
                        hola[dato]+=1
                    else:
                        hola[dato] =1
            except:
                pass

    for i in range(alto):
        for j in range(ancho):
            if i>0 and j>0 and i<alto-1 and j<ancho-1:
                try:
                    #print "si paso aki la llama"
                    if pixels[j,i][1] ==255:
                        if rhos[i][j] != None:
                           # if rhos[i][j] == 0.75:
                            pixels[j,i] = (255,0,0)
                            print 'ola ke ase'
                        else:
                            print 'no ase'
                except:
                    pass
    img2.save('lineas2.jpg')

def main ():
    pygame.init()
    #pygame.display.set_caption("Ventana")
    r,ancho,alto = imagen()
    screen = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("Ventana")
    im = pygame.image.load(r)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        screen.blit(im,(0,0))
        pygame.display.update()
    return 0

main()
