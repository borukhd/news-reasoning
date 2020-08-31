import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math


input = '/home/hippo/git/news-reasoning/benchmarks/misinformation/data/Study1dataReshaped.csv'

lines = open(input, 'r')
X = []
y = []
count = 0
keys = []
ind = {}
linecount = 0
line1 = True

fig = plt.figure()
ax1 = fig.add_subplot(121)

perfPerCRTreal = {}
perfPerCRTfake = {}
avgPerfPerCRTreal = {}
avgPerfPerCRTfake = {}
for line in lines:
    listLine = line.replace('\r','').replace('\n','').split(',')
    if line1:
        line1 = False
        for key in listLine:
            ind[key] = count
            count += 1
            keys.append([key])
        continue
    linecount += 1
    crtresults = []
    for item in ind.keys():
        if 'CRT1' in item or 'CRT3' in item:
            crtresults.append(float(listLine[ind[item]] in item.split('_')[1].split(':')[1:]))
            #print(float(listLine[ind[item]] in item.split('_')[1].split(':')[1:]), listLine[ind[item]], item.split('_')[1].split(':')[1:])
    crt = sum(crtresults)/len(crtresults)
    i = [listLine[ind['id']], listLine[ind['binaryResponse']],listLine[ind['truthful']]]
    if ' ' in i:
        continue
    i = [int(i[0])]+[float(a) for a in i[1:]]
    newItem = i[1]
    #print(i, newItem)
    if 0 == int(i[2]):
        if i[0] in perfPerCRTfake.keys():
            perfPerCRTfake[i[0]].append(newItem)
        else:
            perfPerCRTfake[i[0]] = [newItem]
    if 1 == int(i[2]):
        if i[0] in perfPerCRTreal.keys():
            perfPerCRTreal[i[0]].append(newItem)
        else:
            perfPerCRTreal[i[0]] = [newItem]
    if linecount % 100 == 0:
        pass
        #print(linecount)

for i0 in perfPerCRTreal.keys():
    avgPerfPerCRTreal[i0] = sum(perfPerCRTreal[i0])/len(perfPerCRTreal[i0]) 
for i0 in perfPerCRTfake.keys():
    avgPerfPerCRTfake[i0] = sum(perfPerCRTfake[i0])/len(perfPerCRTfake[i0]) 
    #ax1.scatter(i0,avgPerfPerCRT[i0],10)#, c='r' if bool(i[0]) else 'b')

xr = []
xf = []
for a in avgPerfPerCRTreal.keys():
    xr.append(a)
for a in avgPerfPerCRTfake.keys():
    xf.append(a)
    
xr = sorted([a for a in xr])
xf = sorted([a for a in xf])
y1 = [avgPerfPerCRTreal[a] for a in xr]
y2 = [1- avgPerfPerCRTfake[a] for a in xf]
ax1.set(xlabel='participants', ylabel='response correctness')
#xlim=(0, 1), ylim=(0,1), 
size = 10
ax1.scatter(xf, y2, color='r',s=size, label = 'fake')
ax1 = fig.add_subplot(122)

xr = sorted([a for a in xr])
xf = sorted([a for a in xf])
y1 = [avgPerfPerCRTreal[a] for a in xr]
y2 = [1- avgPerfPerCRTfake[a] for a in xf]
ax1.scatter(xr, y1, color='b',s=size, label = 'real')
#ax1.legend()
plt.show()