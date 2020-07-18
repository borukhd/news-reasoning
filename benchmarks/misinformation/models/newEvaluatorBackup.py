from MotivatedReasoning.s2mr import S2MR
from MotivatedReasoning.s2mrcr import S2MRCR
from ClassicalReasoning.cr import CR
from ccobra import Item
import pandas as pd
from scipy.optimize import *
import os
from multiprocessing import Pool
import time
import warnings
from matplotlib import pyplot as plt
import seaborn as sns
import csv




models = [S2MR, CR, S2MRCR]

sources = ['st1ext']

modelParameters = {
    S2MR : ['Dcons', 'Dlib', 'Kc' , 'Kl', 'Mc', 'Ml'],#, 'vInit'],
    CR : ['Cr', 'Cf', 'Mr','Mf'],#, 'vInit'],
    S2MRCR : ['Dcons', 'Dlib', 'Kc' , 'Kl', 'Mc', 'Ml', 'Cr', 'Cf', 'Mr','Mf']  
    }
"""
modelBounds = {
    RLELO : [[0,50], [0,50]],#, [0,50]],
    RLELO_F : [[0,50], [0,50], [0,50]],#, [0,50]],
    SiemannDelius : [[0,50], [0,50], [0,50]],#, [0,50], [0,50]],
    RWBS :  [[0,50], [0,50]],#, [0,50]],
    RWWy :  [[0,50], [0,50]],#, [0,50]],
    CCW :  [[0,50], [0,50], [0,50]],#, [0,50]],
    VTTBS : [[0,50], [0,50], [0,50]],#, [0,50]],
    BushMosteller : [[0,50]],#, [0,50]]
    CorrectReply : [[0,0]],
    RandomModel : [[0,0]],
    Trabasso : [[0,50]],
    DeSoto : [[0,0]],
    SCTinterpr : [[0,0]], 
    SCT : [[0,0]]
    }
    """


class Evaluator():
    totalerer =0
    counterer =0
    def __init__(self):
        pass

    def iterate(self, source):
        person = {}
        linecount = 0
        indcount = 0
        line1 = True
        lines = open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/'+source+'.csv')
        keys = []
        ind = {}
        modelpredictions = {}
        modelpredictionProbs = {}
        for model in models:
            modelpredictions[model().name] = []
        for model in models:
            modelpredictionProbs[model().name] = []
        for line in lines:
            listLine = line.replace('\r','').replace('\n','').split(',')
            if line1:
                line1 = False
                for key in listLine:
                    ind[key] = indcount
                    indcount += 1
                continue
            linecount += 1
            if listLine[ind['_Accurate']] == ' ':
                continue

            item = Item(
                listLine[ind['id']], listLine[ind['domain']],
                listLine[ind['task']], listLine[ind['response_type']],
                listLine[ind['choices']], listLine[ind['sequence']], 
                float(listLine[ind['CRT']]), 
                float(listLine[ind['Conservatism']]), 
                bool(int(listLine[ind['truthful']])), 
                bool(int(listLine[ind['_Accurate']])), 
                bool(int(listLine[ind['_C']])), 
                bool(int(listLine[ind['_L']])),
                bool(int(listLine[ind['_N']])),  
                bool(int(listLine[ind['binaryResponse']])),
                int(listLine[ind['ClintonTrump']]),
                int(listLine[ind['response']]) if not 'e' in listLine[ind['response']] else str(listLine[ind['response']]),
                {}#allfeatures
            )
            if item.identifier not in person.keys():
                person[item.identifier] = [model() for model in models]
            for model in person[item.identifier]:
                #prediction = int('Accept' in model.predict(item))
                predictionProb = min(1.0, max(0.0,float(model.predictS(item))))
                if item.birep:
                    predictionProb = predictionProb
                if not item.birep:
                    predictionProb = 1 - predictionProb


                if 'Classic' in model.name:
                    print(predictionProb,item.response)
                if 'Class' in model.name:# or predictionProb == 0:
                    Evaluator.counterer += predictionProb
                    #print('none', predictionProb, prediction, item.response)
                    Evaluator.totalerer +=1
                
                #modelpredictions[model.name].append([prediction, item])
                modelpredictionProbs[model.name].append([predictionProb, item])
        return modelpredictions, modelpredictionProbs

def main():
    data = {}
    dict_data = []
    categorical = ['model','c', 'l', 'binaryResponse', 'truthful','person','sequence']
    numerical = ['predprob', 'crt', 'conserv']
    for key in categorical + numerical:
        data[key] = []
    ev= Evaluator()
    results = {}
    for source in sources:
        results[source] = ev.iterate(source)
        dec, probs = results[source]
        for m in probs.keys():
            for pair in probs[m]:
                if 'Class' not in m:
                    pass
                    #continue
                p, item = pair
                data['person'].append(item.identifier)
                data['crt'].append(item.crt)
                data['conserv'].append(item.cons)
                data['c'].append(item.consNews)
                data['l'].append(item.libeNews)
                data['predprob'].append(p)
                data['binaryResponse'].append(item.birep)
                data['model'].append(m)
                data['truthful'].append(item.truthful)
                data['sequence'].append(item.sequence_number)
                #print(p, item.birep, p == item.birep)
                itemDict = {}
                for a in categorical + numerical:
                    itemDict[a] = data[a][-1]
                dict_data.append(itemDict)
                if p == 0:
                    pass
                    #print('zero',itemDict)
    
    for a in dict_data:
        if a['model'] == 'ClassicReas':
            print(a)
    good = 0
    total= 0
    for item in dict_data:
        #print(item)
        if 'ClassicReas' != item['model']:
            #print(item['model'])
            continue
        #print('prob',item['binaryResponse'])
        #print(item['predprob'])
        else:
            good += bool(item['predprob'])
            total += 1
    print(good, total, good/total)
    print(Evaluator.counterer, Evaluator.totalerer, Evaluator.counterer/Evaluator.totalerer)

    csv_columns = [a for a in data.keys()]
    try:
        with open('tempSave.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for dataRow in dict_data:
                writer.writerow(dataRow)
    except IOError:
        print("I/O error")

    df = pd.DataFrame(data)
    sns.set(style="whitegrid")
    snsset = pd.read_csv('tempSave.csv')
    print('written')


    for truth in [True, False]:
        #
        break
        fig, ax = plt.subplots(1, 6, figsize=(15, 10))
        for var, subplot in zip(categorical[1:-2]+numerical[1:], ax.flatten()):
            plot = sns.boxplot(x=var, y='predprob', hue='model', #errwidth=5 
                data=snsset[snsset['truthful']==truth], ax=subplot)
            plot.set(ylim=(0, 1))    
        plt.show()

        


if __name__ == '__main__':
    main()
