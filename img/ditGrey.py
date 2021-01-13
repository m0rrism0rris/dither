from ditLib import *
from vo import vo
bit = 8
bitd = 255
c = c1

def load(file):
    t0 = time(); prnt('load ')
    file = png.Reader(file=open(file+'.png')).asDirect()
    info = file[3]
    s = 2 if info['alpha'] else 1
    img = []
    if info['greyscale']:
        for row in file[2]:
            r = []
            i = 0
            while i<info['size'][0]*s:
                r.append(lin(row[i]))
                i += s
            img.append(r)
    else:
        s += 2
        for row in file[2]:
            r = []
            i = 0
            while i<info['size'][0]*s:
                p = row[i]
                #c = (lin(row[i]),lin(row[i+1]),lin(row[i+2])); r.append((min(c)+max(c))/2) #HSL
                r.append(0.2126729*lin(row[i])+0.7151521*lin(row[i+1])+0.0721750*lin(row[i+2])) #XYZ
                i += s
            img.append(r)
    prnt(str(time()-t0)+'s\n'); return img

def save(file, vals):
    #print vals
    t0 = time(); prnt('save ')
    if isinstance(vals[0][0],float):
        vals = [[int(gam(i)*bitd+0.5) for i in ii] for ii in vals]
    file = open(file+'.png', 'wb')
    png.Writer(len(vals[0]),len(vals),(len(vals[0]),len(vals)),True,False,bit).write(file, vals)
    prnt(str(time()-t0)+'s\n')

def threshold(vals):
    t0 = time(); prnt('threshold ')
    vals = [[c(i) for i in ii] for ii in vals]
    prnt(str(time()-t0)+'s\n'); return vals

def sierraL(vals):
    t0 = time(); prnt('sierra-l ')
    bb = len(vals)-1; rb = len(vals[0])-1; ii = 0; i = 0; b = True
    while b:
        b = ii != bb
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = p-tup[cp]
                if b:
                    vals[ii+1][i] += e*0.25
                    if i!=0: vals[ii+1][i-1] += e*0.25
                if i<rb: vals[ii][i+1] += e*0.5
                else: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = p-tup[cp]
                if b:
                    vals[ii+1][i] += e*0.25
                    if i<rb: vals[ii+1][i+1] += e*0.25
                if i!=0: vals[ii][i-1] += e*0.5
                else: break
                i -= 1
        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def floydSteinberg(vals):
    t0 = time(); prnt('floyd-steinberg ')
    bb = len(vals)-1; rb = len(vals[0])-1; ii = 0; i = 0; b = True
    while b:
        b = ii != bb
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = p-tup[cp]
                if b:
                    vals[ii+1][i] += e*0.3125
                    if i!=0: vals[ii+1][i-1] += e*0.1875
                    if i<rb: vals[ii+1][i+1] += e*0.0625
                if i<rb: vals[ii][i+1] += e*0.4375
                else: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = p-tup[cp]
                if b:
                    vals[ii+1][i] += e*0.3125
                    if i<rb: vals[ii+1][i+1] += e*0.1875
                    if i!=0: vals[ii+1][i-1] += e*0.0625
                if i!=0: vals[ii][i-1] += e*0.4375
                else: break
                i -= 1
        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals


#floydsteinberg
#   x 7
# 3 5 1

#maybe
#   x 3
# 1 2 1

#stucki
#     x 8 4
# 2 4 8 4 2
# 1 2 4 2 1
'''
def floydSteinberg(vals):
    t0 = time(); prnt('floyd-steinberg ')
    bb = len(vals)-1; rb = len(vals[0])-1; ii = 0; i = 0; b = True
    while b:
        b = ii != bb
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/6
                if b:
                    vals[ii+1][i] += e*2
                    if i!=0: vals[ii+1][i-1] += e
                    if i<rb: vals[ii+1][i+1] += e
                if i<rb: vals[ii][i+1] += e*2
                else: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/6
                if b:
                    vals[ii+1][i] += e*2
                    if i<rb: vals[ii+1][i+1] += e
                    if i!=0: vals[ii+1][i-1] += e
                if i!=0: vals[ii][i-1] += e*2
                else: break
                i -= 1
        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals
'''


k = [
        [4],
    [2,3,1]]

'''
8 level-3
5 1 1 1
4 2 1 1
3 3 1 1
3 2 2 1
2 2 2 2

'''

# 3 2 1
k0 = float(k[0][0])/sum([sum(i) for i in k]); k1 = float(k[1][0])/sum([sum(i) for i in k]); k2 = float(k[1][1])/sum([sum(i) for i in k]); k3 = float(k[1][2])/sum([sum(i) for i in k])
def floydSteinberg(vals):
    t0 = time(); prnt('kernel ')
    bb = len(vals)-1; rb = len(vals[0])-1; ii = 0; i = 0; b = True
    while b:
        b = ii != bb
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = p-tup[cp]
                if b:
                    vals[ii+1][i] += e*k2
                    if i!=0: vals[ii+1][i-1] += e*k1
                    if i<rb: vals[ii+1][i+1] += e*k3
                if i<rb: vals[ii][i+1] += e*k0
                else: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = p-tup[cp]
                if b:
                    vals[ii+1][i] += e*k2
                    if i<rb: vals[ii+1][i+1] += e*k1
                    if i!=0: vals[ii+1][i-1] += e*k3
                if i!=0: vals[ii][i-1] += e*k0
                else: break
                i -= 1
        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals


def burkes(vals):
    t0 = time(); prnt('burkes ')
    bb = len(vals)-1; rb = len(vals[0])-1; rb2 = rb-1; ii = 0; i = 0; b = True
    while b:
        ii1 = ii+1; b = ii != bb
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/8
                l2 = i>1; l = i>0; r = i<rb; r2 = i<rb2
                if b:
                    if l2: vals[ii1][i-2] += e/2
                    if l: vals[ii1][i-1] += e
                    vals[ii1][i] += e*2
                    if r: vals[ii1][i+1] += e
                    if r2: vals[ii1][i+2] += e/2
                if r:
                    vals[ii][i+1] += e*2
                    if r2: vals[ii][i+2] += e
                else: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/8
                l2 = i>1; l = i>0; r = i<rb; r2 = i<rb2
                if b:
                    if l2: vals[ii1][i-2] += e/2
                    if l: vals[ii1][i-1] += e
                    vals[ii1][i] += e*2
                    if r: vals[ii1][i+1] += e
                    if r2: vals[ii1][i+2] += e/2
                if l:
                    vals[ii][i-1] += e*2
                    if l2: vals[ii][i-2] += e
                else: break
                i -= 1
        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def sierra2(vals):
    t0 = time(); prnt('sierra2 ')
    bb = len(vals)-1; rb = len(vals[0])-1; rb2 = rb-1; ii = 0; i = 0; b = True
    while b:
        ii1 = ii+1; b = ii != bb
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/16
                l2 = i>1; l = i>0; r = i<rb; r2 = i<rb2
                if b:
                    if l2: vals[ii1][i-2] += e
                    if l: vals[ii1][i-1] += e*2
                    vals[ii1][i] += e*3
                    if r: vals[ii1][i+1] += e*2
                    if r2: vals[ii1][i+2] += e
                if r:
                    vals[ii][i+1] += e*4
                    if r2: vals[ii][i+2] += e*3
                else: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/16
                l2 = i>1; l = i>0; r = i<rb; r2 = i<rb2
                if b:
                    if l2: vals[ii1][i-2] += e
                    if l: vals[ii1][i-1] += e*2
                    vals[ii1][i] += e*3
                    if r: vals[ii1][i+1] += e*2
                    if r2: vals[ii1][i+2] += e
                if l:
                    vals[ii][i-1] += e*4
                    if l2: vals[ii][i-2] += e*3
                else: break
                i -= 1
        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def sierra3(vals):
    t0 = time(); prnt('sierra3 ')
    bb = len(vals)-1; bb2 = bb-1; rb = len(vals[0])-1; rb2 = rb-1; ii = 0; i = 0; b = True
    while b:
        ii1 = ii+1; ii2 = ii+2; b = ii != bb; b2 = ii < bb2
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/16
                l2 = i>1; l = i>0; r = i<rb; r2 = i<rb2
                if b2:
                    if l: vals[ii2][i-1] += e
                    vals[ii2][i] += e*1.5
                    if r: vals[ii2][i+1] += e
                    if b:
                        if l2: vals[ii1][i-2] += e
                        if l: vals[ii1][i-1] += e*2
                        vals[ii1][i] += e*2.5
                        if r: vals[ii1][i+1] += e*2
                        if r2: vals[ii1][i+2] += e
                if r:
                    vals[ii][i+1] += e*2.5
                    if r2: vals[ii][i+2] += e*1.5
                else: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/16
                l2 = i>1; l = i>0; r = i<rb; r2 = i<rb2
                if b2:
                    if l: vals[ii2][i-1] += e
                    vals[ii2][i] += e*1.5
                    if r: vals[ii2][i+1] += e
                    if b:
                        if l2: vals[ii1][i-2] += e
                        if l: vals[ii1][i-1] += e*2
                        vals[ii1][i] += e*2.5
                        if r: vals[ii1][i+1] += e*2
                        if r2: vals[ii1][i+2] += e
                if l:
                    vals[ii][i-1] += e*2.5
                    if l2: vals[ii][i-2] += e*1.5
                else: break
                i -= 1

        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def stucki(vals):
    t0 = time(); prnt('stucki ')
    bb = len(vals)-1; bb2 = bb-1; rb = len(vals[0])-1; rb2 = rb-1; ii = 0; i = 0; b = True
    while b:
        ii1 = ii+1; ii2 = ii+2; b = ii != bb; b2 = ii < bb2
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/21
                l2 = i>1; l = i>0; r = i<rb; r2 = i<rb2
                if b2:
                    if l2: vals[ii2][i-2] += e/2
                    if l: vals[ii2][i-1] += e
                    vals[ii2][i] += e*2
                    if r: vals[ii2][i+1] += e
                    if r2: vals[ii2][i+2] += e/2
                    if b:
                        if l2: vals[ii1][i-2] += e
                        if l: vals[ii1][i-1] += e*2
                        vals[ii1][i] += e*4
                        if r: vals[ii1][i+1] += e*2
                        if r2: vals[ii1][i+2] += e
                if r:
                    vals[ii][i+1] += e*4
                    if r2: vals[ii][i+2] += e*2
                else: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/21
                l2 = i>1; l = i>0; r = i<rb; r2 = i<rb2
                if b2:
                    if l2: vals[ii2][i-2] += e/2
                    if l: vals[ii2][i-1] += e
                    vals[ii2][i] += e*2
                    if r: vals[ii2][i+1] += e
                    if r2: vals[ii2][i-1] += e/2
                    if b:
                        if l2: vals[ii1][i-2] += e
                        if l: vals[ii1][i-1] += e*2
                        vals[ii1][i] += e*4
                        if r: vals[ii1][i+1] += e*2
                        if r2: vals[ii1][i+2] += e
                if l:
                    vals[ii][i-1] += e*4
                    if l2: vals[ii][i-2] += e*2
                else: break
                i -= 1

        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def jarvis(vals):
    t0 = time(); prnt('jarvis ')
    bb = len(vals)-1; bb2 = bb-1; rb = len(vals[0])-1; rb2 = rb-1; ii = 0; i = 0; b = True
    while b:
        ii1 = ii+1; ii2 = ii+2; b = ii != bb; b2 = ii < bb2
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/48
                l2 = i>1; l = i>0; r = i<rb; r2 = i<rb2
                if b2:
                    if l2: vals[ii2][i-2] += e
                    if l: vals[ii2][i-1] += e*3
                    vals[ii2][i] += e*5
                    if r: vals[ii2][i+1] += e*3
                    if r2: vals[ii2][i+2] += e
                    if b:
                        if l2: vals[ii1][i-2] += e*3
                        if l: vals[ii1][i-1] += e*5
                        vals[ii1][i] += e*7
                        if r: vals[ii1][i+1] += e*5
                        if r2: vals[ii1][i+2] += e*3
                if r:
                    vals[ii][i+1] += e*7
                    if r2: vals[ii][i+2] += e*5
                else: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/48
                l2 = i>1; l = i>0; r = i<rb; r2 = i<rb2
                if b2:
                    if l2: vals[ii2][i-2] += e
                    if l: vals[ii2][i-1] += e*3
                    vals[ii2][i] += e*5
                    if r: vals[ii2][i+1] += e*3
                    if r2: vals[ii2][i-1] += e
                    if b:
                        if l2: vals[ii1][i-2] += e*3
                        if l: vals[ii1][i-1] += e*5
                        vals[ii1][i] += e*7
                        if r: vals[ii1][i+1] += e*5
                        if r2: vals[ii1][i+2] += e*3
                if l:
                    vals[ii][i-1] += e*7
                    if l2: vals[ii][i-2] += e*5
                else: break
                i -= 1

        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def shiauFan(vals):
    t0 = time(); prnt('shiau-fan ')
    bb = len(vals)-1; rb = len(vals[0])-1; r2 = rb-1; r3 = r2-1; ii = 0; i = 0; b = True
    while b:
        b = ii != bb
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/16
                if b:
                    vals[ii+1][i] += e*4
                    if i>0: vals[ii+1][i-1] += e*2
                    if i>1: vals[ii+1][i-2] += e
                    if i>2: vals[ii+1][i-3] += e
                if i<rb: vals[ii][i+1] += e*8
                else: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/16
                if b:
                    vals[ii+1][i] += e*4
                    if i<rb: vals[ii+1][i+1] += e*2
                    if i<r2: vals[ii+1][i+2] += e
                    if i<r3: vals[ii+1][i+3] += e
                if i!=0: vals[ii][i-1] += e*8
                else: break
                i -= 1
        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def ostromoukhov(vals):
    t0 = time(); prnt('ostromoukhov ')
    bb = len(vals)-1; rb = len(vals[0])-1; ii = 0; i = 0; b = True
    while b:
        b = ii != bb
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = p-tup[cp]
                n = vo[int(min(p,1)*255+0.5)]
                if b:
                    vals[ii+1][i] += e*n[2]
                    if i>0: vals[ii+1][i-1] += e*n[1]
                if i<rb: vals[ii][i+1] += e*n[0]
                else: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = p-tup[cp]
                n = vo[int(min(p,1)*255+0.5)]
                if b:
                    vals[ii+1][i] += e*n[2]
                    if i<rb: vals[ii+1][i+1] += e*n[1]
                if i>0: vals[ii][i-1] += e*n[0]
                else: break
                i -= 1
        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals
