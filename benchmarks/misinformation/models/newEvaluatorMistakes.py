from MotivatedReasoning.s2mr import S2MR
from MotivatedReasoning.s2mrcr import S2MRCR
from ClassicalReasoning.cr import CR
from Baseline.rand import BaselineRandom
from Baseline.corr import CorrectReply
from New.lc import LC
from New.lc_byParty import LCparty
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




models = [LCparty,LC]#, CR, S2MR, S2MRCR, BaselineRandom, CorrectReply]

sources = ['st1ext']
sources = ['Study1dataReshaped']

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
        if listLine[ind['_accurate']] == '':
            continue
        
        crtresults = []
        itemComponents = {}
        for item in ind.keys():
            if item in ['Exciting_Democrats_Combined', 'Exciting_Republicans_Combined', 'Familiarity_Democrats_Combined', 'Familiarity_Republicans_Combined', 'Importance_Democrats_Combined', 'Importance_Republicans_Combined', 'Likelihood_Democrats_Combined', 'Likelihood_Republicans_Combined', 'Partisanship_All_Combined', 'Partisanship_All_Partisan', 'Partisanship_Democrats_Combined', 'Partisanship_Republicans_Combined', 'Sharing_Democrats_Combined', 'Sharing_Republicans_Combined', 'Worrying_Democrats_Combined', 'Worrying_Republicans_Combined']:
                itemComponents[item] = float(listLine[ind[item]])
            if 'CRT1' in item or 'CRT3' in item:
                crtresults.append(float(listLine[ind[item]] in item.split('_')[1].split(':')[1:]))
        crt = sum(crtresults)/len(crtresults)
        if '' == listLine[ind['DemRep_C_current']]:
            continue

        itemsList.append(Item(
            listLine[ind['id']], listLine[ind['domain']],
            listLine[ind['task']], listLine[ind['response_type']],
            listLine[ind['choices']], listLine[ind['sequence']], 
            float(crt), 
            float(listLine[ind['DemRep_C_current']]), 
            bool(int(listLine[ind['truthful']])), 
            bool(int(listLine[ind['_accurate']])), 
            bool(int(listLine[ind['_C']])), 
            bool(int(listLine[ind['_L']])),
            bool(int(listLine[ind['_N']])),  
            bool(int(listLine[ind['binaryResponse']])),
            int(listLine[ind['POTUS2016_Who did yo']]),
            str(listLine[ind['response']]),
            itemComponents,
            {}#allfeatures
        ))
    return itemsList

def main():
    allitems = []
    for source in sources:
        allitems.extend(itemsList(source))
    allitems = [a for a in allitems if (a.birep == 0 if a.truthful else 1)]
    #print(personPerformance(allitems, []))
    for model in models:
        if model == BaselineRandom:
            continue
        print(model().name,':')

        personOptimum = minimize(minimized,[1]*len(model().parameter.keys()), method='COBYLA',#'Nelder-Mead', #
                options={'maxiter' : 200, 'tol' : 0.01, 'adaptive' : True}, #'rhobeg' : 5.9},
                    args = (model, allitems))
        print('  Optimized globally:  ', -1*personOptimum.fun, [round(a,5) for a in personOptimum.x])
        print('  Optimized per person:', -1*itemsOptimizedOneModelPeformance(model, allitems))
        #break
    print('done')

def minimized(pars, model, items):
    optCommands = []
    i = 0
    for a in model().parameter.keys():
        optCommands.append('self.parameter[\'' + a + '\'] = ' + str(pars[i]))
        i += 1
    return round(-1*itemsOneModelPeformance(optCommands, model, items),100)

def minimizedOnePerson(pars, model, person, items):
    optCommands = []
    i = 0
    for a in model().parameter.keys():
        optCommands.append('self.parameter[\'' + a + '\'] = ' + str(pars[i]))
        i += 1
    return round(-1*itemsOnePersonOneModelPeformance(optCommands, model, person, items),100)


def minimizedOneModelPerPerson(pars, model, person, items):
    optCommands = toCommandList(pars, model)
    return round(-1*itemsOptimizedOneModelPeformance(optCommands, model, person, items),100)

def toCommandList(pars, model):
    optCommands = []
    i = 0
    for a in model().parameter.keys():
        optCommands.append('self.parameter[\'' + a + '\'] = ' + str(pars[i]))
        i += 1
    return optCommands

def itemsPerformance(items, pars, predicS = True):
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
        performanceOfPerson = []
        ms = [model(commands=pars) for model in models]
        for seq in sorted([a for a in sequencesPerPers[person].keys()]):
            item = sequencesPerPers[person][seq]
            for m in ms:
                if not predicS:
                    prediction = item.response == m.predict(item)
                else:
                    prediction = m.predicS(item)
                trialperformance = prediction if item.birep else 1-prediction
                performanceOfPerson.append(trialperformance)
        performance.extend(trialperformance)
        #print(sum(performanceOfPerson)/len(performanceOfPerson))
    return sum(performance)/len(performance)

def itemsModelPeformance(items, pars, predicS = True):
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
                    print(item.response == m.predict(item),item.response, m.predict(item))
                    prediction = item.response == m.predict(item)
                else:
                    prediction = m.predictS(item)
                trialperformance = prediction if item.birep else 1-prediction
                modelPerformance[m.name].append(trialperformance)
    return {m().name : sum(modelPerformance[m().name])/len(modelPerformance[m().name]) for m in models}

def itemsOneModelPeformance(pars, model, items, predicS = True):
    #input: list of items
    items = [a for a in items]
    modelPerformance = []
    sequencesPerPers = {}
    for item in items:
        if item.identifier not in sequencesPerPers.keys():
            sequencesPerPers[item.identifier] = {}
        if item.sequence_number not in sequencesPerPers[item.identifier].keys():
            sequencesPerPers[item.identifier][item.sequence_number] = item
    for person in sequencesPerPers.keys():
        performanceOfPerson= []
        m = model(commands=pars)
        #print(pars)
        #print(m.parameter)
        for seq in sorted([int(a) for a in sequencesPerPers[person].keys()]):
            item = sequencesPerPers[person][str(seq)]
            if not predicS:
                prediction = (item.response == m.predict(item))
            else:
                if item.birep:
                    prediction = min(1.0,max(m.predictS(item),0.0)) 
                elif not item.birep:
                    prediction = 1.0 - min(1.0,max(m.predictS(item),0.0)) 
                else:
                    print('Error')
            trialperformance = prediction #if item.birep else 1-prediction
            performanceOfPerson.append(trialperformance)
        modelPerformance.extend(performanceOfPerson)
        #print(sum(performanceOfPerson)/len(performanceOfPerson))
    print('onemodel',sum(modelPerformance)/len(modelPerformance))
    return sum(modelPerformance)/len(modelPerformance)

def itemsOptimizedOneModelPeformance(model, items, predicS = True):
    #input: list of items
    totalPerformances = 0
    items = [a for a in items]
    performanceOfPerson = {}
    sequencesPerPers = {}
    for item in items:
        if item.identifier not in sequencesPerPers.keys():
            sequencesPerPers[item.identifier] = []
        sequencesPerPers[item.identifier].append(item)
    people = [a for a in sequencesPerPers.keys()]
    for person in people:
        personOptimum = minimize(minimizedOnePerson,[2]*len(model().parameter.keys()), method='COBYLA',
                options={'maxiter' : 200, 'tol' : 0.01}, args = (model, person, sequencesPerPers[person]))
        performanceOfPerson[person] = personOptimum.x
        comment = toCommandList(performanceOfPerson[person],model)
        #print([a.split('\'')[1] + ': ' + str(round(float(a.split('= ')[1]),3)) for a in comment], person, -1*round(float(personOptimum.fun),3))
        totalPerformances += personOptimum.fun
    #print('onemodel',totalPerformances/len(people))
    return totalPerformances/len(people)


def seqnum(item):
    return int(item.sequence_number)

def itemsOnePersonOneModelPeformance(pars, model, person, items, predicS = True):
    #input: list of items
    items = [a for a in items]
    performanceOfPerson = []
    m = model(commands=pars)
    for item in sorted(items, key=seqnum):
        if item.identifier != person:
            print('Error')
            RuntimeError
        if not predicS:
            prediction = float(item.response == m.predict(item))
        else:
            if item.birep:
                prediction = min(1.0,max(m.predictS(item),0.0)) 
            elif not item.birep:
                prediction = 1-min(1.0,max(m.predictS(item),0.0)) 
            else:
                print('Error')
        trialperformance = prediction #if item.birep else 1-prediction
        performanceOfPerson.append(trialperformance)
    return sum(performanceOfPerson)/len(performanceOfPerson) 



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


