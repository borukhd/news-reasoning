from MotivatedReasoning.s2mr import S2MR
from MotivatedReasoning.s2mrcr import S2MRCR
from ClassicalReasoning.cr import CR
from ClassicalReasoning.cr_recog import CRrecog
from Baseline.rand import BaselineRandom
from Baseline.corr import CorrectReply
from New.lc import LC
from New.lc_byParty import LCparty
from New.lp import LP
from New.fft import FFT
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
import statistics as stats
import time


models = [CR]#CRrecog,S2MR, CorrectReply, BaselineRandom,LP,FFT,LCparty]

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

currentmax = {}
currentmaxpers = {}

def main():
    allitems = []
    for source in sources:
        allitems.extend(itemsList(source))
    #print(personPerformance(allitems, []))
    pool = Pool(4)
    pool.map(doModel, [(model, allitems) for model in models if not "nandom" in model().name])
    print('done')


def doModel(args):
    model, allitems = args
    try:
        model().trainModel(allitems)
        print(model().name, 'trained.')
    except:
        pass
    currentmax[model().name] = 0
    print(model().name,':')
    if len(model().parameter.keys()) > 0:
        personOptimum = basinhopping(minimized, [0]*len(model().parameter.keys()),niter=120, stepsize=3.0, T=0.8, minimizer_kwargs={"args" : (model, allitems)},disp=False)
        print(model().name, '  Optimized globally:  ', -1*minimized(personOptimum.x, model, allitems), personOptimum.x)
        perf2d, corr2d, tend2d, pars =itemsOptimizedOneModelPeformance(model, allitems)
        perf = [item for sublist in perf2d for item in sublist]
        corr = [item for sublist in corr2d for item in sublist]
        tend = [item for sublist in tend2d for item in sublist]
        print(model().name, '  Optimized per person:', 
            stats.mean(perf), stats.stdev(perf), stats.mean(corr), stats.stdev(corr), stats.mean(tend), stats.stdev(tend), 
            [(stats.mean([pars[key][a] for key in pars.keys()]),stats.stdev([pars[key][a] for key in pars.keys()])) for a in range(len([pars[[a for a in pars.keys()][0]]]))])
    else:
        print(model().name, '  Non Optimizable:     ', -1*minimized([], model, allitems))

def minimized(pars, model, items):
    optCommands = []
    i = 0
    parKeys = sorted(model().parameter.keys())
    for a in parKeys:
        if len(pars)<=i: 
            break
        optCommands.append('self.parameter[\'' + a + '\'] = ' + str(pars[parKeys.index(a)]))
        i += 1
    return round(-1*itemsOneModelPeformance(optCommands, model, items),100)

def minimizedOnePerson(pars, model, person, items):
    optCommands = toCommandList(pars, model)
    perf, corr, tend = itemsOnePersonOneModelPeformance(optCommands, model, person, items)
    return round(-1*sum(perf)/len(perf),100)

def toCommandList(pars, model):
    optCommands = []
    i = 0
    parKeys = sorted(model().parameter.keys())
    for a in parKeys:
        if len(pars)<=i: 
            print('keys length error', model)
            break
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
    modelTendency = []
    modelPerformance = []
    modelCorrectness = []
    sequencesPerPers = {}
    for item in items:
        if item.identifier not in sequencesPerPers.keys():
            sequencesPerPers[item.identifier] = {}
        if item.sequence_number not in sequencesPerPers[item.identifier].keys():
            sequencesPerPers[item.identifier][item.sequence_number] = item
    for person in sequencesPerPers.keys():
        performanceOfPerson= []
        m = model(commands=pars)
        for seq in sorted([int(a) for a in sequencesPerPers[person].keys()]):
            item = sequencesPerPers[person][str(seq)]
            if not predicS:
                predictionPerf = (item.response == m.predict(item))
            else:
                pred = min(1.0,max(m.predictS(item),0.0)) 
                if item.birep:
                    predictionPerf = min(1.0,max(m.predictS(item),0.0)) 
                elif not item.birep:
                    predictionPerf = 1.0 - pred
                else:
                    print('Error')
            modelTendency.append(pred)
            modelCorrectness.append(pred if item.truthful else 1-pred)
            trialperformance = predictionPerf #if item.birep else 1-prediction
            performanceOfPerson.append(trialperformance)
        modelPerformance.extend(performanceOfPerson)
    if sum(modelPerformance)/len(modelPerformance)> currentmax[model().name]:
        print('currentmax', model().name ,sum(modelPerformance)/len(modelPerformance), 'tendency:', sum(modelTendency)/len(modelTendency), 'correctness:', sum(modelCorrectness)/len(modelCorrectness), model(commands=pars).parameter)
        currentmax[model().name] = sum(modelPerformance)/len(modelPerformance)
    return sum(modelPerformance)/len(modelPerformance)

def itemsOptimizedOneModelPeformance(model, items, predicS = True, atMostPeople = -1):
    #input: list of items
    peopleCounter = 0
    totalPerformances = []
    items = [a for a in items]
    performanceOfPerson = {}
    correctnessOfPerson = {}
    tendencyOfPerson = {}
    sequencesPerPers = {}
    parametersOfPerson = {}
    for item in items:
        if item.identifier not in sequencesPerPers.keys():
            sequencesPerPers[item.identifier] = []
        sequencesPerPers[item.identifier].append(item)
    people = [a for a in sequencesPerPers.keys()]
    for person in people:
        personOptimum = basinhopping(minimizedOnePerson, [0]*len(model().parameter.keys()),niter=120, stepsize=3.0, T=0.8, minimizer_kwargs={"args" : (model, person, sequencesPerPers[person])})
        """
        minimize(minimizedOnePerson,[2]*len(model().parameter.keys()), method='COBYLA',
                options={'maxiter' : 200, 'tol' : 0.01}, args = (model, person, sequencesPerPers[person]))
        """
        perf, corr, tend = itemsOnePersonOneModelPeformance(toCommandList(personOptimum.x, model), model, person, sequencesPerPers[person])
        performanceOfPerson[person] = perf
        correctnessOfPerson[person] = corr
        tendencyOfPerson[person] = tend
        parametersOfPerson[person] = personOptimum.x
        if atMostPeople > peopleCounter and atMostPeople > 0:
            peopleCounter +=1
        if atMostPeople <= peopleCounter:
            break
    return performanceOfPerson.values(), correctnessOfPerson.values(), tendencyOfPerson.values(), parametersOfPerson


def seqnum(item):
    return int(item.sequence_number)

def itemsOnePersonOneModelPeformance(pars, model, person, items, predicS = True):
    #input: list of items
    items = [a for a in items]
    modelTendency = []
    modelCorrectness = []
    performanceOfPerson = []
    m = model(commands=pars)
    for item in sorted(items, key=seqnum):
        if item.identifier != person:
            print('Error')
            RuntimeError
        if not predicS:
            predictionPerf = float(item.response == m.predict(item))
        else:
            pred = min(1.0,max(m.predictS(item),0.0)) 
            if item.birep:
                predictionPerf = min(1.0,max(m.predictS(item),0.0)) 
            elif not item.birep:
                predictionPerf = 1.0 - pred
            else:
                print('Error')
        modelTendency.append(pred)
        modelCorrectness.append(pred if item.truthful else 1-pred)
        performanceOfPerson.append(predictionPerf)
    if model().name + person not in currentmaxpers.keys() or sum(performanceOfPerson)/len(performanceOfPerson)> currentmaxpers[model().name + person]:
        #print('currentmaxpers', model().name, person ,sum(performanceOfPerson)/len(performanceOfPerson), 'tendency:', sum(modelTendency)/len(modelTendency), 'correctness:', sum(modelCorrectness)/len(modelCorrectness), model(commands=pars).parameter)
        currentmaxpers[model().name + person] = sum(performanceOfPerson)/len(performanceOfPerson)
    return performanceOfPerson, modelCorrectness, modelTendency
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
                

def stopwatch(seconds):
    start = time.time()
    print(start)
    elapsed = 0
    while seconds< 0 or elapsed < seconds:
        time.sleep(1)
        print()


if __name__ == '__main__':
    start = time.time()
    main()
    print('Time for calculation:', round(time.time()-start,1))

