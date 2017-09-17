import Image, ImageDraw
from mascaras import gradientes, detectaBorde, existe, \
    magnitud, pideEntero, ampliar
from random import choice
from math import fabs, sqrt

image=Image.open('filtro.png')

def midpoint(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    x = (x1 + x2) / 2.0
    y = (y1 + y2) / 2.0
    return (x, y)

def crossing(l1, l2):
    global ZERO
    (a1, b1) = l1
    (a2, b2) = l2
    if fabs(a1 - a2) > ZERO:
        x = (b2 - b1) / (1.0 * (a1 - a2))
    else:
        return None
    y = a1 * x + b1
    return (x, y)

UMBRAL = 0.2

def parallel(l1, l2):
    (a1, b1) = l1
    (a2, b2) = l2
    return fabs(a1 - a2) < UMBRAL

def line(A, B):
    global ZERO
    (x1, y1) = A
    (x2, y2) = B
    if fabs(x2 - x1) < ZERO:
        return None
    a = (y2 - y1) / ((x2 - x1) * 1.0)
    b = y1 - a * x1
    return (a, b)

def offset((x, y), (dx, dy)):
    return line((x, y), (x + dx, y + dy))

def direction(source, target):
    (xs, ys) = source
    (xt, yt) = target
    dx = xt - xs
    dy = yt - ys
    l = sqrt(dx**2 + dy**2)
    x = dx / l
    y = dy / l
    return (x, y)

RANGO = 5

def near(pixel, pixels):
    global RANGO
    (x, y) = pixel
    for dx in xrange(-RANGO, RANGO + 1):
        for dy in xrange(-RANGO, RANGO + 1):
            if (x + dx, y + dy) in pixels:
                return True
    return False

ZERO = 0.001

def eval(line, x = None, y = None):
    global ZERO
    (a, b) = line
    if x is None:
        if fabs(a) > ZERO:
            return (y - b) / (1.0 * a)
        else:
            return None
    if y is None:
        return a * x + b
    return None

def visible(line, dim):
    global RANGO
    (w, h) = dim
    cand = set()
    x = 0
    y = eval(line, x=x)
    if y is not None:
        y = int(y)
        if y >= 0 and y < h:
            cand.add((x, y))
    x = w - 1
    y = eval(line, x=x)
    if y is not None:
        y = int(y)
        if y >= 0 and y < h:
            cand.add((x, y))
    y = 0
    x = eval(line, y=y)
    if x is not None:
        x = int(x)
        if x >= 0 and x < w:
            cand.add((x, y))
    y = h - 1
    x = eval(line, y=y)
    if x is not None:
        x = int(x)
        if x >= 0 and x < w:
            cand.add((x, y))
    start = cand.pop()
    (xs, ys) = start
    while len(cand) > 0:
        end = cand.pop()
        (xe, ye) = end
        if fabs(xe - xs) < RANGO and fabs(ye - ys) < RANGO:
            continue
    return (start, end)

def contact(initial, direction, final, dim):
    global RANGO
    visited = []
    (x, y) = initial
    (dx, dy) = direction
    current = (x + RANGO * dx, y + RANGO * dy)
    start = True
    while True:
        (x, y) = current
        pos = (int(x), int(y))
        visited.append(pos)
        if not start and near(pos, final):
            return visited, current
        elif not near(pos, final):
            start = False
        nx = x + dx
        ny = y + dy
        if not existe((int(nx), int(ny)), dim):
            return visited, pos # out of the image on the next step
        current = (nx, ny)

def distance(A, B):
    (x1, y1) = A
    (x2, y2) = B
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def elipses(imagen):
    global RANGO
    (Gx, Gy, dom) = gradientes(imagen, borde = True)
    G = magnitud(Gx, Gy)
    borde = detectaBorde(imagen, G)
    dim = imagen.size
    (w, h) = dim
    grueso = ampliar(borde, dim)
    cand = list(borde) 
    votos = dict()
    segmentos = list()
    muestra = pideEntero('Cantidad de muestras: ')
    exitos = 0
    resultado = Image.new('RGB', dim)
    nuevos = resultado.load('filtro.png')
    pixeles = imagen.load('filtro.png')
    for x in xrange(w):
        for y in xrange(h):
            if (x, y) in borde:
                nuevos[x, y] = pixeles[x, y]
            else:
                nuevos[x, y] = 0, 0, 0

    draw = ImageDraw.Draw(resultado) 
    while exitos < muestra:
        A = choice(cand)
        (x1, y1) = A
        if x1 < RANGO or x1 > w - RANGO or y1 < RANGO or y1 > h - RANGO:
            continue
        B = choice(cand)
        (x2, y2) = B
        if x2 < RANGO or x2 > w - RANGO or y2 < RANGO or y2 > h - RANGO:
            continue
        if (A, B) in votos:
            continue

        A = (x1, y1) 
        B = (x2, y2)

        if distance(A, B) < 0.1 * min(w, h):
            continue

        gA = (Gx[x1][y1], Gy[x1][y1]) # the tangent is the gradient reversed
        gB = (Gx[x2][y2], Gy[x2][y2]) # and the direction of y is reversed due
        T1 = offset(A, gA)
        T2 = offset(B, gB)
        if parallel(T1, T2):
            continue
        #((x1, y1), (x2, y2)) = visible(T1, dim)
        #draw.line((x1, y1, x2, y2), fill=(0, 255, 0))
        #((x1, y1), (x2, y2)) = visible(T2, dim)
        #draw.line((x1, y1, x2, y2), fill=(0, 0, 255))
        #(x1, y1) = A
        #nuevos[x1, y1] = 255, 0, 0
        #(x2, y2) = B
        #nuevos[x2, y2] = 255, 0, 0

        T = crossing(T1, T2)
        if T is None:
            continue
        (x, y) = T
        T = (x, y)
 
        M = midpoint(A, B)
        if M in borde:
            continue

        if distance(M, T) > max(w, h):
            continue 

        TM = line(T, M)
        if TM is None:
            continue

        #((x1, y1), (x2, y2)) = visible(TM, dim)
        #draw.line((x1, y1, x2, y2), fill=(255, 100, 100))

 #       if existe(T, dim):
 #           (x, y) = T
 #           nuevos[x, y] = 255, 0, 0
 #       if existe(M, dim):
 #           (x, y) = M
 #           nuevos[x, y] = 255, 0, 0

        (dx, dy) = direction(T, M)
        (S, F) = contact(M, (dx, dy), grueso, dim)
        if distance(M, F) < RANGO:
            continue
   #     (sx, sy) = M
   #     (tx, ty) = F
   #     draw.line((int(sx), int(sy), int(tx), int(ty)), \
   #                  fill=(0, 255, 0))
        exitos += 1
        segmentos.append(S)
        votos[(A, B)] = S
        score = dict()
    for S in segmentos:
        for p in S:
            if p in score:
                score[p] += 1
            else:
                score[p] = 1
    highscore = max(score.values()) / 255.0
    for x in xrange(w):
        for y in xrange(h):
            p = (x, y)
            if p not in borde:
                if p in score:
                    color = int(score[p] / highscore)
                    nuevos[x, y] = color, color, 0
    imagen.save('final.png')
    return resultado
