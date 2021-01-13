import png,os
from sys import stdout
from time import time
os.chdir('/Users/cy4n/Desktop/python/img')
from vo import vO, vo

def sysP(s):
	stdout.write(s)
	stdout.flush()

info = {}
depth = 255.
bits = 8
gamma = False

pal = ((0,0,0),(1,1,1))

def loadColor(file):
	global info
	t0 = time(); sysP('loading ')
	file = png.Reader(file=open(file+'.png')).asRGBA8()
	info = file[3]
	img = []
	if False:
		for row in file[2]:
			r = []
			i = 0
			while i<info['size'][0]*4:
				r.append(row[i]);r.append(row[i+1]);r.append(row[i+2])
				i += 4
			img.append(r)
		sysP(str(time()-t0)+'s\n'); return img
	else:
		for row in file[2]:
			r = []
			i = 0
			#((v+0.055)/1.055)**2.4 if v>0.04045 else v/12.92
			while i<info['size'][0]*4:
				p = row[i]
				r.append((p/269.025+0.05213270142)**2.4 if p>10 else p/3294.6)
				p = row[i+1]
				r.append((p/269.025+0.05213270142)**2.4 if p>10 else p/3294.6)
				p = row[i+2]
				r.append((p/269.025+0.05213270142)**2.4 if p>10 else p/3294.6)
				i += 4
			img.append(r)
		sysP(str(time()-t0)+'s\n'); return img

def saveColor(file,vals,bits=8,triple=True):
	global info; global depth
	depth = 2**(8-bits)
	tr = trc[bits-1]
	info['bitdepth'] = bits
	info['size'] = (len(vals[0])/3,len(vals))
	print 'saving'
	print info
	if triple:
		exp = [[i/depth for i in ii] for ii in vals]

	file = open(file+'.png', 'wb')
	png.Writer(
	info['size'][0],
	info['size'][1],
	info['size'],
	False,
	False,
	info['bitdepth']
	).write(file, exp)

def saveDir(file,vals):
	t0 = time(); sysP('saving ')
	file = open(file+'.png', 'wb')
	png.Writer(
	len(vals[0])/3,
	len(vals),
	(len(vals[0])/3,len(vals)),
	False,
	False,
	bits
	).write(file, vals)
	sysP(str(time()-t0)+'s\n');

'''def bitVO(vals):
	t0 = time(); sysP('dithering '); exp = []; rb = len(vals[0])-3; w = len(vals[0]); i = 0
	for ii in xrange(len(vals)):
		r = [0]*w; b = ii != len(vals)-1
		if ii % 2 == 0:
			while i < w-1:
				p = vals[ii][i]; np = cBit(p); r[i] = np; e = p-tup[np]
				c = vo[min(int(p*255),255)]
				if i<rb: vals[ii][i+3] += e*c[0]
				if b:
					if i<2: vals[ii+1][i-3] += e*c[1]
					vals[ii+1][i] += e*c[2]
				i += 1
		else:
			while i > 0:
				p = vals[ii][i]; np = cBit(p); r[i] = np; e = p-tup[np]
				c = vo[min(int(p*255),255)]
				if i!=0: vals[ii][i-3] += e*c[0]
				if b:
					if i<rb: vals[ii+1][i+3] += e*c[1]
					vals[ii+1][i] += e*c[2]
				i -= 1
		exp.append(r)
	sysP(str(time()-t0)+'s\n'); return exp'''

def bitFS(vals):
	mx = 2**bits-1
	depth = 2**(8-bits)
	print 'dithering'
	rb = len(vals[0])-3
	exp = []
	for ii in range(len(vals)):
		r = []
		b = ii != len(vals)-1
		for i in range(len(vals[0])):
			p = vals[ii][i]
			r.append(min(p/depth,mx))
			#e = p%depth
			e=0
			v = (i < rb, i != 0)
			if b:
				vals[ii+1][i] += e*5/16
				if v[0]: vals[ii+1][i+3] += e/16
				if v[1]: vals[ii+1][i-3] += e*3/16
			if v[0]:
				vals[ii][i+3] += e*7/16
		exp.append(r)
	return exp

def bitSF(vals):
	mx = 2**bits-1
	depth = 2**(8-bits)
	print 'dithering'
	rb = len(vals[0])-3
	exp = []
	for ii in range(len(vals)):
		r = []
		b = ii != len(vals)-1
		for i in range(len(vals[0])):
			p = vals[ii][i]
			r.append(min(p/depth,mx))
			e = p%depth
			if b:
				vals[ii+1][i] += e/4
				if i > 8:
					vals[ii+1][i-9] += e/16
					if i > 5:
						vals[ii+1][i-6] += e/16
						if i > 2:
							vals[ii+1][i-3] += e/8
			if i < rb:
				vals[ii][i+3] += e/2
		exp.append(r)
	return exp

def bitFSL(vals):
	t0 = time(); sysP('dithering ')
	rb = len(vals[0])-3
	exp = []
	for ii in range(len(vals)):
		r = []
		b = ii != len(vals)-1
		for i in range(len(vals[0])):
			p = vals[ii][i]
			np = cBit(p)
			r.append(np)
			e = p-np/bitd
			if b:
				vals[ii+1][i] += e*5/16.
				if i<rb: vals[ii+1][i+3] += e/16.
				if i!=0: vals[ii+1][i-3] += e*3/16.
			if i<rb:
				vals[ii][i+3] += e*7/16.
		exp.append(r)
	sysP(str(time()-t0)+'s\n'); return exp

def bitFS(vals):
	t0 = time(); sysP('dithering ')
	rb = len(vals[0])-3; w = len(vals[0]); exp = []; i = 0
	for ii in xrange(len(vals)):
		b = ii != len(vals)-1; r = [0]*w
		if ii % 2 == 0:
			while i < w-1:
				p = vals[ii][i]; n = cBit(p); r[i] = n; e = p-tup[n]
				if b:
					vals[ii+1][i] += e*0.3125
					if i<rb: vals[ii+1][i+3] += e*0.0625
					if i!=0: vals[ii+1][i-3] += e*0.1875
				if i<rb: vals[ii][i+3] += e*0.4375
				i += 1
		else:
			while i > 0:
				p = vals[ii][i]; n = cBit(p); r[i] = n; e = p-tup[n]
				if b:
					vals[ii+1][i] += e*0.3125
					if i<rb: vals[ii+1][i+3] += e*0.1875
					if i!=0: vals[ii+1][i-3] += e*0.0625
				if i!=0: vals[ii][i-3] += e*0.4375
				i -= 1
		exp.append(r)
	sysP(str(time()-t0)+'s\n'); return exp

def bitSierraL(vals):
	t0 = time(); sysP('dithering ')
	rb = len(vals[0])-3; w = len(vals[0]); exp = []; i = 0
	for ii in xrange(len(vals)):
		b = ii != len(vals)-1; r = [0]*w
		if ii % 2 == 0:
			while i < w-1:
				p = vals[ii][i]; n = cBit(p); r[i] = n; e = p-tup[n]
				if b:
					vals[ii+1][i] += e*0.25
					if i!=0: vals[ii+1][i-3] += e*0.25
				if i<rb: vals[ii][i+3] += e*0.5
				i += 1
		else:
			while i > 0:
				p = vals[ii][i]; n = cBit(p); r[i] = n; e = p-tup[n]
				if b:
					vals[ii+1][i] += e*0.25
					if i<rb: vals[ii+1][i+3] += e*0.25
				if i!=0: vals[ii][i-3] += e*0.5
				i -= 1
		exp.append(r)
	sysP(str(time()-t0)+'s\n'); return exp

bits = 1
fil = 'great'
bitd = 2**bits-1
def lin(i): return ((i+0.055)/1.055)**2.4 if i>0.04045 else i/12.92
tup = tuple([lin(float(i)/bitd) for i in range(bitd+1)])

def closeL(i):
	dists = [(i-d)**2 for d in tup]
	return dists.index(min(dists))

def cPal(i):
	dists = [(i[0]-d[0])**2+(i[1]-d[1])**2+(i[2]-d[2])**2 for d in pal]
	return dists.index(min(dists))

def cPal2(r,g,b):
	dists = [(tup[r]-d[0])**2+(tup[g]-d[1])**2+(tup[b]-d[2])**2 for d in pal]
	return dists.index(min(dists))

def cOrder(i):
	if i<tup[1]: return 0
	if i>tup[bitd-1]: return bitd
	o = 0
	dPrev = 1; dCurr = 0
	while True:
		dCurr = abs(i-tup[o])
		if dCurr>dPrev:
			break
		dPrev = dCurr
		o += 1
	return o-1

def cSplit1(i):
	if i > 0.24620132670783548: return 1
	return 0

def cSplit2(i):
	if i > 0.24620132670783548:
		if i > 0.4019777798321958: return 3
		return 2
	if i > 0.08865558628577294: return 1
	return 0

cBit = cSplit1
saveDir(fil+'sierra-l',bitSierraL(loadColor(fil)))
