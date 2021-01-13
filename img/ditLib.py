import png
from sys import stdout
from time import time
from timeit import timeit
from os import chdir
chdir('/Users/cy4n/Desktop/python/img')

def prnt(s): stdout.write(s); stdout.flush()

def lin(v): return (v/269.025+0.0521327014218008)**2.4 if v>10 else v/3294.6
def gam(v): return 1.055*v**0.41666666666-0.055 if v>0.0031308 else v*12.92

tup = tuple([lin(float(i)/(2**4)*255) for i in range(2**4+1)][1:-1])

def c1(v): return 1 if v>0.21404114048223158 else 0

def c2(v):
	if v>0.21404114048223158:
		if v>0.5225215539683904: return 3
		return 2
	if v>0.050876088171556415: return 1
	return 0

def c3(v):
	if v>0.21404114048223158:
		if v>0.5225215539683904:
			if v > 0.7388447188680376: return 7
			return 6
		if v > 0.34851019523974996: return 5
		return 4
	if v>0.050876088171556415:
		if v > 0.11601613423276537: return 3
		return 2
	if v > 0.014349874706802372: return 1
	return 0

def c4(v):
	if v>0.21404114048223233:
		if v>0.5225215539683916:
			if v>0.7388447188680392:
				if v>0.863669004659515:return 15
				return 14
			if v>0.6252315100117787: return 13
			return 12
		if v>0.34851019523975096:
			if v>0.4303933932276219: return 11
			return 10
		if v>0.276517616996: return 9
		return 8
	if v>0.0508760881716:
		if v>0.116016134233:
			if v>0.160682677718: return 7
			return 6
		if v>0.0795814267681: return 5
		return 4
	if v>0.0143498747068:
		if v>0.0293428490813: return 3
		return 2
	if v>0.00515566839903: return 1
	return 0

def cList(v):
	dists = [abs(v-i) for i in tup]
	return dists.index(min(dists))
