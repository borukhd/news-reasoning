import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from staticCommon import Keys


class CorAnalyzer:
    allmodelsfile = open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/allmodelsStudy1dataReshaped.csv', 'r')



data = pd.read_csv(CorAnalyzer.allmodelsfile)
df = pd.DataFrame(data)
todrop = ['id',"fakenews",'realnews','acc','task','choices','domain','trial','response_type','response','Partisanship_All_Partisan','Partisanship_All_Combined']
drop1 = todrop + ['Exciting_Party_Combined', 'Familiarity_Party_Combined', 'Importance_Party_Combined', 'Partisanship_All_Combined', 'Partisanship_All_Partisan', 'Partisanship_Party_Combined', 'Worrying_Party_Combined', 'negative_emotion', 'fight', 'optimism', 'sexual', 'money', 'aggression', 'affection', 'positive_emotion', 'science', 'law', 'crime']
personoptimizedmodelnames = [a for a in df.columns if 'Glob' in a or 'ent' in a or 'ecomm' in a]
drop1.extend(personoptimizedmodelnames)
df1 = df.drop(columns=[a for a in drop1 if a in df.columns])
drop2 = todrop + ['crt', 'conservatism', 'ct', 'education', 'gender', 'accimp', 'panasPos', 'panasNeg']
drop2.extend(personoptimizedmodelnames)
df2 = df.drop(columns=[a for a in drop2 if a in df.columns])
print(df2.columns)
df1 = df1.reindex(sorted(df1.columns), axis=1)
df2 = df2.reindex(sorted(df2.columns), axis=1)

newcolumns1 = {
    "ct": "Trump or Clinton", 
    "crt": "CRT", 
    "acc" : "response accuracy", 
    "birep" : "participant response",
    "conservatism" : "conservatism",
    "Partisanship_Party_Combined" : "Partisanship"
    }
newcolumns2 = {
    "ct": "Trump or Clinton", 
    "crt": "CRT", 
    "acc" : "response accuracy", 
    "birep" : "participant response",
    "conservatism" : "conservatism",
    "Partisanship_Party_Combined" : "Partisanship"
    }
for a in df1.columns:
    if a in newcolumns1.keys():
        continue
    a1 = a.replace('Fast-Frugal-Tree','FFT')
    a1 = a1.replace('_Party_Combined','')
    a1 = a1.replace('Pers','')
    a1 = a1.replace('Heuristic-','')
    a1 = a1.replace('SuppressionBy','')
    newcolumns1[a] = a1.split('_')[0].split('.')[0].split('with')[-1].replace('Models','')

for a in df2.columns:
    if a in newcolumns2.keys():
        continue
    a1 = a.replace('Fast-Frugal-Tree','FFT')
    a1 = a1.replace('_Party_Combined','')
    a1 = a1.replace('Pers','')
    a1 = a1.replace('Heuristic-','')
    a1 = a1.replace('SuppressionBy','')

    newcolumns2[a] = a1.split('_')[0].split('.')[0].split('with')[-1].replace('Models','')

data1 = df1.rename(columns=newcolumns1)
data2 = df2.rename(columns=newcolumns2)
corr1 = data1.corr()
corr2 = data2.corr()
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(corr1,cmap='coolwarm', vmin=-1, vmax=1)
ticks = np.arange(0,len(data1.columns),1)
ax.set_xticks(ticks)
fig.colorbar(cax)
plt.xticks(rotation=90)
ax.set_yticks(ticks)
ax.set_xticklabels(data1.columns)
ax.set_yticklabels(data1.columns)
plt.show()
fig = plt.figure()

ax = fig.add_subplot(111)
cax = ax.matshow(corr2,cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,len(data2.columns),1)
ax.set_xticks(ticks)
plt.xticks(rotation=90)
ax.set_yticks(ticks)
ax.set_xticklabels(data2.columns)
ax.set_yticklabels(data2.columns)
plt.show()
