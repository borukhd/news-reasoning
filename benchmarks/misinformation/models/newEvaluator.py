from MotivatedReasoning.s2mr import S2MR
from ClassicalReasoning.cr import CR
from Baseline.rand import BaselineRandom
from Baseline.corr import CorrectReply
from New.surp import SURP
from Heuristic.hr import RH
from Heuristic.ar import RA
from Heuristic.hrlinear import RHlinear
from New.lc import LC
from New.lp import LP
from New.fft import FFTifan
from New.recommenderPerson import RecommenderP
from New.recommenderPersonLinear import RecommenderPlinear
from New.sentimentanalyzer import SentimentAnalyzer
from staticCommon import Keys
from New.fftmax import FFTmax
from New.fftzigzag import FFTzigzag
from New.rt import RT
from metaModelData import metaModelData
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
import glob
from random import random
from statistics import mean


models = [LP,S2MR,RHlinear,RT,CorrectReply,FFTzigzag,FFTmax,FFTifan,RH,CR,BaselineRandom,SURP,LC]
#RecommenderP, RecommenderPlinear
outfileGlob = '/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/withGlobModels'
outfilePers = '/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/withPersModels'
outfileParameters = '/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/params'
outfileLog = '/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/log1.txt'
outfileOverview = '/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/overview.txt'
while any(a for a in glob.glob("/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/*") if a == outfileLog):
    outfileLog = '/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/log' + str(int(outfileLog[len('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/log'):-4]) +1)+'.txt'
log = open(outfileLog, 'w+')
overview = open(outfileOverview, 'w+')
overview.close()
log.close()
def logstr(*text, otherfile = False):
    if otherfile:
        log = open(otherfile,'a')
        outtext = ''
        for t in text:
            outtext += str(t) + ', '
        log.write(outtext[:-1] +'\n')
        log.close()
    log = open(outfileLog,'a')
    outtext = ''
    for t in text:
        outtext += str(t) + ', '
    print(str(outtext)[:-1])
    log.write(outtext[:-1] +'\n')
    log.close()

sources = ['Study12dataReshaped']#,'Study11dataReshaped','Study12dataReshaped','Study1dataReshaped']

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
        panas = {}
        media = {}
        if 'DemRep_C_current' in ind.keys():
            if '' == listLine[ind['DemRep_C_current']]:
                continue
            conservatism = float(listLine[ind['DemRep_C_current']])
        elif 'Conservatism' in ind.keys():
            conservatism = float(listLine[ind['Conservatism']])*7/5
        elif 'Conserv' in ind.keys():
            try:
                conservatism = float(listLine[ind['Conserv']])*7/5
            except:
                continue
        if '' == conservatism:
            continue
        for item in ind.keys():
            if item in ['Exciting_Democrats_Combined', 'Exciting_Republicans_Combined', 'Familiarity_Democrats_Combined', 'Familiarity_Republicans_Combined', 'Importance_Democrats_Combined', 'Importance_Republicans_Combined', 'Likelihood_Democrats_Combined', 'Likelihood_Republicans_Combined', 'Partisanship_All_Combined', 'Partisanship_All_Partisan', 'Partisanship_Democrats_Combined', 'Partisanship_Republicans_Combined', 'Worrying_Democrats_Combined', 'Worrying_Republicans_Combined']: #'Sharing_Democrats_Combined', 'Sharing_Republicans_Combined', 
                itemComponents[item] = float(listLine[ind[item]])
            elif 'CRT1' in item or 'CRT3' in item:
                crtresults.append(float(listLine[ind[item]] in item.split('_')[1].split(':')[1:]))
            elif 'PANAS' in item and 'Inst' not in item:
                if listLine[ind[item]] == '':
                    #logstr('One panas error', listLine[ind['id']], item)
                    panas[item.split('_T')[0]] = None
                    continue
                panas[item.split('_T')[0]] = float(listLine[ind[item]])
            elif 'AccImp_How important' in item:
                accimp = float(listLine[ind[item]])
            elif 'Gender_What' in item:
                gender = float(listLine[ind[item]])
            elif 'Sex' == item:
                try:
                    gender = float(listLine[ind[item]])
                except:
                    gender = 'NoInfo'

        crt = sum(crtresults)/len(crtresults)
        panasPos = ['PANAS_' + str(i) for i in [1,3,5,9,10,14,16,17,19]]
        panasNeg = ['PANAS_' + str(i) for i in [2,4,6,7, 8,11,12,13,15,18,20]]
        for a in ['_RT_2_Timing-Last Click','_RT_accurate','_A_RT_accurate']:
            if a not in ind.keys():
                continue
            try:
                react_time = float(listLine[ind[a]])
            except:
                react_time = 'NoInfo'
        if react_time == 'NoInfo':
            continue
        for a in ['ClintonTrump','POTUS2016_Who did yo']:
            if a not in ind.keys():
                continue
            try:
                ct = int(listLine[ind[a]])
            except:
                ct = 'NoInfo'
                print('ct:', listLine[ind[a]])
        for a in ['Education','Education_What is th']:
            if a not in ind.keys():
                continue
            try:
                edu = int(listLine[ind[a]])
            except:
                edu = 'NoInfo'
        if 'AccImp_How important' not in ind.keys():
            accimp = 'NoInfo'
            
        personfeatures = {
            'crt' : float(crt), 
            'conservatism' : conservatism, 
            'ct' : ct,
            'education' : edu,
            'gender' : gender,
            'accimp' : accimp,
            'panasPos' : sum(panas[a] for a in panasPos if panas[a] != None) if len(panas.keys())>0 else 'NoInfo',
            'panasNeg' : sum(panas[a] for a in panasNeg if panas[a] != None) if len(panas.keys())>0 else 'NoInfo',
            'reaction_time' : react_time
            }
        nokeys = []
#        for a in personfeatures.keys():
#            if personfeatures[a] == 'NoInfo':
#                nokeys.append(a)
#        for a in nokeys:
#            personfeatures.pop(a)
        taskfeatures = {}
        for a in itemComponents.keys():
            if conservatism >= 3.5:
                if 'Democrats' in a:
                    continue
                else:
                    key = a.replace('Republicans', 'Party')
            elif conservatism <= 3.5:
                if 'Republicans' in a:
                    continue
                else: 
                    key = a.replace('Democrats', 'Party')
            taskfeatures[key] = itemComponents[a]
        if Keys.person == None:
            Keys.person = [a for a in personfeatures.keys()]
        if Keys.task == None:
            SentimentAnalyzer.initialize()
            Keys.task = [a for a in taskfeatures.keys() if 'ikelihood' not in a] 
            Keys.task += [a for a in SentimentAnalyzer.relevant]
        
        newItem = Item(
            listLine[ind['id']], listLine[ind['domain']],
            listLine[ind['task']], listLine[ind['response_type']],
            listLine[ind['choices']], listLine[ind['sequence']], 
            float(crt), 
            bool(int(listLine[ind['truthful']])), 
            bool(int(listLine[ind['_accurate']])), 
            bool(int(listLine[ind['binaryResponse']])),
            str(listLine[ind['response']]),
            persFeat= personfeatures,
            taskFeat= taskfeatures
        )

        itemsList.append(newItem)
    return itemsList

currentmax = {}
currentmaxpers = {}

def ordering(item):
    return item.sequence_number

def main(mini = True):
    mini = False
    allcitems = []
    for source in sources:
        allcitems =itemsList(source)
        logstr('Items read out')
        persons = {}
        for item in allcitems:
            if item.identifier not in persons.keys():
                persons[item.identifier] = []
            persons[item.identifier].append(item)
        newpersons = {}
        for person in persons.keys():
            persons[person].sort(key=ordering)
            if not mini:
                newpersons[person] = persons[person]
            if random() > mean([i.birep == i.truthful for i in persons[person]]):
                newpersons[person] = persons[person]
            #if random() < 10.01:
            #    newpersons[person] = persons[person]
        logstr(len(newpersons))
        persons = newpersons

        allitems = []
        for ident in persons.keys():
            if 'y1d' in source and len(persons[ident]) < 35:
                logstr('Wrong number of items:', len(persons[ident]), ident)
            if 'y11d' in source and len(persons[ident]) != 20:
                logstr('Wrong number of items:', len(persons[ident]), ident)
            if 'y12d' in source and len(persons[ident]) != 24:
                logstr('Wrong number of items:', len(persons[ident]), ident)
            else:
                allitems.extend(persons[ident])
        logstr('Incomplete items filtered out')
        pool = Pool(4)
        pool.map(doModel, [(model, allitems) for model in models if not "nandom" in model().name])
        pool.close()
        pool.join()
        logstr('Done, merging one model file')
        os.chdir("/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2")
        modelResponse = {}
        allmodelsfile = open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/allmodels'+source +'.csv', 'w+')
        for modelfile in glob.glob("with*"):
            with open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/'+modelfile, 'r') as csvfile:
                spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    if row['id'] not in modelResponse.keys():
                        modelResponse[row['id']] = {}
                    if row['task'] not in modelResponse[row['id']].keys():
                        modelResponse[row['id']][row['task']] = {}
                    resp = row['modelResponseGlob'] if 'modelResponseGlob' in row.keys() else row['modelResponsePers']
                    print(row.keys())
                    if '.' in str(resp):
                        modelResponse[row['id']][row['task']][modelfile] = int(random()<float(resp))
                    elif 'e' in str(resp):
                        modelResponse[row['id']][row['task']][modelfile] = int(bool('T' in resp or str(resp)==1))
                    else:
                        modelResponse[row['id']][row['task']][modelfile] = int(resp)
            #logstr(modelResponse[row['id']][row['task']].keys(), modelfile)
        keys = "id,task,choices,domain,trial,response_type,realnews,fakenews,acc,birep,response"
        logstr(Keys.person+ Keys.task)
        for word in Keys.person+ Keys.task:
            keys += ','+ word
        for word in glob.glob("with*"):
            keys += ','+ word
        allmodelsfile.write(keys +'\n')
        for item in allitems:
            for modelfile in glob.glob("with*"):
                if modelfile not in modelResponse[item.identifier][item.task_str].keys():
                    logstr(modelfile,item.identifier,item.task_str)
                    modelResponse[item.identifier][item.task_str][modelfile] = 'Noreply'
            outstring = ""
            for a in [
                item.identifier,
                item.task_str,
                item.choices_str,
                item.domain,
                item.sequence_number,
                item.response_type,
                item.realnews,
                item.fakenews,
                item.acc,
                item.birep,
                item.response
                ] + [str(item.person_features[a]) for a in Keys.person
                ] + [str(item.feature(a)) for a in Keys.task
                ] + [str(modelResponse[item.identifier][item.task_str][modelfile]) for modelfile in glob.glob("with*")]:
                outstring += str(a) + ","
            allmodelsfile.write(outstring[:-1]+'\n')


def doModel(args):
    model, allitems = args
    metaModelData.modelTendencyPerTask[model().name + '-glob'] = {}
    if 'T' in model().name:
        logstr(model().name, 'training')

        model().fitTreeOnTrials(allitems)
        logstr(model().name, 'trained.')
    currentmax[model().name] = 0
    try:
        model().globalTrain(allitems)
    except:
        logstr(model().name, 'not trained globally')
    tendPerTask = {}
    logstr(model().name,'optimizing')
    optimizingitems = []
    persons = {}
    for item in allitems:
        if item.identifier not in persons.keys():
            persons[item.identifier] = []
        persons[item.identifier].append(item)
    for person in persons.keys():
        if random() < 10.1:
            optimizingitems.extend(persons[person])
    logstr(len(optimizingitems))
    if len(model().parameter.keys())>0:
        personOptimum = basinhopping(minimized, [0.05]*len(model().parameter.keys()), niter=200, stepsize=3, T=4, minimizer_kwargs={"args" : (model, optimizingitems), "tol":0.001, "bounds": [[-40,40] for a in range(len(model().parameter.keys()))],},disp=False)
        optpars = personOptimum.x
    else:
        outpars = []
    perf2d, corr2d, tend2d, pars = itemsOptimizedOneModelPeformance(model, optimizingitems)
    perf = [item for sublist in perf2d for item in sublist]
    corr = [item for sublist in corr2d for item in sublist]
    tend = [item for sublist in tend2d for item in sublist]
    parsPerModelPar = {}
    for par in range(len(model().parameter.keys())):
        parsPerModelPar[par] = []
    for a in pars.keys():
        for par in range(len(pars[a])):
            parsPerModelPar[par].append(pars[a][par])
    logstr(model().name, '  Optimized per person:', 
        stats.mean(perf), stats.stdev(perf), stats.mean(corr), stats.stdev(corr), stats.mean(tend), stats.stdev(tend), 
        [(stats.mean(parsPerModelPar[a]), stats.stdev(parsPerModelPar[a])) for a in parsPerModelPar.keys()], otherfile=outfileOverview)
    
 

    #result, modelPerformance, modelTendency, modelCorrectness = itemsOneModelPeformance(toCommandList(optpars, model), model, allitems, writeFile=open(outfileGlob + model().name + '.csv','w+'))
    #logstr(model().name, '  Evaluation result:  ', result, 'tendency:', sum(modelTendency)/len(modelTendency), 'correctness:', sum(modelCorrectness)/len(modelCorrectness), model(commands=toCommandList(optpars, model)).parameter, otherfile=outfileOverview)
    #for task in metaModelData.modelTendencyPerTask[model().name + '-glob'].keys():
    #    tendPerTask[task + '-glob'] = stats.mean(metaModelData.modelTendencyPerTask[model().name + '-glob'][task])

    if model().name + '-pers' in metaModelData.modelTendencyPerTask.keys():
        for task in metaModelData.modelTendencyPerTask[model().name + '-pers'].keys():
            tendPerTask[task + '-pers'] = stats.mean(metaModelData.modelTendencyPerTask[model().name + '-pers'][task])
    logstr(model().name, tendPerTask,otherfile=outfileOverview)
    

def minimized(pars, model, items):
    optCommands = toCommandList(pars, model)
    result, a, modelTendency, modelCorrectness, = itemsOneModelPeformance(optCommands, model, items)
    #tend = sum(modelTendency)/len(modelTendency)
    #corr = sum(modelCorrectness)/len(modelCorrectness)
    #if tend < 0.1:
        #logstr(tend)
        #return 1
    return round(-1*result,100)

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
            logstr('keys length error', model)
            break
        optCommands.append('self.parameter[\'' + a + '\'] = ' + str(pars[i]))
        i += 1
    return optCommands


def itemsOneModelPeformance(pars, model, items, predicS = True, writeFile = False):

    keys = "id,task,choices,domain,trial,response_type,realnews,fakenews,acc,birep,response,"
    for a in Keys.person + Keys.task:
        keys += a+',' 

    if writeFile:
        writeFile.write(keys[:-1] + ",model,modelResponseGlob,parameters,tend,corr\n")
    corrLimit = False#'assic' in model().name 
    #input: list of items
    maxpers = -1
    perscount = 0
    items = [a for a in items]
    for item in items:
        metaModelData.modelTendencyPerTask[model().name + '-glob'][item.task[0][0]] = []
    modelTendency = []
    modelPerformance = []
    modelCorrectness = []
    if len(metaModelData.sequencesPerPers.keys()) == 0:
        for item in items:
            if item.identifier not in metaModelData.sequencesPerPers.keys():
                metaModelData.sequencesPerPers[item.identifier] = {}
            if item.sequence_number not in metaModelData.sequencesPerPers[item.identifier].keys():
                metaModelData.sequencesPerPers[item.identifier][item.sequence_number] = item
    for person in metaModelData.sequencesPerPers.keys():
        if perscount < maxpers or maxpers <0:
            perscount += 1
        else:
            break
        performanceOfPerson= []
        m = model(commands=pars)
        for seq in sorted([int(a) for a in metaModelData.sequencesPerPers[person].keys()]):
            item = metaModelData.sequencesPerPers[person][str(seq)]
            if not predicS:
                predictionPerf = (item.response == m.predict(item))
            else:
                pred = min(1.0,max(m.predictS(item),0.0)) 
                if item.birep:
                    predictionPerf = pred
                elif not item.birep:
                    predictionPerf = 1.0 - pred
                else:
                    logstr('Error')
            modelTendency.append(pred)
            modelCorrectness.append(pred if item.truthful else 1-pred)
            trialperformance = predictionPerf #if item.birep else 1-prediction
            performanceOfPerson.append(trialperformance)
            metaModelData.modelTendencyPerTask[m.name + '-glob'][item.task[0][0]].append(pred)
            
            if writeFile:
                outstring = ""
                for a in [
                    item.identifier,
                    item.task_str,
                    item.choices_str,
                    item.domain,
                    item.sequence_number,
                    item.response_type,
                    item.realnews,
                    item.fakenews,
                    item.acc,
                    item.birep,
                    item.response
                    ] + [str(item.person_features[a]) for a in Keys.person
                    ] + [str(item.feature(a)) for a in Keys.task
                    ] + [m.name, predictionPerf
                    ]:
                    outstring += str(a) + ","
                writeFile.write(outstring+ str(pars).replace(',',';') +str(pred) + str(pred if item.truthful else 1-pred) +'\n')
        modelPerformance.extend(performanceOfPerson)
        #logstr('Person done', person, perscount)
    #logstr('current', model().name ,sum(modelPerformance)/len(modelPerformance), 'tendency:', sum(modelTendency)/len(modelTendency), 'correctness:', sum(modelCorrectness)/len(modelCorrectness), model(commands=pars).parameter)
    if corrLimit and sum(modelCorrectness)/len(modelCorrectness) > 0.79:
        return 0, [0], [0], [0]
    if sum(modelPerformance)/len(modelPerformance) > currentmax[model().name]:
        logstr('currentmax', model().name ,sum(modelPerformance)/len(modelPerformance), 'tendency:', sum(modelTendency)/len(modelTendency), 'correctness:', sum(modelCorrectness)/len(modelCorrectness), model(commands=pars).parameter)
        currentmax[model().name] = sum(modelPerformance)/len(modelPerformance)
    return sum(modelPerformance)/len(modelPerformance), modelPerformance, modelTendency, modelCorrectness

def itemsOptimizedOneModelPeformance(model, items, predicS = True, atMostPeople = -1):
    atMostPeople = -100
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
    keys = "id,task,choices,domain,trial,response_type,realnews,fakenews,acc,birep,response,"
    for a in Keys.person + Keys.task:
        keys += a+',' 
    open(outfilePers + model().name + '.csv',"w+").write(keys[:-1] + ",model,modelResponsePers,parameters,tend,corr\n")
    for person in people:
        if len(model().parameter.keys()) > 0:
            personOptimum = basinhopping(minimizedOnePerson, [0.05]*len(model().parameter.keys()), niter=200, stepsize=3, T=4, minimizer_kwargs={"args" : (model, person, sequencesPerPers[person])})
            optpars = personOptimum.x
        else: 
            optpars = [] 
        perf, corr, tend = itemsOnePersonOneModelPeformance(toCommandList(optpars, model), model, person, sequencesPerPers[person], writeFile= open(outfilePers + model().name + '.csv',"a"))
        performanceOfPerson[person] = perf
        correctnessOfPerson[person] = corr
        tendencyOfPerson[person] = tend
        parametersOfPerson[person] = optpars
        if atMostPeople > peopleCounter and atMostPeople > 0:
            peopleCounter +=1
        if atMostPeople <= peopleCounter and atMostPeople > 0:
            break
    return performanceOfPerson.values(), correctnessOfPerson.values(), tendencyOfPerson.values(), parametersOfPerson


def seqnum(item):
    return int(item.sequence_number)

def itemsOnePersonOneModelPeformance(pars, model, person, items, predicS = True,writeFile=False):
    #input: list of items
    items = [a for a in items]
    modelTendency = []
    modelCorrectness = []
    performanceOfPerson = []
    m = model(commands=pars)
    metaModelData.modelTendencyPerTask[m.name + '-pers'] = {}
    for item in sorted(items, key=seqnum):
        metaModelData.modelTendencyPerTask[m.name + '-pers'][item.task[0][0]] = []
        if item.identifier != person:
            logstr('Error')
            RuntimeError
        if not predicS:
            accrej = m.predict(item)
            predictionPerf = float(item.response == accrej)
            pred = 'Accept' in accrej
        else:
            pred = min(1.0,max(m.predictS(item),0.0)) 
            if item.birep:
                predictionPerf = min(1.0,max(m.predictS(item),0.0)) 
            elif not item.birep:
                predictionPerf = 1.0 - pred
            else:
                logstr('Error')
        modelTendency.append(pred)
        modelCorrectness.append(pred if item.truthful else 1-pred)
        performanceOfPerson.append(predictionPerf)
        metaModelData.modelTendencyPerTask[m.name + '-pers'][item.task[0][0]].append(pred)
        if writeFile:
            outstring = ""
            for a in [
                item.identifier,
                item.task_str,
                item.choices_str,
                item.domain,
                item.sequence_number,
                item.response_type,
                item.realnews,
                item.fakenews,
                item.acc,
                item.birep,
                item.response
                ] + [str(item.person_features[a]) for a in Keys.person
                ] + [str(item.feature(a)) for a in Keys.task
                ] + [m.name, pred]:
                outstring += str(a) + ","
            writeFile.write(outstring+ str(pars).replace(',',';') +str(pred) + str(pred if item.truthful else 1-pred) +'\n')


    if model().name + person not in currentmaxpers.keys() or sum(performanceOfPerson)/len(performanceOfPerson)> currentmaxpers[model().name + person]:
        logstr('currentmaxpers', model().name, person ,sum(performanceOfPerson)/len(performanceOfPerson), 'tendency:', sum(modelTendency)/len(modelTendency), 'correctness:', sum(modelCorrectness)/len(modelCorrectness), model(commands=pars).parameter)
        currentmaxpers[model().name + person] = sum(performanceOfPerson)/len(performanceOfPerson)
    return performanceOfPerson, modelCorrectness, modelTendency
    return sum(performanceOfPerson)/len(performanceOfPerson) 





def stopwatch(seconds):
    start = time.time()
    logstr(start)
    elapsed = 0
    while seconds< 0 or elapsed < seconds:
        time.sleep(1)
        logstr()


if __name__ == '__main__':
    start = time.time()
    main(mini=True)
    logstr('Time for calculation:', round(time.time()-start,1))

