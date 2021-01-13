import os, png, math
import cie
os.chdir('/Users/cy4n/Desktop/python/ciedither')

info = {}
depth = 255.
img = []

def bit(v):
	return int(min(max(v,0),1)*depth+0.5)

def _bit(bit):
	return (
		bit[0]/depth,
		bit[1]/depth,
		bit[2]/depth)

def luma(rgb): return (0.2126*rgb[0]+0.7152*rgb[1]+0.0722*rgb[2])

def load(file,greyscale=False):
	print 'loading'
	file = png.Reader(file=open(file+'.png')).asRGBA()
	global info
	info = file[3]
	img = []
	if greyscale:
		info['greyscale'] = True
		for row in file[2]:
			r = []
			for i in xrange(info['size'][0]):
				r.append(luma(_bit((row[4*i],row[4*i+1],row[4*i+2]))))

			img.append(r)

		return img

	for row in file[2]:
		r = []
		for i in xrange(info['size'][0]):
			r.append(_bit((row[4*i],row[4*i+1],row[4*i+2])))

		img.append(r)

	print 'processing'
	return img

def colors2rgb(row):
	n = []
	for i in row:
		n.append(i[0])
		n.append(i[1])
		n.append(i[2])
	return n
'''

def load(file,greyscale=False):
	print 'loading'
	file = png.Reader(file=open(file+'.png')).asRGBA()
	global info
	info = file[3]
	img = []
	for row in file[2]:
		r = []
		i = 0
		while i < 4 * info['size'][0]:
			r.append(row[i]/255.)
			r.append(row[i+1]/255.)
			r.append(row[i+2]/255.)
			i += 4

		img.append(r)

	return img
'''
def save(file,vals,depth=3):
	print 'saving'
	file = open(file+'.png', 'wb')
	if info['greyscale']:
		info['bitdepth'] = math.log(depth+1,2)
		exp = []
		for row in vals:
			r = []
			for v in row:
				r.append(int(min(max(v,0),1)*depth+0.5))
			exp.append(r)

	else:
		exp = []
		for row in vals:
			r = []
			for pix in row:
				r.append(bit(pix[0]));r.append(bit(pix[1]));r.append(bit(pix[2]))

			exp.append(r)

	png.Writer(
	info['size'][0],
	info['size'][1],
	greyscale = info['greyscale'],
	alpha = False,
	bitdepth = info['bitdepth']
	).write(file, exp)
