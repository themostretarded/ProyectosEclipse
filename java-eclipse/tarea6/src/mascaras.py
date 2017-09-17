from numpy import array, zeros, absolute
import Image, ImageDraw
from random import randint, shuffle, random
from math import sqrt, atan2, pi, fabs, log

def selectPixels(pixels, nx, ny, prop):
    (wp, hp) = prop
    xr = int(wp)
    yr = int(hp)
    rc = 0
    gc = 0
    bc = 0
    c = 0
    for dx in [-xr, xr]:
        for dy in [-yr, yr]:
            try:
                r, g, b = pixeles[nx + dx, ny + dy]
            except:
                continue
            m = (fabs(dx) + fabs(dy) + 1)
            c += 1.0 / m
            rc += r / m
            gc += g / m 
            bc += b / m
    if c > 0:
        r = rc / c
        g = gc / c
        b = bc / c
        return int(r), int(g), int(b)
    else:
        return pixels[nx, ny]

def oscuro(valor, umbral):
    return valor < umbral

def claro(valor, umbral):
    return valor > umbral

def promedio(p, x, y, rx = 1, ry = 1):
    c = 0
    rt = 0
    gt = 0
    bt = 0
    for dx in range(-rx, rx + 1):
        for dy in range(-ry, ry + 1):
            try:
                r, g, b = p[x + dx, y + dy]
            except:
                continue
            c += 1
            rt += r
            gt += g
            bt += b
    if c == 0:
        return p[x, y]
    return rt / c, gt / c, bt / c

def reemplazo(p, x, y, uo, uc, rx, ry):
    rp, gp, bp = promedio(p, x, y, rx, ry)
    comp = (rp + gp + bp) / 3.0
    r, g, b = p[x, y]
    valor = (r + g + b) / 3.0
    if (oscuro(valor, uo) and not oscuro(comp, uo)) or \
            (claro(valor, uc) and not claro(comp, uc)):
        return rp, gp, bp
    else:
        return r, g, b

def niveles(p, w, h):
    FRACCION = 4
    min = 255 * 3
    max = 0
    total = 0
    for x in range(w):
        for y in range(h):
            r, g, b = promedio(p, x, y)
            valor = (r + g + b) / 3
            if valor < min:
                min = valor
            if valor > max:
                max = valor
            total += valor
    prom = total / (w * h)
    oscuro = (prom - min) / FRACCION
    claro = max - ((max - prom) / FRACCION)
    return (oscuro, claro)

def eliminarRuidoSalYPimienta(data):
    (w, h) = data.size
    pixeles = data.load()
    resultado = Image.new('RGB', (w, h))
    nuevos = resultado.load()
    (oscuro, claro) = niveles(pixeles, w, h)
    rx = int(log(w)) / 2
    ry = int(log(h)) / 2
    if rx < 1:
        rx = 1
    if ry < 1:
        ry = 1
    for x in range(w):
        for y in range(h):
            nuevos[x, y] = reemplazo(pixeles, x, y, oscuro, claro, rx, ry)
    return resultado

def agregarRuidoSalYPimienta(data):
    prob = float(raw_input('Probabilidad de ruido: '))
    (w, h) = data.size
    pixeles = data.load()
    resultado = Image.new('RGB', (w, h))
    nuevos = resultado.load()
    for x in range(w):
        for y in range(h):
            if random() < prob: # si toca poner ruido
                v = 0 # negro la mitad del tiempo
                if random() < 0.5:
                    v = 255 # blanco la otra mitad
                nuevos[x, y] = v, v, v
            else:
                nuevos[x, y] = pixeles[x, y]
    return resultado

RADIO = 3

def marcador(pixeles, pos, dim, color):
    global RADIO
    (x, y) = pos
    for dx in xrange(-RADIO, RADIO + 1):
        for dy in xrange(-RADIO, RADIO + 1):
            vx = x + dx
            vy = y + dy
            if existe((vx, vy), dim):
                pixeles[vx, vy] = color
    return

def matrix2grayscale(matrix):
    (w, h) = matrix.shape
    resultado = Image.new('RGB', (w, h))
    grises = resultado.load()
    for x in xrange(w):
        for y in xrange(h):
            g = int(matrix[x][y] * 255.0)
            grises[x, y] = g, g, g
    return resultado

def generaColoresAleatorios(cuantos):
    colores = list()
    while len(colores) < cuantos:
        c = [0, 255, randint(1, 25) * 10]
        shuffle(c)
        c = (c[0], c[1], c[2])
        if c not in colores:
            colores.append(c)
    return colores

def existe(pos, dim):
    (x, y) = pos
    (w, h) = dim
    return x >= 0 and x < w and y >= 0 and y < h

def componente(pos, dim, clasificados):
    nuevo = set()
    cola = [pos]
    (w, h) = dim

    xmin = w
    ymin = h
    xmax = 0
    ymax = 0
    
    while len(cola) > 0:
        (x, y) = cola.pop(0)
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if  y > ymax:
            ymax = y
        nuevo.add((x, y))
        clasificados.add((x, y))
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                vecino = (x + dx, y + dy)
                if existe(vecino, dim):
                    if not vecino in clasificados:
                        if not vecino in cola:
                            cola.append(vecino)
    return (nuevo, ((xmin, ymin), (xmax, ymax)))

def objetos(clasificados, dim):
    componentes = list()
    (w, h) = dim
    for x in xrange(w):
        for y in xrange(h):
            pos = (x, y)
            if not pos in clasificados:
                res = componente(pos, dim, clasificados)
                componentes.append(res)
    return componentes

RobertsX = array([[0, 1], [-1, 0]])
RobertsY = array([[1, 0], [0, -1]])
SobelX = array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
SobelY = array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
PrewittX = array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
PrewittY = array([[1, 1, 1], [0, 0, 0], [-1, -1, 1]])
ExOrd = array([[1, 2, 1], [2, 0, 2], [1, 2, 1]])

def rojo(pixel):
    r, g, b = pixel
    return r

def verde(pixel):
    r, g, b = pixel
    return g

def azul(pixel):
    r, g, b = pixel
    return b

def gris(pixel):
    r, g, b = pixel
    return (r + g + b) / 3

def menor(pixel):
    r, g, b = pixel
    return min(r, g, b)

def mayor(pixel):
    r, g, b = pixel
    return max(r, g, b)

opciones = {'r': rojo, 'g': verde, 'b': azul, 'g': gris, 'i': menor, 'a': mayor}

def dominante(matriz, borde = False):
    w, h = matriz.shape
    votos = dict()
    if borde:
        wr = [0, w-1]
        hr = [0, h-1]
    else:
        wr = xrange(w)
        hr = xrange(h)
    for x in wr:
        for y in hr:
            v = matriz[x][y]
            if v in votos:
                votos[v] +=1
            else:
                votos[v] = 1
    return max(votos.iterkeys(), key=(lambda v: votos[v]))

def canal(pixeles, (w, h), seleccion):
    global opciones
    valores = zeros((w, h))
    selector = opciones[seleccion]
    for x in xrange(w):
        for y in xrange(h):
            valores[x][y] = selector(pixeles[x, y])
    return valores

def combine(x, y):
    return sqrt(x**2 + y**2)

def magnitud(X, Y):
    if not X.shape == Y.shape:
        return None # no sirve
    (w, h) = X.shape
    M = zeros((w, h))
    for x in xrange(w):
        for y in xrange(h):
            M[x][y] = combine(X[x][y], Y[x][y])
    return M

def normaliza(M):
    minimum = M.min()
    maximum = M.max()
    scaling = (maximum - minimum) * 1.0
    (w, h) = M.shape
    N = zeros(M.shape)
    for x in xrange(w):
        for y in xrange(h):
            N[x][y] = (M[x][y] - minimum) / scaling
    sum = N.sum()
    ssq = (N*N).sum()
    c = N.size
    return (N, sum / c, sqrt((1.0 / (c - 1)) * (ssq - (1.0 / c) * sum**2)))

def umbral(M, nivel):
    resultado = set()
    (w, h) = M.shape
    for x in xrange(w):
        for y in xrange(h):
            if M[x][y] > nivel:
                resultado.add((x, y))
    return resultado

def convolucion(datos, mascara, fondo):
    (wi, hi) = datos.shape
    (wm, hm) = mascara.shape
    dx = wm / 2
    dy = hm / 2
    resultado = zeros((wi, hi))
    for x in xrange(wi):
        for y in xrange(hi):
            valor = 0.0
            for xm in xrange(wm):
                vx = x + xm - dx
                for ym in xrange(hm):
                    vy = y + ym - dy
                    contribucion = None
                    if vx >= 0 and vx < wi and vy >= 0 and vy < hi:
                        contribucion = datos[vx][vy]
                    else:
                        contribucion = fondo
                    valor += contribucion * mascara[xm][ym]
            resultado[x][y] = valor
    return resultado

from sys import argv

def obtenColor():
    while True:
        hexstr = raw_input('Hexadecimal: #')
        if len(hexstr) == 6:
            try:
                r = int(hexstr[:2], 16)
                g = int(hexstr[2:4], 16)
                b = int(hexstr[4:], 16)
            except:
                continue
            return r, g, b
        

def ampliar(conjunto, dim):
    (w, h) = dim
    agregar = set()
    for (x, y) in conjunto:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                xv = x + dx
                yv = y + dy
                if xv >= 0 and xv < w and yv >= 0 and yv < h:
                    if (xv, yv) not in conjunto:
                        agregar.add((xv, yv))
    return conjunto.union(agregar)

def seleccionaCanal():
    global opciones
    opcion = None
    while True:
        try:
            opcion = raw_input('Canal a utilizar: ')[0]
        except:
            continue
        if opcion in opciones.keys():
            return opcion

def extraord(imagen):
    pixeles = imagen.load()
    datos = canal(pixeles, imagen.size, 'g')
    dom = dominante(datos, False)
    (N, avg, stddev) = normaliza(convolucion(datos, ExOrd, dom))
    return matrix2grayscale(binariza(N))

def gradientes(imagen, borde = True):
    opcion = seleccionaCanal()
    pixeles = imagen.load()
    datos = canal(pixeles, imagen.size, opcion)
    dom = dominante(datos, borde)
    Gx = convolucion(datos, SobelX, dom)
    Gy = convolucion(datos, SobelY, dom)    
    return (Gx, Gy, dom)

def detectaBorde(imagen, G):
    (G, avg, stddev) = normaliza(G)
    nivel = avg + stddev 
    borde = umbral(G, nivel)
    (w, h) = imagen.size
    return borde

def pideEntero(mensaje):
    entero = None
    while entero is None:
        try:
            entero = int(raw_input(mensaje))
        except:
            pass
    return int(fabs(entero))

def angulos(borde, Gx, Gy):
    angs = dict()
    for (x, y) in borde:
        angulo = atan2(Gy[x][y], Gx[x][y])
        angulo += pi
        angulo /= 2.0 * pi
        angulo *= 360.0
        if angulo >= 180.0:
            angulo -= 180.0
        a = int(angulo)
        if a == 180:
            a = 0
        angs[(x, y)] = a
    return angs
            
def frecuencias(pairs):
    freq = dict()
    for key in pairs:
        if key in freq:
            freq[key] += 1
        else:
            freq[key] = 1
    return freq

def lineas(imagen):
    (Gx, Gy, dom) = gradientes(imagen)
    (w, h) = imagen.size
    borde = detectaBorde(imagen, magnitud(Gx, Gy))

    ang = angulos(borde, Gx, Gy)
    valores = frecuencias(ang)        
    mapping = dict()
    procesados = dict()
    while True:
        if len(valores) == 0:
            break
        count = max(valores.values())
        pos = None
        for p in valores:
            if valores[p] == count:
                pos = p
                break
        lp = pos 
        c = 1
        while True:
            anterior = valores[lp]
            lp = (lp - 1) % 180
            if lp not in valores:
                break
            valor = valores[lp]
            if valor > anterior:
                break
            if valor == 0:
                break
            c += 1
        rp = pos 
        while True:
            anterior = valores[rp]
            rp = (rp + 1) % 180
            if not rp in valores:
                break
            valor = valores[rp] 
            if valor > anterior:
                break
            if valor == 0:
                break
            c += 1
        total = 0
        for i in xrange(c):
            p = (lp + i + 1) % 180
            total += valores[p]
            mapping[p] = pos
            del valores[p]
        procesados[pos] = total
    valores = procesados
    rango = pideEntero('Rango de unir picos: ')
    while True:
        nuevo = None
        total = None
        for pos in valores:
            for otro in valores:
                if otro == pos:
                    continue
                if fabs(pos - otro) < rango:
                    p = valores[pos]
                    o = valores[otro]
                    total = p + o
                    nuevo = (pos * p + otro * o) / total
                    eliminar = [pos, otro]
                    break
            if nuevo is not None:
                break
        if nuevo is None:
            break
        else:
            for e in eliminar:
                for m in mapping:
                    if mapping[m] == e:
                        mapping[m] = nuevo
                del valores[e]
            valores[nuevo] = total
    
    umbral = (sum(valores.values()) / len(valores)) / 2
    eliminar = list()
    for pos in valores:
        valor = valores[pos]
        if valor < umbral: # ruido
            eliminar.append(pos)
    for e in eliminar:
        del valores[e]
    colores = generaColoresAleatorios(len(valores))
    for pos in valores:
        valores[pos] = colores.pop()
    resultado = Image.new('RGB', (w, h))
    nuevos = resultado.load()
    for x in xrange(w):
        for y in xrange(h):
            try:
                nuevos[x, y] = valores[mapping[angulos[(x, y)]]]
            except:
                nuevos[x, y] = 0, 0, 0
    return resultado

def separaFondo(componentes):
    maximo = 0
    fondo = None
    for (c, bb) in componentes:
        if len(c) > maximo:
            maximo = len(c)
            fondo = (c, bb)
    componentes.remove(fondo)
    return fondo

def bordes(imagen):

    print('Color para borde: ')
    colorDeBorde = obtenColor()
    print('Color para fondo: ')
    colorDeFondo = obtenColor()

    (Gx, Gy, dom) = gradientes(imagen)
    G = magnitud(Gx, Gy)
    borde = detectaBorde(imagen, G)
    dim = imagen.size
    borde = ampliar(borde, dim)
    componentes = objetos(borde, dim)
    fondo = separaFondo(componentes)
    colores = generaColoresAleatorios(len(componentes))
    resultado = Image.new('RGB', dim)
    nuevos = resultado.load()
    (w, h) = dim
    for x in xrange(w):
        for y in xrange(h):
            if (x, y) in borde:
                if colorDeBorde is not None:
                    nuevos[x, y] = colorDeBorde
            elif (x, y) in fondo:
                if colorDeFondo is not None:
                    nuevos[x, y] = colorDeFondo
            else:
                c = 0
                for (comp, bb) in componentes:
                    if (x, y) in comp:
                        nuevos[x, y] = colores[c]
                        break
                    c += 1
    return resultado

def boundingboxes(imagen):
    dim = imagen.size
    resultado = Image.new('RGB', dim)
    nuevos = resultado.load()
    pixeles = imagen.load()

    (w, h) = dim
    for x in xrange(w):
        for y in xrange(h):
            nuevos[x, y] = pixeles[x, y]
    (Gx, Gy, dom) = gradientes(imagen)
    G = magnitud(Gx, Gy)
    borde = detectaBorde(imagen, G)
    componentes = objetos(borde, dim)
    separaFondo(componentes)

    print('Color para cajas:')
    colorDeCajas = obtenColor()

    print('Color para centros:')
    colorDeCentros = obtenColor()

    draw = ImageDraw.Draw(resultado) 
    for (comp, bb) in componentes:
        draw.rectangle(bb, outline=colorDeCajas)
        cx = (bb[0][0] + bb[1][0]) / 2
        cy = (bb[0][1] + bb[1][1]) / 2
        marcador(nuevos, (cx, cy), dim, colorDeCentros)
    return resultado

def datosDeVecinos(data, (x, y), dim):
    res = list()
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            vecino = (x + dx, y + dy)
            if existe(vecino, dim):
                res.append(data[x + dx][y + dy])
    return res

def mediano(data):
    w, h = data.shape
    med = zeros((w, h))
    for x in xrange(w):
        for y in xrange(h):
            v = sorted(datosDeVecinos(data, (x, y), (w, h)))
            med[x][y] = v[len(v)/2]
    return med

def binariza(M):
    sum = M.sum()
    c = M.size
    avg = sum / (c * 1.0)
    (w, h) = M.shape
    B = zeros(M.shape)
    for x in xrange(w):
        for y in xrange(h):
            if M[x][y] > avg:
                B[x][y] = 1.0
            else:
                B[x][y] = 0.0
    return B

def bw(imagen):
    print 'Binarizando'
    binarizado = binariza(canal(imagen.load(), imagen.size, \
                                    seleccionaCanal()))    
    return matrix2grayscale(binarizado)

def esquinas(imagen):
    imagen = eliminarRuidoSalYPimienta(bw(imagen))
    data = canal(imagen.load(), imagen.size, seleccionaCanal())
    (diff, avg, stddev) = normaliza(absolute(data - mediano(data)))
    resultado = imagen.copy()
    nuevos = resultado.load()
    umbral = stddev

    print('Color para esquinas: ')
    color = obtenColor()

    dim = imagen.size
    (w, h) = dim
    for x in xrange(w):
        for y in xrange(h):
            if diff[x][y] > umbral:
                marcador(nuevos, (x, y), dim, color)
                
    return resultado
    
