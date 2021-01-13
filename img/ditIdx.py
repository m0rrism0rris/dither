from ditLib import *
from vo import vo
bit = 8
bitd = 255
c = c1
pal = ((0,0,0),(1,1,1))

def getPal(file):
    file = png.Reader(file=open(file+'.png')).asDirect()
    info = file[3]
    s = 4 if info['alpha'] else 3
    pal = []
    palrgb = []
    for row in file[2]:
        i = 0
        while i<info['size'][0]*s:
            pal.append((lin(row[i]),lin(row[i+1]),lin(row[i+2])))
            palrgb.append((row[i],row[i+1],row[i+2]))
            i += s
    palpy = open('palette.py','w+')
    palpy.write('palRgb = '+format(tuple(palrgb))+'\npal = '+format(tuple(pal))+'\npalD = '+str(len(palrgb)))
    palpy.close()

getPal('_db8')
from palette import *

def load(file):
    t0 = time(); prnt('load ')
    file = png.Reader(file=open(file+'.png')).asDirect()
    info = file[3]
    img = []
    if info['alpha']:
        for row in file[2]:
            r = []
            w = info['size'][0]*4
            i = 0
            while i<w:
                r.append(lin(row[i])); r.append(lin(row[i+1])); r.append(lin(row[i+2]))
                i += 4
            img.append(r)
    else:
        for row in file[2]:
            r = []
            w = info['size'][0]*3
            i = 0
            while i<w:
                r.append(lin(row[i])); r.append(lin(row[i+1])); r.append(lin(row[i+2]))
                i += 3
            img.append(r)
    prnt(str(time()-t0)+'s\n'); return img

def save(file,vals,pal):
    t0 = time(); prnt('save ')
    file = open(file+'.png', 'wb')
    png.Writer(len(vals[0]),len(vals),(len(vals[0]),len(vals)),alpha=False,palette=pal).write(file, vals)
    file.close()
    prnt(str(time()-t0)+'s\n')

'''def c_naive(i):
    dists = [(i[0]-p[0])**2+(i[1]-p[1])**2+(i[2]-p[2])**2 for p in pal]
    return dists.index(min(dists))

def c_weight(c):
    dists = []
    for p in pal:
        r = (c[0]+p[0])/2
        dists.append((2+r)*(c[0]-p[0])**2+4*(c[1]-p[1])**2+(3-r)*(c[2]-p[2])**2)
    return dists.index(min(dists))

c = c_naive
'''

def c_nv(r,g,b):
    dists = [(r-p[0])**2+(g-p[1])**2+(b-p[2])**2 for p in pal]
    return dists.index(min(dists))

def c_wt(r,g,b):
    dists = []
    for p in pal:
        R = (r+p[0])/2
        dists.append((2+R)*(r-p[0])**2+4*(g-p[1])**2+(3-R)*(b-p[2])**2)
    return dists.index(min(dists))

c = c_wt

def threshold(vals):
    t0 = time(); prnt('threshold ')
    w =  len(vals[0])
    oo = []
    for ii in vals:
        o = []
        i = 0
        while i < w:
            o.append(c(ii[i],ii[i+1],ii[i+2]))
            i += 3
        oo.append(o)
    prnt(str(time()-t0)+'s\n'); return oo

def sierraL(vals):
    t0 = time(); prnt('sierraL ')
    img = []; bb = len(vals)-1; rb = len(vals[0])-3; ii = 0; i = 0
    row = vals[0]
    while ii<=bb:
        prnt('\rsierraL '+str(ii))
        b = ii != bb
        o = []
        if b: row2 = vals[ii+1]
        i = 0
        while i<rb:
            R = i<rb
            r = row[i]; g = row[i+1]; b = row[i+2]
            np = c(r,g,b); o.append(np); nc = pal[np]
            r = min(r-nc[0],3); g = min(g-nc[1],3); b = min(b-nc[2],3);
            if b:
                row2[i] += r/4; row2[i+1] += g/4; row2[i+2] += b/4
                if i!=0: row2[i-3] += r/4; row2[i-2] += g/4; row2[i-1] += b/4
            if R: row[i+3] += r/2; row[i+4] += g/2; row[i+5] += b/2
            #else: break
            i += 3
        row = row2
        img.append(o)
        ii += 1

    prnt('\rsierraL '+str(time()-t0)+'s\n'); return img

save('H-sl',sierraL(load('H')),palRgb)
#from timeit import timeit
#print timeit('c_weight((random(),random(),random()))','from random import random; from __main__ import c_weight; from palette import pal',number=50000)
#print timeit('c_naive((random(),random(),random()))','from random import random; from __main__ import c_naive; from palette import pal',number=50000)
