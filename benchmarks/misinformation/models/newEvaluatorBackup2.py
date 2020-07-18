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
                prediction = int('Accept' in model.predict(item))
                predictionProb = min(1.0, max(0.0,float(model.predictS(item))))
                if item.birep:
                    predictionProb = predictionProb
                if not item.birep:
                    predictionProb = 1 - predictionProb
                modelpredictions[model.name].append([prediction, item])
                modelpredictionProbs[model.name].append([predictionProb, item])
        return modelpredictions, modelpredictionProbs

def main():
    dec, prob = createDictData('probs,decs')
    print('done')



def createDictData(input):
    data = {}
    dataDec = {}
    dict_data = []
    dec_dict_data = []
    categorical = ['model','c', 'l', 'binaryResponse', 'truthful','person','sequence','source']
    numerical = ['predprob', 'crt', 'conserv']
    for key in categorical + numerical:
        data[key] = []
        dataDec[key] = []
    ev= Evaluator()
    results = {}
    for source in sources:
        results[source] = ev.iterate(source)
        dec, probs = results[source]
        if 'prob' in input:
            for m in probs.keys():
                for pair in probs[m]:
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
                    data['source'].append(source)
                    itemDict = {}
                    for a in categorical + numerical:
                        itemDict[a] = data[a][-1]
                    dict_data.append(itemDict)
        
        if 'decs' in input:
            for m in dec.keys():
                for pair in dec[m]:
                    p, item = pair
                    dataDec['person'].append(item.identifier)
                    dataDec['crt'].append(item.crt)
                    dataDec['conserv'].append(item.cons)
                    dataDec['c'].append(item.consNews)
                    dataDec['l'].append(item.libeNews)
                    dataDec['predprob'].append(p)
                    dataDec['binaryResponse'].append(item.birep)
                    dataDec['model'].append(m)
                    dataDec['truthful'].append(item.truthful)
                    dataDec['sequence'].append(item.sequence_number)
                    dataDec['source'].append(source)
                    itemDict = {}
                    for a in categorical + numerical:
                        itemDict[a] = dataDec[a][-1]
                    dec_dict_data.append(itemDict)
    return dict_data, dec_dict_data

def writetocsv(data):
    csv_columns = [a for a in data.keys()]
    try:
        with open('tempSave.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for dataRow in dict_data:
                writer.writerow(dataRow)
    except IOError:
        print("I/O error")
    print('TempSave written')


if __name__ == '__main__':
    main()
