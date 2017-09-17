from numpy import array, argmax, std, mean, zeros
from mascaras import pideEntero, existe, canal, seleccionaCanal, normaliza
from PIL import Image, ImageDraw



def mayor(valor, umbral):
    return valor > umbral

def menor(valor, umbral):
    return valor < umbral

def minomax():
    opcion = None
    while opcion is None or opcion not in 'co':
        try:
            opcion = raw_input('Claros u oscuros [co]: ')[0].lower()
        except:
            continue
    if opcion == 'o':
        return menor
    elif opcion == 'c':
        return mayor
    

RANGO = 2

def box((x, y), dim, pixels, radio):
    for nx in [x - radio, x + radio]:
        for ny in xrange(y - radio, y + radio + 1):
            if existe((nx, ny), dim):
                pixels[nx, ny] = 255, 0, 0
    for ny in [y - radio, y + radio]:
        for nx in xrange(x - radio, x + radio + 1):
            if existe((nx, ny), dim):
                pixels[nx, ny] = 255, 0, 0
    return

def agujero(datos, x, y, corte, umbral):
    global RANGO
    dim = datos.shape
    for dx in xrange(-RANGO, RANGO + 1):
        nx = x + dx
        for dy in xrange(-RANGO, RANGO + 1):
            ny = y + dy
            if existe((x, y), dim):
                if not corte(datos[x][y], umbral):
                    return False
    return True

def eliminatePlains(data):
    prev = None
    survivors = []
    current = 0
    n = len(data)
    while current < n:
        value = data[current]
        pos = current + 1
        while pos < n:
            if data[pos] == value:
                pos += 1
            else:
                break
        rep = (current + pos) / 2
        survivors.append((rep, value))
        current = pos
    return survivors

def localExtrema(data, cut):
    prev = None 
    extrema = []
    for x in xrange(len(data)):
        (key, this) = data[x]
        next = None
        try:
            (tmp, next) = data[x+1]
        except:
            pass
        p = (prev is None or cut(this, prev))
        n = (next is None or cut(this, next))
        if p and n:
            extrema.append((key, this))
        prev = this
    return extrema

def prune(pairs, cut):
    FACTOR = 0.2
    data = [value for (key, value) in pairs]
    threshold = None
    if max(data) > 2 * min(data):
        threshold = mean(data)
        var = std(data) * FACTOR
        if cut(1, 2):
            threshold -= var
        else: 
            threshold += var
    clean = []
    for (k, d) in pairs:
        if threshold is None or not cut(d, threshold):
            clean.append(k)
    return clean

def norm2grayscale(data, dim):
    (w, h) = dim
    gray = zeros((w, h))
    for x in xrange(w):
        for y in xrange(h):
            gray[x][y] = int(data[x][y] * 255)
    return gray

def agujeros(imagen):
    global RANGO
    dim = imagen.size
    (w, h) = dim
    pixeles = imagen.load()
    (datos, avg, stddev) = normaliza(canal(pixeles, dim, seleccionaCanal()))
    datos = norm2grayscale(datos, dim)
    corte = minomax()
    suma = []
    for x in xrange(w):
        suma.append(int(sum(datos[x, :]) / w))
    columnas = localExtrema(eliminatePlains(suma), corte)
    suma = []
    for y in xrange(h):
        suma.append(int(sum(datos[:, y]) / h))
    filas = localExtrema(eliminatePlains(suma), corte)
    columnas = prune(columnas, corte)
    filas = prune(filas, corte)
    resultado = Image.new('RGB', dim)
    nuevos = resultado.load()
    for x in xrange(w):
        for y in xrange(h):
            nuevos[x, y] = pixeles[x, y]
    draw = ImageDraw.Draw(resultado) 
#    for x in columnas:
#        draw.line((x, 0, x, h-1), fill=(255, 255, 0))
#    for y in filas:
#        draw.line((0, y, w-1, y), fill=(0, 255, 255))
    print 'Examining %d candidate positions.' % (len(columnas) * len(filas))
    umbral = pideEntero('Threshold for qualifying as a hole pixel: ')
    total = 1
    for x in columnas:
        for y in filas:
            if agujero(datos, x, y, corte, umbral):
                total += 1
                box((x, y), dim, nuevos, RANGO * 2)
    print total, 'holes found.'
    return resultado

