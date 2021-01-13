from ditLib import *
import sys

if __name__ == "__main__":
    args = sys.argv[1:]

if len(args) == 0:
	raise BaseException()

file = args[0]
bit = 1
type = 'color'
dtype = 'sl'
ddtype = True
for arg in args:
	if arg in '12345678': bit = int(arg)
	elif arg in ('grey','color','index'): type = arg
	elif arg.lower() in ('floydsteinberg','fs', 'sierralite','sl', 'burkes','br', 'sierra2','s2', 'jarvis','jv', 'sierra3','s3' ,'stucki','st', 'ostromoukhov','os', 'shiaufan','sf', 'all'):
		dtype = arg.lower()
		ddtype = False

bitd = 2**bit-1
tup = tuple([lin(float(i)/(bitd)*255) for i in range(bitd+1)])
c = cList
if bit == 1: c = c1
if bit == 2: c = c2
if bit == 3: c = c3
if bit == 4: c = c4

if type == 'color':
	import ditRGB
	ditRGB.bit = bit
	ditRGB.bitd = bitd
	ditRGB.c = c
	ditRGB.tup = tup
	load = ditRGB.load; save = ditRGB.save
	floydSteinberg = ditRGB.floydSteinberg; sierraL = ditRGB.sierraL
	burkes = ditRGB.burkes; sierra2 = ditRGB.sierra2
	jarvis = ditRGB.jarvis; sierra3 = ditRGB.sierra3; stucki = ditRGB.stucki

if type == 'grey':
	import ditGrey
	ditGrey.bit = bit
	ditGrey.bitd = bitd
	ditGrey.c = c
	ditGrey.tup = tup
	load = ditGrey.load; save = ditGrey.save
	floydSteinberg = ditGrey.floydSteinberg; sierraL = ditGrey.sierraL
	burkes = ditGrey.burkes; sierra2 = ditGrey.sierra2
	jarvis = ditGrey.jarvis; sierra3 = ditGrey.sierra3; stucki = ditGrey.stucki
	ostromoukhov = ditGrey.ostromoukhov; shiauFan = ditGrey.shiauFan

if dtype in ('floydsteinberg','fs'): dither = floydSteinberg
if dtype in ('sierralite','sl'): dither = sierraL
if dtype in ('burkes','br'): dither = burkes
if dtype in ('sierra2','s2'): dither = sierra2
if dtype in ('jarvis','jv'): dither = jarvis
if dtype in ('sierra3','s3'): dither = sierra3
if dtype in ('stucki','st'): dither = stucki
if dtype in ('ostromoukhov','os'): dither = ostromoukhov
if dtype in ('shiaufan','sf'): dither = shiauFan

#save(file+('' if type == 'color' else '-'+type)+'-'+str(bit)+('' if ddtype else '-'+str(dtype)),dit)

if dtype == 'all':
	dithers = (floydSteinberg,sierraL,burkes,sierra2,jarvis,sierra3,stucki)
	dnames = ('floydSteinberg','sierraLite','burkes','sierra2','jarvis','sierra3','stucki')
	for i in xrange(len(dithers)):
		img = load(file)
		save(dnames[i],dithers[i](img))

else:
    img = load(file)
    dit = dither(img)
    name = 'greatgrey2'
    #for ii in ditGrey.k:
    #    for i in ii:
    #        name += str(i)+' '
    #print name
    save(name,dit)
