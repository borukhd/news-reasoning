from MotivatedReasoning.s2mr import S2MR
from MotivatedReasoning.s2mrcr import S2MRCR
from ClassicalReasoning.cr import CR
from Baseline.rand import BaselineRandom
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




models = [S2MR, CR, S2MRCR, BaselineRandom]

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

def minimized(pars, items):
    return -1*itemsPerformance(items, pars)


def itemsPerformance(items, pars, predicS = False):
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

def itemsOneModelPeformance(pars, model, items, predicS = False):
    #input: list of items
    items = [a for a in items]
    modelPerformance = []
    for m in models:
        modelPerformance[m().name] = []
    sequencesPerPers = {}
    for item in items:
        if item.identifier not in sequencesPerPers.keys():
            sequencesPerPers[item.identifier] = {}
        if item.sequence_number not in sequencesPerPers[item.identifier].keys():
            sequencesPerPers[item.identifier][item.sequence_number] = item
    for person in sequencesPerPers.keys():
        m = model(commands=pars)
        for seq in sorted([int(a) for a in sequencesPerPers[person].keys()]):
            item = sequencesPerPers[person][str(seq)]
            if not predicS:
                prediction = 'Accept' == m.predict(item)
            else:
                prediction = m.predicS(item)
            trialperformance = prediction if item.birep else 1-prediction
            modelPerformance.append(trialperformance)
    return sum(modelPerformance)/len(modelPerformance)



    parOpt = minimize(minimized,[0.5]*len(modelParameters[model]), method='cobyla', options={'maxiter' : 20, 'tol' : 0.001}, 
        args = (allitems))#, bounds = modelBounds[model])
    print(parOpt)

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
                

if __name__ == '__main__':
    main()
