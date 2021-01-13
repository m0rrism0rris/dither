import png
import cie
import math
import os
import sys
os.chdir('/Users/cy4n/Desktop/python/ciedither')

info = {'greyscale' : False, 'alpha' : False, 'bitdepth' : 8}
depth = 255.
def loadGrey(file):
	global depth; global info
	depth = float(depth)
	print 'loading'
	file = png.Reader(file=open(file+'.png')).asRGB8()
	info = file[3]
	info['greyscale'] = True
	img = []
	for row in file[2]:
		r = []
		i = 0
		while i<info['size'][0]*3:
			r.append(vMunsell((row[i]/depth,
			row[i+1]/depth,
			row[i+2]/depth)))
			i += 3

		img.append(r)
	depth = int(2**bits-1)
	return img

def loadPal(file):
	file = png.Reader(file=open(file+'.png')).asRGB8()
	pal = []
	width = file[3]['size'][0]*3
	for row in file[2]:
		i = 0
		while i<width:
			pal.append((row[i]/depth,
			row[i+1]/depth,
			row[i+2]/depth))
			i += 3

	return pal

def load(file,greyscale=False):
	global info
	print 'loading'
	file = png.Reader(file=open(file+'.png')).asRGB8()
	info = file[3]
	info['greyscale'] = greyscale
	img = []
	if greyscale:
		for row in file[2]:
			r = []
			i = 0
			while i<info['size'][0]*3:
				v = lrgb((row[i]/depth,
				row[i+1]/depth,
				row[i+2]/depth))
				v = 0.2126729*v[0]+0.7151522*v[1]+0.0721750*v[2]
				r.append(1.055*v**0.41666666666-0.055 if v>0.0031308 else v*12.92)
				i += 3

			img.append(r)

	else:
		for row in file[2]:
			r = []
			i = 0
			while i<info['size'][0]*3:
				r.append((row[i]/depth,
				row[i+1]/depth,
				row[i+2]/depth))
				i += 3

			img.append(r)

	return img

def loadT(file,type='color'):
	print 'loading'
	global info
	type = type.lower()
	file = png.Reader(file=open(file+'.png')).asRGB()
	info = file[3]
	info['greyscale'] = type in ('l','grey','gray','greyscale','grayscale')
	img = []; i = 0
	if info['greyscale']:
		for row in file[2]:
			r = []; i = 0
			while i<info['size'][0]*3:
				v = lrgb((row[i]/depth,row[i+1]/depth,row[i+2]/depth))
				r.append((0.2126729*v[0]+0.7151522*v[1]+0.0721750*v[2]))
				i += 3
			img.append(r)
	if type in ('rgb','srgb','color'):
		for row in file[2]:
			r = []; i = 0
			while i<info['size'][0]*3:
				r.append((row[i]/depth,row[i+1]/depth,row[i+2]/depth))
				i += 3
			img.append(r)
	if type == 'lrgb':
		for row in file[2]:
			r = []; i = 0
			while i<info['size'][0]*3:
				r.append(lrgb((row[i]/depth,row[i+1]/depth,row[i+2]/depth)))
				i += 3
			img.append(r)
	if type == 'xyz':
		for row in file[2]:
			r = []; i = 0
			while i<info['size'][0]*3:
				r.append(cie.xyz((row[i]/depth,row[i+1]/depth,row[i+2]/depth)))
				i += 3
			img.append(r)
	if type == 'lab':
		for row in file[2]:
			r = []; i = 0
			while i<info['size'][0]*3:
				r.append(cie.lab(cie.xyz((row[i]/depth,row[i+1]/depth,row[i+2]/depth))))
				i += 3
			img.append(r)
	if type == 'uvw':
		for row in file[2]:
			r = []; i = 0
			while i<info['size'][0]*3:
				r.append(cie.uvw(cie.xyz((row[i]/depth,row[i+1]/depth,row[i+2]/depth))))
				i += 3
			img.append(r)
	if type == 'luv':
		for row in file[2]:
			r = []; i = 0
			while i<info['size'][0]*3:
				r.append(cie.luv(cie.xyz((row[i]/depth,row[i+1]/depth,row[i+2]/depth))))
				i += 3
			img.append(r)
	return img

def lrgb(srgb):
	return (
        ((srgb[0]+0.055)/1.055)**2.4 if srgb[0]>0.04045 else srgb[0]/12.92,
        ((srgb[1]+0.055)/1.055)**2.4 if srgb[1]>0.04045 else srgb[1]/12.92,
        ((srgb[2]+0.055)/1.055)**2.4 if srgb[2]>0.04045 else srgb[2]/12.92)

def lin(v): return ((v+0.055)/1.055)**2.4 if v>0.04045 else v/12.92
def gamma(v): return 1.055*v**0.41666666666-0.055 if v>0.0031308 else v*12.92
def clip(i): i #return 1 if i > 1 else -.05 if i < -.05 else i
def bit(i): return 0 if i <= 0 else depth if i >= 1 else int(i*depth+0.5)

def saveGrey(file,vals):
	print 'saving'
	exp = [[bit(i) for i in ii] for ii in vals]
	file = open(file+'.png', 'wb')
	png.Writer(
	info['size'][0],
	info['size'][1],
	info['size'],
	greyscale = True
	).write(file, exp)

def saveColor(file,vals,bits=8):
	global info; global depth
	depth = 2**bits-1
	info['bitdepth'] = bits
	info['greyscale'] = isinstance(vals[0][0],float)
	info['size'] = (len(vals[0]) if info['greyscale'] else len(vals[0])/3,len(vals))
	print 'saving'
	print info
	if info['greyscale']:
		exp = [[bit(i) for i in ii] for ii in vals]

	else:
		exp = []
		for ii in vals:
			o = []
			for i in ii:
				o.append(bit(i[0]))
				o.append(bit(i[1]))
				o.append(bit(i[2]))
			exp.append(o)

	file = open(file+'.png', 'wb')
	png.Writer(
	info['size'][0],
	info['size'][1],
	info['size'],
	info['greyscale'],
	False,
	info['bitdepth']
	).write(file, exp)

def close(c):
	dists = []
	for p in pal:
		dists.append((c[0]-p[0])**2+(c[1]-p[1])**2+(c[2]-p[2])**2)
	return dists.index(min(dists))

def close2(c):
	dists = []
	for p in pal:
		r = (c[0]+p[0])/2
		dists.append((2+r)*(c[0]-p[0])**2+4*(c[1]-p[1])**2+(3-r)*(c[2]-p[2])**2)
	return dists.index(min(dists))

def saveIndexed(file,img):
	global depth; global info; depth = int(depth)
	print 'saving'
	info['size'] = (len(img[0]),len(img))
	file = open(file+'.png', 'wb')
	png.Writer(
	info['size'][0],
	info['size'][1],
	info['size'],
	False,
	False,
	8,
	palette=[(bit(a),bit(b),bit(c)) for a,b,c in palS]
	).write(file, img)

def indexFS(vals):
	print 'dithering'
	x = 0
	for y in range(len(vals)):
		b = y != info['size'][1]-1
		if y % 2 == 0:
			while True:
				i = vals[y][x]
				vals[y][x] = close(i)
				p = pal[vals[y][x]]
				e = (((i[0]-p[0])/16.),
					((i[1]-p[1])/16.),
					((i[2]-p[2])/16.))
				v = (x != info['size'][0]-1, x != 0)
				if b:
					vals[y+1][x] = (vals[y+1][x][0]+e[0]*5,vals[y+1][x][1]+e[1]*5,vals[y+1][x][2]+e[2]*5)
					if v[0]: vals[y+1][x+1] = (vals[y+1][x+1][0]+e[0],vals[y+1][x+1][1]+e[1],vals[y+1][x+1][2]+e[2])
					if v[1]: vals[y+1][x-1] = (vals[y+1][x-1][0]+e[0]*3,vals[y+1][x-1][1]+e[1]*3,vals[y+1][x-1][2]+e[2]*3)
				if v[0]:
					vals[y][x+1] = (vals[y][x+1][0]+e[0]*7,vals[y][x+1][1]+e[1]*7,vals[y][x+1][2]+e[2]*7)
					x += 1
				else: break
		else:
			while True:
				i = vals[y][x]
				vals[y][x] = close(i)
				p = pal[vals[y][x]]
				e = (((i[0]-p[0])/16.),
					((i[1]-p[1])/16.),
					((i[2]-p[2])/16.))
				v = (x != 0, x != info['size'][0]-1)
				if b:
					vals[y+1][x] = (vals[y+1][x][0]+e[0]*5,vals[y+1][x][1]+e[1]*5,vals[y+1][x][2]+e[2]*5)
					if v[0]: vals[y+1][x-1] = (vals[y+1][x-1][0]+e[0],vals[y+1][x-1][1]+e[1],vals[y+1][x-1][2]+e[2])
					if v[1]: vals[y+1][x+1] = (vals[y+1][x+1][0]+e[0]*3,vals[y+1][x+1][1]+e[1]*3,vals[y+1][x+1][2]+e[2]*3)
				if v[0]:
					vals[y][x-1] = (vals[y][x-1][0]+e[0]*7,vals[y][x-1][1]+e[1]*7,vals[y][x-1][2]+e[2]*7)
					x -= 1
				else: break

	return vals

if __name__ == "__main__":
    files = sys.argv[1:]

def db32(file):
	global pal; global palS
	palS = loadPal('db32')
	pal = [(cie.xyz(i)) for i in palS]
	img = loadT(file,'xyz')
	exp = indexFS(img)
	saveIndexed(file+'-xyz',exp)

for file in files:
	db32(file)
