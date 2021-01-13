import f
import png
import cie
import sys
from time import sleep

def lin(rgb):
	return (
        ((rgb[0]+0.055)/1.055)**2.4 if rgb[0]>0.04045 else rgb[0]/12.92,
        ((rgb[1]+0.055)/1.055)**2.4 if rgb[1]>0.04045 else rgb[1]/12.92,
        ((rgb[2]+0.055)/1.055)**2.4 if rgb[2]>0.04045 else rgb[2]/12.92)

def bit(c):
	return (
		int(min(max(c[0],0),1)*255+0.5),
		int(min(max(c[1],0),1)*255+0.5),
		int(min(max(c[2],0),1)*255+0.5))


def clip(value):
    #return -.05 if value < -.05 else .05 if value > .05 else value #XYZ
	#return -.1 if value < -.1 else .1 if value > .1 else value #lRGB
	return -1 if value < -1 else 1 if value > 1 else value
	#return -10 if value < -10 else 10 if value > 10 else value #luv
	#return -5 if value < -5 else 5 if value > 5 else value #lab

def loadpalette(file):
	file = png.Reader(file=open(file+'.png')).asRGBA8()
	pal = []
	seen = []
	for row in file[2]:
		for i in xrange(len(row)/4):
			pix = f._bit((row[4*i],row[4*i+1],row[4*i+2]))
			if pix not in seen:
				seen = list(seen)
				seen.append(pix)
				seen = set(seen)
				pal.append(pix)
	return pal

def genPalette(bits):
	bits = (1<<bits)-1
	pal = []
	for i in xrange(bits+1):
		c = float(i)/bits
		pal.append(tuple([((c+0.055)/1.055)**2.4 if c>0.04045 else c/12.92]*3))
	return pal

def saveIndexed(file,vals):
	print 'saving'
	file = open(file+'.png', 'wb')
	png.Writer(
	f.info['size'][0],
	f.info['size'][1],
	palette = [(f.bit(a),f.bit(b),f.bit(c)) for a,b,c in palrgb],
	).write(file, vals)

def floydSteinberg(vals):
	img = []
	x = f.info['size'][0]
	for y in range(f.info['size'][1]):
		sys.stdout.write('\r'+str(y)); sys.stdout.flush()
		row = [11]*f.info['size'][0]
		if y % 2 == 1:
			while True:
				pix = vals[y][x]
				close = closest(pix)
				row[x] = close
				close = pal[close]
				e = ((clip(pix[0]-close[0])/16.),clip((pix[1]-close[1])/16.),clip((pix[2]-close[2])/16.))
				v = (x != f.info['size'][0] - 1, y != f.info['size'][1] - 1, x != 0)
				if v[1]:
					w = vals[y+1][x]; vals[y+1][x] = (w[0]+e[0]*5,w[1]+e[1]*5,w[2]+e[2]*5)
					if v[0]:
						w = vals[y+1][x+1]; vals[y+1][x+1] = (w[0]+e[0],w[1]+e[1],w[2]+e[2])
					if v[2]:
						w = vals[y+1][x-1]; vals[y+1][x-1] = (w[0]+e[0]*3,w[1]+e[1]*3,w[2]+e[2]*3)
				if v[0]:
					w = vals[y][x+1]; vals[y][x+1] = (w[0]+e[0]*7,w[1]+e[1]*7,w[2]+e[2]*7)
					x += 1
				else: break
		else:
			while True:
				pix = vals[y][x]
				close = closest(pix)
				row[x] = close
				close = pal[close]
				e = ((clip(pix[0]-close[0])/16.),clip((pix[1]-close[1])/16.),clip((pix[2]-close[2])/16.))
				v = (x != 0, y != f.info['size'][1] - 1, x != f.info['size'][0] - 1)
				if v[1]:
					w = vals[y+1][x]; vals[y+1][x] = (w[0]+e[0]*5,w[1]+e[1]*5,w[2]+e[2]*5)
					if v[0]:
						w = vals[y+1][x-1]; vals[y+1][x-1] = (w[0]+e[0],w[1]+e[1],w[2]+e[2])
					if v[2]:
						w = vals[y+1][x+1]; vals[y+1][x+1] = (w[0]+e[0]*3,w[1]+e[1]*3,w[2]+e[2]*3)
				if v[0]:
					w = vals[y][x-1]; vals[y][x-1] = (w[0]+e[0]*7,w[1]+e[1]*7,w[2]+e[2]*7)
					x -= 1
				else: break

		img.append(row)
	sys.stdout.write('\r'); sys.stdout.flush()
	return img

def closest(c):
	dists = []
	for p in pal:
		dists.append((c[0]-p[0])**2+(c[1]-p[1])**2+(c[2]-p[2])**2)
	return dists.index(min(dists))

#def deltaE(c):
#	dists = []
#	for p in pal:
#		dists.append((c[0]-p[0])**2+(c[1]-p[1])**2+(c[2]-p[2])**2)
#		#dists.append(abs(c[0]-p[0])+abs(c[1]-p[1])+abs(c[2]-p[2]))
#	return dists.index(min(dists))


#palrgb = loadpalette('majesty')
palrgb = tuple(genPalette(2))
pal = palrgb
files = []
if __name__ == "__main__":
    files = sys.argv[1:]

for file in files:
	vals = f.load(file,greyscale=False)
	indexes = []
	for row in vals:
		irow = []
		for rgb in row:
			rgb = (rgb)
			#irow.append((0.2126729*rgb[0]+0.7151522*rgb[1]+0.0721750*rgb[2]))
			irow.append(int(rgb[0]*3.99999))
		indexes.append(irow)
	print palrgb
	#f.info['greyscale'] = True
	#def clip(value): return -1 if value < -1 else 1 if value > 1 else value

	#pal = [bit(lin(c)) for c in palrgb]
	#vals_c = [[bit(lin(c)) for c in row] for row in vals]
	#vals_i = floydSteinberg(vals_c)
	saveIndexed(file+'-bw',indexes)

#	def clip(value): return -.05 if value < -.05 else .05 if value > .05 else value

#	pal = [bit(cie.xyz(c)) for c in palrgb]
#	vals_c = [[bit(cie.xyz(c)) for c in row] for row in vals]
#	vals_i = floydSteinberg(vals_c)
#	saveIndexed(file+'-xyz',vals_i)

'''
	pal = [cie.lab(cie.xyz(c)) for c in palrgb]
	vals_c = [[cie.lab(cie.xyz(c)) for c in row] for row in vals]
	vals_i = floydSteinberg(vals_c)
	saveIndexed(file+'-lab',vals_i)

	pal = [cie.luv(cie.xyz(c)) for c in palrgb]
	vals_c = [[cie.luv(cie.xyz(c)) for c in row] for row in vals]
	vals_i = floydSteinberg(vals_c)
	saveIndexed(file+'-luv',vals_i)
'''
