
from New.dt import DT
from staticCommon import Keys
from metaModelData import metaModelData
from New.sentimentanalyzer import SentimentAnalyzer

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


models = [DT]#,RecommenderP, RecommenderPlinear]
#LCparty,LP,S2MR,CR, CorrectReply,BaselineRandom,FFTzigzag,FFTmax,FFTifan

outfileGlob = '/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/metaGlobModels'
outfilePers = '/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/metaPersModels'


sources = ['data/study2/allmodelsStudy1dataReshaped']#'data/Study1dataReshaped']



def itemsList(source):
    itemsList = []
    linecount = 0
    indcount = 0
    line1 = True
    lines = open('/home/hippo/git/news-reasoning/benchmarks/misinformation/'+source+'.csv')
    ind = {}
    for line in lines:
        listLine = line.replace('\r','').replace('\n','').split(',')
        if line1:
            line1 = False
            for key in listLine:
                ind[key] = indcount
                indcount += 1
            continue
        panasPos = ['PANAS_' + str(i) for i in [1,3,5,9,10,14,16,17,19]]
        panasNeg = ['PANAS_' + str(i) for i in [2,4,6,7, 8,11,12,13,15,18,20]]
        personfeatures = {
            'crt' : float(listLine[ind['crt']]), 
            'conservatism' : listLine[ind['conservatism']], 
            'ct' : int(listLine[ind['ct']]),
            'education' : int(listLine[ind['education']]),
            'gender' : listLine[ind['gender']],
            'accimp' : float(listLine[ind['accimp']]),
            'panasPos' : float(listLine[ind['panasPos']]),
            'panasNeg' : float(listLine[ind['panasNeg']]),
            'reaction_time' : float(listLine[ind['reaction_time']])
            }
        taskfeatures = {}
        os.chdir("/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2")
        for modelfile in glob.glob("with*"):
            no = False
            for a in ['ecision', 'Pers', 'inear', 'ecommend', 'Tree']:
                if a in modelfile:
                    no = True
            if no:
                continue
            taskfeatures[modelfile] = float(listLine[ind[modelfile]])

        if Keys.person == None:
            Keys.person = [a for a in personfeatures.keys()]
        if Keys.task == None:
            SentimentAnalyzer.initialize()
            Keys.task = [a for a in taskfeatures.keys() if 'ikelihood' not in a] 
            Keys.task += [a for a in SentimentAnalyzer.relevant]
        

        linecount += 1
        itemsList.append(Item(
            listLine[ind['id']], listLine[ind['domain']],
            listLine[ind['task']], listLine[ind['response_type']],
            listLine[ind['choices']], listLine[ind['trial']], 
            float(listLine[ind['crt']]), 
            bool('T' in listLine[ind['realnews']]), 
            bool('T' in listLine[ind['acc']]), 
            bool('T' in listLine[ind['birep']]),
            str(listLine[ind['response']]),
            persFeat= personfeatures,
            taskFeat= taskfeatures
        ))
    return itemsList

currentmax = {}
currentmaxpers = {}


def main(mini = True):
    allcitems = []
    for source in sources:
        allcitems.extend(itemsList(source))
    print('Items read out')
    persons = {}
    for item in allcitems:
        if item.identifier not in persons.keys():
            persons[item.identifier] = []
        persons[item.identifier].append(item)
    newpersons = {}
    for person in persons.keys():
        if not mini:
            break
        #if random() > mean([i.birep == i.truthful for i in persons[person]]):
        #    newpersons[person] = persons[person]
        if random() < 10.01:
            newpersons[person] = persons[person]
    print(len(newpersons))
    persons = newpersons

    allitems = []
    for ident in persons.keys():
        if False and len(persons[ident]) != 36:
            print('Wrong number of items:', len(persons[ident]), ident)
        else:
            allitems.extend(persons[ident])
    print('Incomplete items filtered out')
    pool = Pool(4)
    pool.map(doModel, [(model, allitems) for model in models if not "nandom" in model().name])
    pool.close()
    pool.join()
    print('Done, merging one model file')
    os.chdir("/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2")
    modelResponse = {}
    allmodelsfile = open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/allmodelsdt.csv', 'w+')
    for modelfile in glob.glob("with*"):
        with open('/home/hippo/git/news-reasoning/benchmarks/misinformation/data/study2/'+modelfile, 'r') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if row['id'] not in modelResponse.keys():
                    modelResponse[row['id']] = {}
                if row['task'] not in modelResponse[row['id']].keys():
                    modelResponse[row['id']][row['task']] = {}
                resp = row['modelResponseGlob'] if 'modelResponseGlob' in row.keys() else row['modelResponsePers']
                if '.' in str(resp):
                    modelResponse[row['id']][row['task']][modelfile] = int(random()<float(resp))
                elif 'e' in str(resp):
                    modelResponse[row['id']][row['task']][modelfile] = int(bool('T' in resp))
                else:
                    modelResponse[row['id']][row['task']][modelfile] = int(resp)
        #print(modelResponse[row['id']][row['task']].keys(), modelfile)
    keys = "id,task,choices,domain,trial,response_type,realnews,fakenews,acc,birep,response"
    for word in Keys.person+ Keys.task:
        keys += ','+ word
    for word in glob.glob("with*"):
        keys += ''#','+ word
    print(keys)
    allmodelsfile.write(keys +'\n')
    for item in allitems:
        for modelfile in glob.glob("with*"):
            if modelfile not in modelResponse[item.identifier][item.task_str].keys():
                #print(modelfile,item.identifier,item.task_str)
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
            ] + [str(item.feature(a)) +a for a in SentimentAnalyzer.relevant
            ] + [str(modelResponse[item.identifier][item.task_str][modelfile]) + modelfile for modelfile in glob.glob("with*")]:
            outstring += str(a) + ","
        allmodelsfile.write(outstring[:-1]+'\n')


def doModel(args):
    model, allitems = args
    metaModelData.modelTendencyPerTask[model().name + '-glob'] = {}
    if 'T' in model().name:
        print(model().name, 'training')

        model().fitTreeOnTrials(allitems)
        print(model().name, 'trained.')
    currentmax[model().name] = 0
    try:
        model().globalTrain(allitems)
    except:
        print(model().name, 'not trained globally')
    if len(model().parameter.keys()) > 0:
        print(model().name,'optimizing')
        personOptimum = basinhopping(minimized, [0.05]*len(model().parameter.keys()), niter=200, stepsize=3, T=4, minimizer_kwargs={"args" : (model, allitems), "tol":0.001, "bounds": [[-40,40] for a in range(len(model().parameter.keys()))],},disp=False)
        print(model().name, '  Optimized globally:  ', -1*minimized(personOptimum.x, model, allitems), personOptimum.x)
        result, a, b, c = itemsOneModelPeformance(toCommandList(personOptimum.x, model), model, allitems, writeFile=open(outfileGlob + model().name + '.csv','w+'))
        tendPerTask = {}
        for task in metaModelData.modelTendencyPerTask[model().name + '-glob'].keys():
            tendPerTask[task + '-glob'] = stats.mean(metaModelData.modelTendencyPerTask[model().name + '-glob'][task])
        #return
        perf2d, corr2d, tend2d, pars = itemsOptimizedOneModelPeformance(model, allitems)
        perf = [item for sublist in perf2d for item in sublist]
        corr = [item for sublist in corr2d for item in sublist]
        tend = [item for sublist in tend2d for item in sublist]
        parsPerModelPar = {}
        for par in range(len(model().parameter.keys())):
            parsPerModelPar[par] = []
        for a in pars.keys():
            for par in range(len(pars[a])):
                parsPerModelPar[par].append(pars[a][par])
        print(model().name, '  Optimized per person:', 
            stats.mean(perf), stats.stdev(perf), stats.mean(corr), stats.stdev(corr), stats.mean(tend), stats.stdev(tend), 
            [(stats.mean(parsPerModelPar[a]), stats.stdev(parsPerModelPar[a])) for a in parsPerModelPar.keys()])
        for task in metaModelData.modelTendencyPerTask[model().name + '-pers'].keys():
            tendPerTask[task + '-pers'] = stats.mean(metaModelData.modelTendencyPerTask[model().name + '-pers'][task])
        print(tendPerTask)
    else:
        print(model().name,'not optimizing')
        result, a, b, c = itemsOneModelPeformance(toCommandList([], model), model, allitems, writeFile=open(outfileGlob + model().name + '.csv',"w+"))
        print(model().name, '  Non Optimizable:     ', result)
    

def minimized(pars, model, items):
    optCommands = toCommandList(pars, model)
    result, a, modelTendency, modelCorrectness, = itemsOneModelPeformance(optCommands, model, items)
    #tend = sum(modelTendency)/len(modelTendency)
    #corr = sum(modelCorrectness)/len(modelCorrectness)
    #if tend < 0.1:
        #print(tend)
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
            print('keys length error', model)
            break
        optCommands.append('self.parameter[\'' + a + '\'] = ' + str(pars[i]))
        i += 1
    return optCommands


def itemsOneModelPeformance(pars, model, items, predicS = True, writeFile = False):

    keys = "id,task,choices,domain,trial,response_type,realnews,fakenews,acc,birep,response,"
    for a in Keys.person + Keys.task:
        keys += a+',' 

    if writeFile:
        writeFile.write(keys[:-1] + ",model,modelResponseGlob\n")
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
                    print('Error')
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
                    ] + [str(item.feature(a)) for a in SentimentAnalyzer.relevant
                    ] + [m.name, pred]:
                    outstring += str(a) + ","
                writeFile.write(outstring[:-1]+'\n')
            modelTendency.append(pred)
            modelCorrectness.append(pred if item.truthful else 1-pred)
            trialperformance = predictionPerf #if item.birep else 1-prediction
            performanceOfPerson.append(trialperformance)
            metaModelData.modelTendencyPerTask[m.name + '-glob'][item.task[0][0]].append(trialperformance)
        modelPerformance.extend(performanceOfPerson)
        #print('Person done', person, perscount)
    #print('current', model().name ,sum(modelPerformance)/len(modelPerformance), 'tendency:', sum(modelTendency)/len(modelTendency), 'correctness:', sum(modelCorrectness)/len(modelCorrectness), model(commands=pars).parameter)
    if corrLimit and sum(modelCorrectness)/len(modelCorrectness) > 0.79:
        return 0, [0], [0], [0]
    if sum(modelPerformance)/len(modelPerformance) > currentmax[model().name]:
        print('currentmax', model().name ,sum(modelPerformance)/len(modelPerformance), 'tendency:', sum(modelTendency)/len(modelTendency), 'correctness:', sum(modelCorrectness)/len(modelCorrectness), model(commands=pars).parameter)
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
    open(outfilePers + model().name + '.csv',"w+").write(keys[:-1] + ",model,modelResponsePers\n")
    for person in people:
        personOptimum = basinhopping(minimizedOnePerson, [0.05]*len(model().parameter.keys()), niter=200, stepsize=1, T=4, minimizer_kwargs={"args" : (model, person, sequencesPerPers[person])})
        perf, corr, tend = itemsOnePersonOneModelPeformance(toCommandList(personOptimum.x, model), model, person, sequencesPerPers[person], writeFile= open(outfilePers + model().name + '.csv',"a"))
        performanceOfPerson[person] = perf
        correctnessOfPerson[person] = corr
        tendencyOfPerson[person] = tend
        parametersOfPerson[person] = personOptimum.x
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
            print('Error')
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
                print('Error')
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
                ] + [str(item.feature(a)) for a in SentimentAnalyzer.relevant
                ] + [m.name, pred]:
                outstring += str(a) + ","
            writeFile.write(outstring[:-1]+'\n')


    if model().name + person not in currentmaxpers.keys() or sum(performanceOfPerson)/len(performanceOfPerson)> currentmaxpers[model().name + person]:
        print('currentmaxpers', model().name, person ,sum(performanceOfPerson)/len(performanceOfPerson), 'tendency:', sum(modelTendency)/len(modelTendency), 'correctness:', sum(modelCorrectness)/len(modelCorrectness), model(commands=pars).parameter)
        currentmaxpers[model().name + person] = sum(performanceOfPerson)/len(performanceOfPerson)
    return performanceOfPerson, modelCorrectness, modelTendency
    return sum(performanceOfPerson)/len(performanceOfPerson) 





def stopwatch(seconds):
    start = time.time()
    print(start)
    elapsed = 0
    while seconds< 0 or elapsed < seconds:
        time.sleep(1)
        print()


if __name__ == '__main__':
    start = time.time()
    main(mini=True)
    print('Time for calculation:', round(time.time()-start,1))

