import os, png
import cie
os.chdir('/Users/cy4n/Desktop/python/ciedither')

info = {'bitdepth' : 8}
depth = 255.
img = []

space = 'srgb'

def bit(v):
	return min(max(int(v*depth+0.5),0),depth)

def _bit(bit):
	return (
		bit[0]/depth,
		bit[1]/depth,
		bit[2]/depth)

def luma(rgb): return (0.2126*rgb[0]+0.7152*rgb[1]+0.0722*rgb[2])

def load(file,space='srgb'):
	space = space.lower()
	file = open(file+'.png')
	file = png.Reader(file=file).asRGBA()
	global info
	info = file[3]
	img = []
	if space == 'l':
		info['greyscale'] = True
		for row in file[2]:
			r = []
			for i in xrange(info['size'][0]):
				r.append(luma(_bit((row[4*i],row[4*i+1],row[4*i+2]))))

			img.append(r)

	elif space == 'srgb':
		for row in file[2]:
			r = []
			for i in xrange(info['size'][0]):
				r.append(_bit((row[4*i],row[4*i+1],row[4*i+2])))

			img.append(r)

	elif space == 'xyz':
		for row in file[2]:
			r = []
			for i in xrange(info['size'][0]):
				r.append(cie.xyz(_bit((row[4*i],row[4*i+1],row[4*i+2]))))

			img.append(r)

	elif space == 'uvw':
		for row in file[2]:
			r = []
			for i in xrange(info['size'][0]):
				r.append(cie.uvw(cie.xyz(_bit((row[4*i],row[4*i+1],row[4*i+2])))))

			img.append(r)

	elif space == 'luv':
		for row in file[2]:
			r = []
			for i in xrange(info['size'][0]):
				r.append(cie.luv(cie.xyz(_bit((row[4*i],row[4*i+1],row[4*i+2])))))

			img.append(r)

	elif space == 'lab':
		for row in file[2]:
			r = []
			for i in xrange(info['size'][0]):
				r.append(cie.lab(cie.xyz(_bit((row[4*i],row[4*i+1],row[4*i+2])))))

			img.append(r)

	return img



def save(file,vals):
	file = open(file+'.png', 'wb')
	exp = []
	if space == 'l':
		for row in vals:
			r = []
			for val in row:
				r.append(bit(val))

			exp.append(r)

	elif space == 'srgb':
		for row in vals:
			r = []
			for pix in row:
				r.append(bit(pix[0]));r.append(bit(pix[1]));r.append(bit(pix[2]))

			exp.append(r)

	elif space == 'xyz':
		for row in vals:
			r = []
			for pix in row:
				pix = cie.rgb(pix)
				r.append(bit(pix[0]));r.append(bit(pix[1]));r.append(bit(pix[2]))
				print bit(pix[0])

			exp.append(r)

	elif space == 'uvw':
		for row in vals:
			r = []
			for pix in row:
				pix = cie.rgb(cie._uvw(pix))
				r.append(bit(pix[0]));r.append(bit(pix[1]));r.append(bit(pix[2]))
				print bit(pix[0])

			exp.append(r)

	elif space == 'luv':
		for row in vals:
			r = []
			for pix in row:
				pix = cie.rgb(cie._luv(pix))
				r.append(bit(pix[0]));r.append(bit(pix[1]));r.append(bit(pix[2]))
				print bit(pix[0])

			exp.append(r)

	elif space == 'lab':
		for row in vals:
			r = []
			for pix in row:
				pix = cie.rgb(cie._lab(pix))
				r.append(bit(pix[0]));r.append(bit(pix[1]));r.append(bit(pix[2]))
				print bit(pix[0])

			exp.append(r)

	png.Writer(info['size'][0],
	info['size'][1],
	greyscale = space=='l',
	alpha = False,
	bitdepth = info['bitdepth']).write(file, exp)

def luminance(img):
	global space
	if space == 'srgb':
		for i in xrange(info['size'][1]):
			for ii in xrange(info['size'][0]):
				img[i][ii] = luma(img[i][ii])

	elif space == 'xyz':
		for i in xrange(info['size'][1]):
			for ii in xrange(info['size'][0]):
				img[i][ii] = img[i][ii][1]

	elif space == 'uvw':
		for i in xrange(info['size'][1]):
			for ii in xrange(info['size'][0]):
				img[i][ii] = (img[i][ii][2]+17)/25.

	elif space == 'luv' or space == 'lab':
		for i in xrange(info['size'][1]):
			for ii in xrange(info['size'][0]):
				img[i][ii] = img[i][ii][0]/100.

	space = 'l'
