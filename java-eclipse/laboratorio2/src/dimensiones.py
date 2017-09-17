import Image
from sys import argv,exit
from math import floor

# Parametros: Nuevas dimensiones
x = int(argv[1])
y = int(argv[2])

"""def procesar(im,w,h,pixeles,pix,scale_i,scale_j):
    salto = 0
    for i in range(w):
        for j in range(h):
            for x in range(scale_i):
                for y in range(scale_j):
                    salto = i*scale_i
                    salto2 = j*scale_j
                    pix[salto+x,salto2+y] = pixeles[i,j]
    return im
"""

def escalar(im,pixeles,pix,scale_i,scale_j,nw,nh):
    for i in range(nw):
        for j in range(nh):
            pix[i,j] = pixeles[int(i/scale_i),int(j/scale_j)]

    return im

def main():
    im = Image.open('miyagi.jpg')
    w,h = im.size
    pixeles = im.load()
    im.show()

    scale_i = (1.0*x)/w
    scale_j = (1.0*y)/h

    nw = int(w*scale_i)
    nh = int(h*scale_j)
    copia = Image.new('RGB',(nw,nh))
    pix = copia.load()
    
    resized = escalar(copia,pixeles,pix,scale_i,scale_j,nw,nh)
    resized.show()

if __name__ == '__main__':
    main()

