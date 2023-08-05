from colorsys import hsv_to_rgb as h2r,  rgb_to_hsv as r2h
__all__ = "getRGB", "getHSV"

def getRGB(baseHSV):
    h, s, v = baseHSV
    r, g, b = h2r(h/360.0, s/100.0, v/100.0) #returns rgb as percentage
    return '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))

def getHSV(rgb):
    "convert RGB format ('#abcdef')to HSV ((360, 100, 100))"
    RGB = []
    for n in (1, 3, 5): #split string into 2 char hex values
        RGB.append(rgb[n : n+2])
    r, g, b = [int(n, 16)/255.0 for n in RGB ]
    h, s, v = r2h(r, g, b)
    return tuple([int(n) for n in (h*360, s*100, v*100)])
    #getHVS('#a42889') yields  (313, 75, 64) gimp shows 313, 76, 64 
    
