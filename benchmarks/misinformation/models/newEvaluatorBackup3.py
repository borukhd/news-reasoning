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


def sequencesPerPerson(source):
    sequencesPerPers = {}
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
        if item.identifier not in sequencesPerPers.keys():
            sequencesPerPers[item.identifier] = {}
        if item.sequence_number not in sequencesPerPers[item.identifier].keys():
            sequencesPerPers[item.identifier][item.sequence_number] = item
    return sequencesPerPers


def itemsList(source):
    itemsList = []
    linecount = 0
    indcount = 0
    line1 = True
    lines = open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/'+source+'.csv')
    ind = {}
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

        itemsList.append(Item(
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
        ))
    return itemsList

def main():
    allitems = []
    for source in sources:
        allitems.extend(itemsList(source))
    print(personPerformance(allitems, []))
    print('done')


def itemsPeformance(items, pars, predicS = False):
    #input: list of items
    items = [a for a in items]
    performance = []
    sequencesPerPers = {}
    for item in items:
        if item.identifier not in sequencesPerPers.keys():
            sequencesPerPers[item.identifier] = {}
        if item.sequence_number not in sequencesPerPers[item.identifier].keys():
            sequencesPerPers[item.identifier][item.sequence_number] = item
    for person in sequencesPerPers.keys():
        ms = [model(commands=pars) for model in models]
        for seq in sorted([a for a in sequencesPerPers[person].keys()]):
            item = sequencesPerPers[person][seq]
            for m in ms:
                if not predicS:
                    prediction = 'Accept' == m.predict(item)
                else:
                    prediction = m.predicS(item)
                trialperformance = prediction if item.birep else 1-prediction
                performance.append(trialperformance)
    return sum(performance)/len(performance)

def itemsModelPeformance(items, pars, predicS = False):
    #input: list of items
    items = [a for a in items]
    modelPerformance = {}
    for m in models:
        modelPerformance[m().name] = []
    sequencesPerPers = {}
    for item in items:
        if item.identifier not in sequencesPerPers.keys():
            sequencesPerPers[item.identifier] = {}
        if item.sequence_number not in sequencesPerPers[item.identifier].keys():
            sequencesPerPers[item.identifier][item.sequence_number] = item
    for person in sequencesPerPers.keys():
        ms = [model(commands=pars) for model in models]
        for seq in sorted([int(a) for a in sequencesPerPers[person].keys()]):
            item = sequencesPerPers[person][str(seq)]
            for m in ms:
                if not predicS:
                    prediction = 'Accept' == m.predict(item)
                else:
                    prediction = m.predicS(item)
                trialperformance = prediction if item.birep else 1-prediction
                modelPerformance[m.name].append(trialperformance)
    return {m().name : sum(modelPerformance[m().name])/len(modelPerformance[m().name]) for m in models}


def personPerformance(items, pars):
    perfPerPers = {}
    itemsPerPers = {}
    for item in items:
        if item.identifier not in itemsPerPers.keys():
            itemsPerPers[item.identifier] = []
        itemsPerPers[item.identifier].append(item)
    for pers in itemsPerPers:
        perfPerPers[pers] = itemsModelPeformance(itemsPerPers[pers],pars)
    return perfPerPers
                

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
    results = {}
    for source in sources:
        results[source] = iterate(source)
        dec, probs = results[source]
        dolist = []
        if 'prob' in input:
            dolist.append(dec)
        if 'decs' in input:
            dolist.append(probs)
        for l in dolist:
            for m in l.keys():
                for pair in l[m]:
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
