from ditLib import *
bit = 8
bitd = 255
c = c1

def load(file):
    t0 = time(); prnt('load ')
    file = png.Reader(file=open(file+'.png')).asDirect()
    info = file[3]
    s = 4 if info['alpha'] else 3
    img = []
    if info['alpha']:
        for row in file[2]:
            r = []
            i = 0
            while i<info['size'][0]*4:
                p = row[i]
                r += [lin(row[i]),lin(row[i+1]),lin(row[i+2])]
                i += 4
            img.append(r)
        prnt(str(time()-t0)+'s\n'); return img
    for row in file[2]:
        r = []
        i = 0
        while i<info['size'][0]*3:
            p = row[i]
            r += [lin(row[i]),lin(row[i+1]),lin(row[i+2])]
            i += 3
        img.append(r)
    prnt(str(time()-t0)+'s\n'); return img


def save(file, vals):
    #print vals
    t0 = time(); prnt('save ')
    if isinstance(vals[0][0],float):
        vals = [[int(gam(i)*bitd+0.5) for i in ii] for ii in vals]
    file = open(file+'.png', 'wb')
    png.Writer(len(vals[0])/3,len(vals),(len(vals[0])/3,len(vals)),False,False,bit).write(file, vals)
    prnt(str(time()-t0)+'s\n')

def threshold(vals):
    t0 = time(); prnt('threshold ')
    vals = [[c(i) for i in ii] for ii in vals]
    prnt(str(time()-t0)+'s\n'); return vals

def sierraL(vals):
    t0 = time(); prnt('sierra-l ')
    bb = len(vals)-1; rb = len(vals[0])-3; R = rb+2; ii = 0; i = 0; b = True
    while b:
        b = ii != bb
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = p-tup[cp]
                if b:
                    vals[ii+1][i] += e*0.25
                    if i>2: vals[ii+1][i-3] += e*0.25
                if i<rb:
                    vals[ii][i+3] += e*0.5
                if i == R: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = p-tup[cp]
                if b:
                    vals[ii+1][i] += e*0.25
                    if i<rb: vals[ii+1][i+3] += e*0.25
                if i>2: vals[ii][i-3] += e*0.5
                if i == 0: break
                i -= 1
        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def floydSteinberg(vals):
    t0 = time(); prnt('floyd-steinberg ')
    bb = len(vals)-1; rb = len(vals[0])-3; R = rb+2; ii = 0; i = 0; b = True
    while b:
        b = ii != bb
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = p-tup[cp]
                if b:
                    vals[ii+1][i] += e*0.3125
                    if i>2: vals[ii+1][i-3] += e*0.1875
                    if i<rb: vals[ii+1][i+3] += e*0.0625
                if i<rb: vals[ii][i+3] += e*0.4375
                if i == R: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = p-tup[cp]
                if b:
                    vals[ii+1][i] += e*0.3125
                    if i<rb: vals[ii+1][i+3] += e*0.1875
                    if i!=0: vals[ii+1][i-3] += e*0.0625
                if i>2: vals[ii][i-3] += e*0.4375
                if i == 0: break
                i -= 1
        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def burkes(vals):
    t0 = time(); prnt('burkes ')
    bb = len(vals)-1; rb = len(vals[0])-3; rb2 = rb-6; R = rb+2; ii = 0; i = 0; b = True
    while b:
        ii1 = ii+1; b = ii != bb
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/8
                l2 = i>5; l = i>2; r = i<rb; r2 = i<rb2
                if b:
                    if l2: vals[ii1][i-6] += e/2
                    if l: vals[ii1][i-3] += e
                    vals[ii1][i] += e*2
                    if r: vals[ii1][i+3] += e
                    if r2: vals[ii1][i+6] += e/2
                if r:
                    vals[ii][i+3] += e*2
                    if r2: vals[ii][i+6] += e
                if i == R: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/8
                l2 = i>5; l = i>2; r = i<rb; r2 = i<rb2
                if b:
                    if l2: vals[ii1][i-6] += e/2
                    if l: vals[ii1][i-3] += e
                    vals[ii1][i] += e*2
                    if r: vals[ii1][i+3] += e
                    if r2: vals[ii1][i+6] += e/2
                if l:
                    vals[ii][i-3] += e*2
                    if l2: vals[ii][i-6] += e
                if i == 0: break
                i -= 1
        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def sierra2(vals):
    t0 = time(); prnt('sierra2 ')
    bb = len(vals)-1; rb = len(vals[0])-3; rb2 = rb-6; R = rb+2; ii = 0; i = 0; b = True
    while b:
        ii1 = ii+1; b = ii != bb
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/16
                l2 = i>5; l = i>2; r = i<rb; r2 = i<rb2
                if b:
                    if l2: vals[ii1][i-6] += e
                    if l: vals[ii1][i-3] += e*2
                    vals[ii1][i] += e*3
                    if r: vals[ii1][i+3] += e*2
                    if r2: vals[ii1][i+6] += e
                if r:
                    vals[ii][i+3] += e*4
                    if r2: vals[ii][i+6] += e*3
                if i == R: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/16
                l2 = i>5; l = i>2; r = i<rb; r2 = i<rb2
                if b:
                    if l2: vals[ii1][i-6] += e
                    if l: vals[ii1][i-3] += e*2
                    vals[ii1][i] += e*3
                    if r: vals[ii1][i+3] += e*2
                    if r2: vals[ii1][i+6] += e
                if l:
                    vals[ii][i-3] += e*4
                    if l2: vals[ii][i-6] += e*3
                if i == 0: break
                i -= 1
        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def jarvis(vals):
    t0 = time(); prnt('jarvis ')
    bb = len(vals)-1; bb2 = bb-1; rb = len(vals[0])-3; rb2 = rb-3; R = rb+2; ii = 0; i = 0; b = True
    while b:
        ii1 = ii+1; ii2 = ii+2; b = ii != bb; b2 = ii < bb2
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/48
                l2 = i>5; l = i>2; r = i<rb; r2 = i<rb2
                if b2:
                    if l2: vals[ii2][i-6] += e
                    if l: vals[ii2][i-3] += e*3
                    vals[ii2][i] += e*5
                    if r: vals[ii2][i+3] += e*3
                    if r2: vals[ii2][i+6] += e
                    if b:
                        if l2: vals[ii1][i-6] += e*3
                        if l: vals[ii1][i-3] += e*5
                        vals[ii1][i] += e*7
                        if r: vals[ii1][i+3] += e*5
                        if r2: vals[ii1][i+6] += e*3
                if r:
                    vals[ii][i+3] += e*7
                    if r2: vals[ii][i+6] += e*5
                if i == R: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/48
                l2 = i>5; l = i>2; r = i<rb; r2 = i<rb2
                if b2:
                    if l2: vals[ii2][i-6] += e
                    if l: vals[ii2][i-3] += e*3
                    vals[ii2][i] += e*5
                    if r: vals[ii2][i+3] += e*3
                    if r2: vals[ii2][i-6] += e
                    if b:
                        if l2: vals[ii1][i-6] += e*3
                        if l: vals[ii1][i-3] += e*5
                        vals[ii1][i] += e*7
                        if r: vals[ii1][i+3] += e*5
                        if r2: vals[ii1][i+6] += e*3
                if l:
                    vals[ii][i-3] += e*7
                    if l2: vals[ii][i-6] += e*5
                if i == 0: break
                i -= 1

        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def sierra3(vals):
    t0 = time(); prnt('sierra3 ')
    bb = len(vals)-1; bb2 = bb-1; rb = len(vals[0])-3; rb2 = rb-3; R = rb+2; ii = 0; i = 0; b = True
    while b:
        ii1 = ii+1; ii2 = ii+2; b = ii != bb; b2 = ii < bb2
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/16
                l2 = i>5; l = i>2; r = i<rb; r2 = i<rb2
                if b2:
                    if l: vals[ii2][i-3] += e
                    vals[ii2][i] += e*1.5
                    if r: vals[ii2][i+3] += e
                    if b:
                        if l2: vals[ii1][i-6] += e
                        if l: vals[ii1][i-3] += e*2
                        vals[ii1][i] += e*2.5
                        if r: vals[ii1][i+3] += e*2
                        if r2: vals[ii1][i+6] += e
                if r:
                    vals[ii][i+3] += e*2.5
                    if r2: vals[ii][i+6] += e*1.5
                if i == R: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/16
                l2 = i>5; l = i>2; r = i<rb; r2 = i<rb2
                if b2:
                    if l: vals[ii2][i-3] += e
                    vals[ii2][i] += e*1.5
                    if r: vals[ii2][i+3] += e
                    if b:
                        if l2: vals[ii1][i-6] += e
                        if l: vals[ii1][i-3] += e*2
                        vals[ii1][i] += e*2.5
                        if r: vals[ii1][i+3] += e*2
                        if r2: vals[ii1][i+6] += e
                if l:
                    vals[ii][i-3] += e*2.5
                    if l2: vals[ii][i-6] += e*1.5
                if i == 0: break
                i -= 1

        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

def stucki(vals):
    t0 = time(); prnt('stucki ')
    bb = len(vals)-1; bb2 = bb-1; rb = len(vals[0])-3; rb2 = rb-3; R = rb+2; ii = 0; i = 0; b = True
    while b:
        ii1 = ii+1; ii2 = ii+2; b = ii != bb; b2 = ii < bb2
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/21
                l2 = i>5; l = i>2; r = i<rb; r2 = i<rb2
                if b2:
                    if l2: vals[ii2][i-6] += e/2
                    if l: vals[ii2][i-3] += e
                    vals[ii2][i] += e*2
                    if r: vals[ii2][i+3] += e
                    if r2: vals[ii2][i+6] += e/2
                    if b:
                        if l2: vals[ii1][i-6] += e
                        if l: vals[ii1][i-3] += e*2
                        vals[ii1][i] += e*4
                        if r: vals[ii1][i+3] += e*2
                        if r2: vals[ii1][i+6] += e
                if r:
                    vals[ii][i+3] += e*4
                    if r2: vals[ii][i+6] += e*2
                if i == R: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/21
                l2 = i>5; l = i>2; r = i<rb; r2 = i<rb2
                if b2:
                    if l2: vals[ii2][i-6] += e/2
                    if l: vals[ii2][i-3] += e
                    vals[ii2][i] += e*2
                    if r: vals[ii2][i+3] += e
                    if r2: vals[ii2][i-6] += e/2
                    if b:
                        if l2: vals[ii1][i-6] += e
                        if l: vals[ii1][i-3] += e*2
                        vals[ii1][i] += e*4
                        if r: vals[ii1][i+3] += e*2
                        if r2: vals[ii1][i+6] += e
                if l:
                    vals[ii][i-3] += e*4
                    if l2: vals[ii][i-6] += e*2
                if i == 0: break
                i -= 1

        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals

#'''
def stucki(vals):
    t0 = time(); prnt('stucki-b ')
    bb = len(vals)-1; bb2 = bb-1; rb = len(vals[0])-3; rb2 = rb-3; R = rb+2; ii = 0; i = 0; b = True
    while b:
        ii1 = ii+1; ii2 = ii+2; b = ii != bb; b2 = ii < bb2
        if ii&1 == 0:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/21; e2 = e*2
                l2 = i>5; l = i>2; r = i<rb; r2 = i<rb2
                if b2:
                    if l2: vals[ii2][i-6] += e/2
                    if l: vals[ii2][i-3] += e
                    vals[ii2][i] += e2
                    if r: vals[ii2][i+3] += e
                    if r2: vals[ii2][i+6] += e/2
                    if b:
                        if l2: vals[ii1][i-6] += e
                        if l: vals[ii1][i-3] += e2
                        vals[ii1][i] += e*4
                        if r: vals[ii1][i+3] += e2
                        if r2: vals[ii1][i+6] += e
                if r:
                    vals[ii][i+3] += e*4
                    if r2: vals[ii][i+6] += e2
                if i == R: break
                i += 1
        else:
            while True:
                p = vals[ii][i]; cp = c(p); vals[ii][i] = cp; e = (p-tup[cp])/21; e2 = e*2
                l2 = i>5; l = i>2; r = i<rb; r2 = i<rb2
                if b2:
                    if l2: vals[ii2][i-6] += e/2
                    if l: vals[ii2][i-3] += e
                    vals[ii2][i] += e2
                    if r: vals[ii2][i+3] += e
                    if r2: vals[ii2][i-6] += e/2
                    if b:
                        if l2: vals[ii1][i-6] += e
                        if l: vals[ii1][i-3] += e2
                        vals[ii1][i] += e*4
                        if r: vals[ii1][i+3] += e2
                        if r2: vals[ii1][i+6] += e
                if l:
                    vals[ii][i-3] += e*4
                    if l2: vals[ii][i-6] += e2
                if i == 0: break
                i -= 1

        ii += 1
    prnt(str(time()-t0)+'s\n'); return vals
#'''
