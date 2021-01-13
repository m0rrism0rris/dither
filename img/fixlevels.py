import os
os.chdir('/Users/cy4n/Desktop/python/img')
lines = [line[:-1] for line in open('levels.txt').readlines()]
#line = lines[0]
flines = []
for line in lines:
	for i in line:
		line = line[1:]
		if i == ':':
			line = [int(i) for i in line.strip().replace(' ','').split(',')]
			flines.append(tuple(line+[sum(line)]))
			#finallines.append(c+[sum(c)])
			break
for i in range(len(flines)):
	flines.append(flines[127-i])
print tuple(flines)
