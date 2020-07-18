import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as sns
import pandas as pd

input = '/home/hippo/git/news-reasoning/benchmarks/misinformation/data/st1ext.csv'

lines = open(input, 'r')
X = []
y = []
count = 0
keys = []
ind = {}
linecount = 0
line1 = True


data = {}
data['crt'] = []
data['conserv'] = []
data['c'] = []
data['l'] = []
data['truthful'] = []
data['binaryResponse'] = []

fig = plt.figure()
ax1 = fig.add_subplot(111)

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
    i = [listLine[ind['CRT']],listLine[ind['binaryResponse']],listLine[ind['truthful']]]
    if ' ' in i: 
        continue
    i = [float(a) for a in i]
    if not (float(listLine[ind['Conserv']]) > 2.5 and int(listLine[ind['_C']])):
        continue
    data['crt'].append(float(listLine[ind['CRT']]))
    data['conserv'].append(float(listLine[ind['Conserv']]))
    data['c'].append(float(listLine[ind['_C']]))
    data['l'].append(float(listLine[ind['_L']]))
    data['truthful'].append(float(listLine[ind['truthful']]))
    data['binaryResponse'].append(float(listLine[ind['binaryResponse']]))

    newItem = 0.0 if int(i[1]) > 2 else 1.0
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
        print(linecount)
categorical = [
  'conserv','c','l','truthful','binaryResponse'
]

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
y2 = [avgPerfPerCRTfake[a] for a in xf]
#y3 = [(0.33 - 0.2*a) for a in range(10)]
#y4 = [(0.74 + 0.1*a) for a in range(10)]
y3 = [(0.3 - 0.2*a) for a in range(10)]
y4 = [(0.55 + 0.1*a) for a in range(10)]
ax1.set(xlim=(0, 1), ylim=(0,1), xlabel='CRT', ylabel='expected response')

ax1.scatter(xr, y1, color='r', label = 'real')
ax1.scatter(xf, y2, color='b', label = 'fake')
ax1.plot([a for a in range(10)], y3, color='b')
ax1.plot([a for a in range(10)], y4, color='r')


ax1.legend()

plt.show()
sns.set(style='whitegrid', palette="deep", font_scale=1.1, rc={"figure.figsize": [8, 5]})

#print(data)
df = pd.DataFrame(data)
print(df)
#fig, ax = plt.subplots(3, 3, figsize=(15, 10))
#for var, subplot in zip(categorical, ax.flatten()):
#    sns.boxplot(x=var, y='crt', data=data, ax=subplot)
#sns.plt.show()
#plt.show()
