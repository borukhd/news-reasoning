from ..scripts.relationPlotter import *
import statistics 
import os
import pathlib

def makeRelForSwpl(adaptInTest, onlyLearningPhaseEval, sources, allStimuli, allModels):
        personsToSuccesses = {}

        fileParobject=str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "/relational/results/swpl" +str(adaptInTest) + str(onlyLearningPhaseEval) +str(allStimuli)+str(allModels)+".csv" 

        filepratowrite = open(fileParobject, 'w')

        for source in sources:
            #adaptInTest = True if 'crm' in source else False 
            print(source)
            first= True
            sfile= open(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "/relational/results/resultLearningTIfor" + source+str(adaptInTest) + str(onlyLearningPhaseEval) + ".csv")
            for listLine in sfile:
                if first: 
                    first = False
                else:
                    line = listLine.split(',')
                    modelName = line[11] + line[0].replace('RL-ELO', 'RL_ELO').replace('resc', 'Resc')
                    if 'train' in modelName:
                        continue
                    if not allStimuli:
                        if '2' not in line[6] or '4' not in line[6]:
                            continue
                    k = modelName
                    if 'RGMD' in source or 'FHL' in source:
                        sourceType = 'macaques'
                    elif 'Wasp' in source:
                        sourceType = 'wasps' 
                    elif 'Camarena' in source:
                        sourceType = 'pigeons'
                    elif 'Hum' in source:
                        sourceType = 'humans'
                    else:
                        sourceType = 'error'
                        print('Species Error')
                    personName = line[1] + source + '@' + sourceType
                    if not personName in personsToSuccesses.keys():
                        personsToSuccesses[personName] = {}
                        print(personName)
                    if not modelName in personsToSuccesses[personName].keys():
                        personsToSuccesses[personName][modelName] = []
                    personsToSuccesses[personName][modelName].append(float(line[12]))
        firstline= 'id,succ,mod,type,mode'
        filepratowrite.write(firstline + '\n')

        keylist = [a for a in personsToSuccesses.keys()]
        keylist.sort()
        for pers in keylist:
            for mod in personsToSuccesses[pers].keys():
                if 'train' in mod.split('ing')[0]:
                    continue
                nextLine = pers + ',' + str(sum(personsToSuccesses[pers][mod])/len(personsToSuccesses[pers][mod])) + ',' + mod.split('ing')[0] + ','+ pers.split('@')[-1] + ',' + mod.split('ing')[1]
                filepratowrite.write(nextLine + '\n')
        filepratowrite.close()


def makeIntvls(adaptInTest,onlyLearningPhaseEval, sources, divisions, allStimuli, allModels):
    modelLineCounter = {}
    modelsToIntervals = {}
    modelLinesTotal = {}
    fileParobject2="benchmarks/relational/results/intvlsModCorrectnessPerModels" +str(False) + str(onlyLearningPhaseEval) + str(divisions)+str(allStimuli)+str(allModels)+".csv" 

    filepratowrite = open(fileParobject2, 'w+')
    for source in sources:
        #adaptInTest = True if 'crm' in source else False 
        first= True
        sfile= open(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "/relational/results/resultLearningTIfor" + source+str(adaptInTest) + str(onlyLearningPhaseEval) + ".csv")
        linesTotal = 0
        print(source + ': finding total length')
        for line in sfile:
            modelName = line.split(',')[11]  + line.split(',')[0].replace('resc', 'Resc') #+ '@' + source
            if modelName not in modelLinesTotal.keys():
                modelLinesTotal[modelName] = 0
            if not allStimuli and 'test' in modelName:
                if not '2' in line.split(',')[6] or not '4' in line.split(',')[6]:
                    #print(line.split(',')[6])
                    continue
            modelLinesTotal[modelName] += 1
            #print(modelName)
        sfile.close()
        sfile= open(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "/relational/results/resultLearningTIfor" + source+str(adaptInTest) + str(onlyLearningPhaseEval)  + ".csv")
        print('iterating', source)
        for listLine in sfile:
            if first: 
                first = False
                continue
            line = listLine.split(',')
            modelName = line[11] +line[0].replace('resc', 'Resc') # +'@' +  source
            if not allStimuli and 'test' in modelName:
                if not '2' in line[6] or not '4' in line[6]:
                    continue
            if modelName not in modelsToIntervals.keys():
                modelsToIntervals[modelName] = {}
                modelLineCounter[modelName] = 0
                for intervalCounter in range(divisions):
                    intervalName = 'interval' + str(intervalCounter)
                    modelsToIntervals[modelName][intervalName] = []
            modelLineCounter[modelName] += 1
            for i in range(divisions-1, -1, -1):
                if modelLineCounter[modelName] >= i * float(modelLinesTotal[modelName])/divisions:# and modelLineCounter[modelName] < (i+1) * float(modelLinesTotal[modelName])/5:
                    modelsToIntervals[modelName]['interval' + str(i)].append(float(line[12]))
                    break
    firstline= 'model,'
    for mod in modelsToIntervals.keys():
        for interv in modelsToIntervals[mod].keys():
            firstline += str(interv) + ','
        break
    filepratowrite.write(firstline[:-1] + '\n')
    
    keylist = [a for a in modelsToIntervals.keys()]
    #print(keylist)
    keylist.sort()
    for mod in keylist:
        nextLine = ''
        for interv in modelsToIntervals[mod].keys():
            #print(keylist, modelLineCounter.keys(), linesTotal)
            nextLine +=str((1 * sum(modelsToIntervals[mod][interv]))/max(1, len(modelsToIntervals[mod][interv]))) + ','
        filepratowrite.write( mod + ',' + nextLine[:-1] + '\n')
        #print(mod + ',' + nextLine[:-1].replace('\n','') + '\n')
    filepratowrite.close()

def makeObjectiveIntvls(adaptInTest,onlyLearningPhaseEval, sources, divisions):
    modelLineCounter = {}
    modelsToIntervals = {}
    modelLinesTotal = {}

    fileParobject2=str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "/relational/results/intvlsObjModCorrectnessFORModels" +str(adaptInTest) + str(onlyLearningPhaseEval) + str(divisions) +".csv" 
    filepratowrite = open(fileParobject2, 'w+')
    for source in sources:
        #adaptInTest = True if 'crm' in source else False 
        first= True
        sfile= open(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "relational/results/resultLearningTIfor" + source+str(adaptInTest) + str(onlyLearningPhaseEval) + ".csv")
        linesTotal = 0
        for line in sfile:
            modelName = line.split(',')[11] + line.split(',')[0]
            if modelName not in modelLinesTotal.keys():
                modelLinesTotal[modelName] = 0
            modelLinesTotal[modelName] += 1
        sfile.close()
        sfile= open(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "/relational/results/resultLearningTIfor" + source+str(adaptInTest) + str(onlyLearningPhaseEval) + ".csv")
        for listLine in sfile:
            if first: 
                first = False
                continue
            line = listLine.split(',')
            if not '2' in line[6] or not '4' in line[6]:
                continue
            modelName = line[11] + line[0]
            if modelName not in modelsToIntervals.keys():
                modelsToIntervals[modelName] = {}
                modelLineCounter[modelName] = 0
                for intervalCounter in range(divisions):
                    intervalName = 'interval' + str(intervalCounter)
                    modelsToIntervals[modelName][intervalName] = []
            modelLineCounter[modelName] += 1
            for i in range(divisions-1, -1, -1):
                if modelLineCounter[modelName] >= i * float(modelLinesTotal[modelName])/divisions :#and modelLineCounter[modelName] < (i+1) * float(modelLinesTotal[modelName])/5:
                    corr_pred_prob = float(line[12])
                    predictedReplyObjcorr = int(line[7]) == min([int(a) for a in line[6].split('|')])
                    actualReplyObjcorr = line[7] == line[8]
                    if 'correct' in modelName or 'Correct' in modelName:
                        modelsToIntervals[modelName]['interval' + str(i)].append(int(actualReplyObjcorr))
                    else:
                        if predictedReplyObjcorr:
                            modelsToIntervals[modelName]['interval' + str(i)].append(corr_pred_prob)
                        else:
                            modelsToIntervals[modelName]['interval' + str(i)].append(1 - corr_pred_prob)
                    break
    firstline= 'model,'
    for mod in modelsToIntervals.keys():
        for interv in modelsToIntervals[mod].keys():
            firstline += str(interv) + ','
        break
    filepratowrite.write(firstline[:-1] + '\n')
    
    keylist = [a for a in modelsToIntervals.keys()]
    keylist.sort()
    for mod in keylist:
        nextLine = ''
        for interv in modelsToIntervals[mod].keys():
            nextLine +=str((1 * sum(modelsToIntervals[mod][interv]))/max(1,len(modelsToIntervals[mod][interv]))) + ','
        filepratowrite.write( mod.replace('CorrectReply','SubjectPerformance').replace('testing','') + ',' + nextLine[:-1] + '\n')
    filepratowrite.close()


def makeRelForModels(adaptInTest, onlyLearningPhaseEval, sources):
    fileParobject=str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "/relational/results/models" +  str(adaptInTest) + str(onlyLearningPhaseEval)+ ".csv" 

    filepratowrite = open(fileParobject, 'w+')

    firstline= 'id,succ,mod,type,mode,adaptInTest,onlyLearningPhaseEval,allStimuli,sd'
    filepratowrite.write(firstline + '\n')
    for allStimuli in [True, False]:
        personsToSuccesses = {}

        for source in sources:
            #adaptInTest = True if 'crm' in source else False 
            print('Working on ' + source)
            first= True
            sfile= open(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "/relational/results/resultLearningTIfor" + source+str(adaptInTest) + str(onlyLearningPhaseEval) + ".csv")
            for listLine in sfile:
                if first: 
                    first = False
                else:
                    line = listLine.split(',')
                    modelName = line[11] + line[0].replace('RL-ELO', 'RL_ELO').replace('resc', 'Resc')
                    if 'train' in modelName:
                        continue
                    if not allStimuli:
                        if '2' not in line[6] or '4' not in line[6]:
                            continue
                    k = modelName
                    if 'RGMD' in source or 'FHL' in source:
                        sourceType = 'macaques'
                    elif 'Wasp' in source:
                        sourceType = 'wasps' 
                    elif 'Camarena' in source:
                        sourceType = 'pigeons'
                    elif 'Hum' in source:
                        sourceType = 'humans'
                    else:
                        sourceType = 'error'
                        print('Species Error')
                    personName = k + '@' + sourceType
                    if not personName in personsToSuccesses.keys():
                        personsToSuccesses[personName] = {}
                    if not modelName in personsToSuccesses[personName].keys():
                        personsToSuccesses[personName][modelName] = []
                    personsToSuccesses[personName][modelName].append(float(line[12]))

        keylist = [a for a in personsToSuccesses.keys()]
        keylist.sort()
        for pers in keylist:
            for mod in personsToSuccesses[pers].keys():
                if 'train' in mod.split('ing')[0]:
                    continue
                nextLine = pers.split('@')[0] + ',' + str(sum(personsToSuccesses[pers][mod])/len(personsToSuccesses[pers][mod])) + ',' + mod.split('ing')[0] + ','+ pers.split('@')[1] + ',' + mod.split('ing')[1] + ','+str(adaptInTest) + ','+str(onlyLearningPhaseEval) +','+str(allStimuli)+ ',' + str(statistics.pstdev(personsToSuccesses[pers][mod]))
                filepratowrite.write(nextLine + '\n')
    filepratowrite.close()



def makeRelForSources(adaptInTest, onlyLearningPhaseEval, sources):
    fileParobject=str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "/relational/results/sources" + str(adaptInTest) + str(onlyLearningPhaseEval)+ ".csv" 


    filepratowrite = open(fileParobject, 'w+')

    firstline= 'id,succ,mod,type,mode,adaptInTest,onlyLearningPhaseEval,allStimuli'
    filepratowrite.write(firstline + '\n')
    for allStimuli in [True, False]:
        personsToSuccesses = {}

        for source in sources:
            #adaptInTest = True if 'crm' in source else False 
            print(source)
            first= True
            sfile= open(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "/relational/results/resultLearningTIfor" + source+str(adaptInTest) + str(onlyLearningPhaseEval) + ".csv")
            for listLine in sfile:
                if first: 
                    first = False
                else:
                    line = listLine.split(',')
                    modelName = line[11] + line[0].replace('RL-ELO', 'RL_ELO').replace('resc', 'Resc')
                    if 'train' in modelName:
                        continue
                    if not allStimuli:
                        if '2' not in line[6] or '4' not in line[6]:
                            continue
                    k = modelName
                    if 'RGMD' in source or 'FHL' in source:
                        sourceType = 'macaques'
                    elif 'Wasp' in source:
                        sourceType = 'wasps' 
                    elif 'Camarena' in source:
                        sourceType = 'pigeons'
                    elif 'Hum' in source:
                        sourceType = 'humans'
                    else:
                        sourceType = 'error'
                        print('Species Error')
                    personName = source + '@' + sourceType
                    if not personName in personsToSuccesses.keys():
                        personsToSuccesses[personName] = {}
                    if not modelName in personsToSuccesses[personName].keys():
                        personsToSuccesses[personName][modelName] = []
                    personsToSuccesses[personName][modelName].append(float(line[12]))

        keylist = [a for a in personsToSuccesses.keys()]
        keylist.sort()
        for pers in keylist:
            for mod in personsToSuccesses[pers].keys():
                if 'train' in mod.split('ing')[0]:
                    continue
                nextLine = pers.split('@')[0] + ',' + str(sum(personsToSuccesses[pers][mod])/len(personsToSuccesses[pers][mod])) + ',' + mod.split('ing')[0] + ','+ pers.split('@')[1] + ',' + mod.split('ing')[1] + ','+str(adaptInTest) + ','+str(onlyLearningPhaseEval) +','+str(allStimuli) + ',' + str(statistics.pstdev(personsToSuccesses[pers][mod]))
                filepratowrite.write(nextLine + '\n')
    filepratowrite.close()


def makeRelForSpecies(adaptInTest, onlyLearningPhaseEval, sources):
    fileParobject=str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "/relational/results/sources" + str(adaptInTest) + str(onlyLearningPhaseEval)+ ".csv" 

    filepratowrite = open(fileParobject, 'w+')

    firstline= 'id,succ,mod,type,mode,adaptInTest,onlyLearningPhaseEval,allStimuli,sd'

    filepratowrite.write(firstline + '\n')
    for allStimuli in [True, False]:
        personsToSuccesses = {}

        for source in sources:
            #adaptInTest = True if 'crm' in source else False 
            print(source)
            first= True
            while os.stat(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "relational/results/resultLearningTIfor" + source+str(adaptInTest) + str(onlyLearningPhaseEval) + ".csv").st_size == 0:
                time.sleep(1)
            sfile= open(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "relational/results/resultLearningTIfor" + source+str(adaptInTest) + str(onlyLearningPhaseEval) + ".csv")
            for listLine in sfile:
                if first: 
                    first = False
                else:
                    line = listLine.split(',')
                    modelName = line[11] + line[0].replace('RL-ELO', 'RL_ELO').replace('resc', 'Resc') 
                    if 'train' in modelName:
                        continue
                    if not allStimuli:
                        if '2' not in line[6] or '4' not in line[6]:
                            continue
                    k = modelName
                    if 'RGMD' in source or 'FHL' in source:
                        sourceType = 'macaques'
                    elif 'Wasp' in source:
                        sourceType = 'wasps' 
                    elif 'Camarena' in source:
                        sourceType = 'pigeons'
                    elif 'Hum' in source:
                        sourceType = 'humans'
                    else:
                        sourceType = 'error'
                        print('Species Error')
                    personName = sourceType + '@' + sourceType
                    if not personName in personsToSuccesses.keys():
                        personsToSuccesses[personName] = {}
                    if not modelName in personsToSuccesses[personName].keys():
                        personsToSuccesses[personName][modelName] = []
                    personsToSuccesses[personName][modelName].append(float(line[12]))

        keylist = [a for a in personsToSuccesses.keys()]
        keylist.sort()
        for pers in keylist:
            for mod in personsToSuccesses[pers].keys():
                if 'train' in mod.split('ing')[0]:
                    continue
                nextLine = pers.split('@')[0] + ',' + str(sum(personsToSuccesses[pers][mod])/len(personsToSuccesses[pers][mod])) + ',' + mod.split('ing')[0] + ','+ pers.split('@')[1] + ',' + mod.split('ing')[1] + ','+str(adaptInTest) + ','+str(onlyLearningPhaseEval) +','+str(allStimuli) + ',' + str(statistics.pstdev(personsToSuccesses[pers][mod]))
                filepratowrite.write(nextLine + '\n')
    filepratowrite.close()


def makeParRelForSpecies(sources):
    fileParobject=str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "/relational/results/params" + ".csv" 

    filepratowrite = open(fileParobject, 'w+')

    firstline= 'species,model,succ,adaptInTest,onlyLearningPhaseEval,allStimuli,meanpars,sd'
    #for a in range(9):
    #    firstline+= ',sd'+str(a) 
    filepratowrite.write(firstline + '\n')
    for allStimuli in [True, False]:
        personsToSuccesses = {}
        personsToPars = {}
        for source in sources:
            #adaptInTest = True if 'crm' in source else False 
            print(source)
            first= True
            sfile= open(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "relational/results/parametersPerPerson.csv" )
            for listLine in sfile:
                if first: 
                    first = False
                else:
                    line = listLine.split(',')
                    modelName = line[4]
                    adaptInTest = 'True' in line[6] 
                    onlyLearningPhaseEval = 'True' in line[3] 
                    #modelName += '_testAdapt' if adaptInTest else '_nonAdapt'
                    #modelName += '_trainOpt' if onlyLearningPhaseEval else '_globOpt'
                    modelName += '+1' if adaptInTest else '+0'
                    modelName += '+1+' if onlyLearningPhaseEval else '+0+'
                    personName = line[1]
                    parsText=line[7]
                    pars = [float(a.split('= ')[1].split('\'')[0]) for a in parsText.split('\'comma \'')]
                    if not personName in personsToSuccesses.keys():
                        personsToSuccesses[personName] = {}
                        personsToPars[personName] = {}
                    if not modelName in personsToSuccesses[personName].keys():
                        personsToSuccesses[personName][modelName] = []
                        personsToPars[personName][modelName] = []
                    personsToSuccesses[personName][modelName].append(float(line[5]))
                    personsToPars[personName][modelName].append(pars)

        keylist = [a for a in personsToSuccesses.keys()]
        keylist.sort()
        for pers in keylist:
            for mod in personsToSuccesses[pers].keys():
                nextLine = pers
                parameters = [statistics.pstdev([n[a] for n in personsToPars[pers][mod]]) for a in range(len(personsToPars[pers][mod][0]))]
                meanpars = [statistics.mean([n[a] for n in personsToPars[pers][mod]]) for a in range(len(personsToPars[pers][mod][0]))]
                for a in [mod.split('+')[0], statistics.mean(personsToSuccesses[pers][mod]), modelName.split('+')[1], modelName.split('+')[2], allStimuli, meanpars, parameters]:
                    nextLine += ',' + str(a).replace(',',';')
                while len(nextLine.split(','))<len(firstline.split(',')):
                    nextLine += ',' + 'nn'
                filepratowrite.write(nextLine + '\n')
    filepratowrite.close()
