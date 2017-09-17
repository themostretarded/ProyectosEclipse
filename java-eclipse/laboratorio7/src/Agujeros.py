#!/usr/bin/python
 
import random
from sys import argv
from PIL import Image, ImageTk, ImageDraw
 
def bfs( photo, pixel, color ):
 
    pix = photo.load()
    w, h = photo.size
 
    l = []
    v = []
 
    original = pix[ pixel ]
    l.append( pixel )
    
    while len( l ) > 0:
        ( x, y ) = l.pop( 0 )
        actual = pix[x, y]
        if actual == original or actual == color:
            for dx in [ -1, 0, 1 ]:
                for dy in [ -1, 0, 1 ]:
                    i, j = ( x + dx, y + dy )
                    if i >= 0 and i < w and j >= 0 and j < h:
                        aux = pix[ i, j ]
                        if aux == original:
                            pix[ i, j ] = color
                            l.append( ( i, j ) )
                            v.append( ( i, j ) )
    return photo, v
 
def binary( photo, u ):
    
    pix = photo.load()
    w, h = photo.size
 
    for i in xrange( w ):
        for j in xrange( h ):
            
            r, g, b = pix[ i, j ]
            gray = int( ( r + g + b ) / 3 )
 
            if gray > u:
                pix[ i, j ] = ( 0, 0, 0 )
            else:
                pix[ i, j ] = ( 255, 255, 255 )
 
    return pix
 
def hole_detection( im ):
 
    w, h = im.size
    pix = binary( im, 130 )
    
    hor_hist = []
    vert_hist = []
    
    peack_h = []
    peack_v = []
 
    for i in range( w ):
        fil = 0
        for j in range( h ):
            fil += pix[ i, j ][ 0 ]
        hor_hist.append( fil )
        
    for i in range( 1, len( hor_hist ) -1 ):   
        if hor_hist[ i ] > hor_hist[ i - 1 ] and hor_hist[ i ] > hor_hist[ i + 1 ]:
            peack_h.append( hor_hist[ i ] )
    
    print peack_h
 
    for i in xrange( h ):
        col = 0
        for j in xrange( w ):
            col += pix[ j, i ][ 0 ]
        vert_hist.append( col )
        
    for i in range( 1, len( vert_hist ) -1 ):   
        if vert_hist[ i ] > vert_hist[ i - 1 ] and vert_hist[ i ] > vert_hist[ i + 1 ]:
            peack_v.append( vert_hist[ i ] )
            
    print peack_v
 
    draw( im, peack_v, peack_h )
    draw( im, vert_hist, hor_hist )
 
    return peack_h, peack_v
 
def hole( im ):
    
    peack_h, peack_v = hole_detection( im )
    
    pix = im.load()
    w, h = im.size
 
    for i in range( w ):
        for j in range( h ):
            
            color = ( random.randint( 197, 255 ), random.randint( 75, 255 ), random.randint( 140, 255 ) )
 
            if pix[ i, j ] == ( 255, 255, 255 ):
                
                imagen, coord = bfs( im, ( i, j ), color )
    return 0
 
def draw( photo, ver, hor ):
 
    d = ImageDraw.Draw( photo )
    w, h = photo.size
 
    for i in range( len( ver ) ):
        if ver[ i ] != 0:
            d.line( ( ( 0, i ), ( w, i ) ), ( 255, 0, 0 ) )
 
    for i in range( len( hor ) ):
        if hor[ i ] != 0:
            d.line( ( ( i, 0 ), ( i, h ) ), ( 0, 255, 0 ) )
 
    photo.show()           
            
def main():
    
    image = Image.open( argv[ 1 ] ).convert( 'RGB' )
 
    hole( image )
 
main()
