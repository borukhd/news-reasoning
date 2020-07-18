from ..models.MotivatedReasoning import ms2r
import ccobra.benchmark.runner as starter
from scipy.optimize import *
from ..scripts.relationMaker import *
from ..scripts.relationPlotter import *
import os
from multiprocessing import Pool
import time
import warnings
import pathlib

#warnings.filterwarnings("ignore")

sources = [ms2r]

assModels = [ SCT,CorrectReply, RLELO,Trabasso,RWWy,RLELO_F,VTTBS,  DeSoto, SCTinterpr, SiemannDelius,  BushMosteller, CCW, RWBS, RandomModel]

modelParameters = {
    RLELO : ['a', 'b'],#, 'vInit'],
    RLELO_F : ['a', 'b', 's'],#, 'vInit'],
    SiemannDelius : ['bMinus', 'bPlus', 'e'],#, 'elemVinit', 'confVinit'],
    RWBS : ['a', 'b'],#, 'vInit'],
    RWWy : ['a', 'B'],#, 'vInit'],
    CCW : ['a', 'B', 'y'],#, 'vInit'],
    VTTBS : ['a', 'b', 't'],#, 'vInit'],
    BushMosteller : ['Db'],#, 'vInit']
    CorrectReply : ['a'],
    RandomModel : ['a'],
    Trabasso : ['h'], 
    DeSoto : ['a'], 
    SCTinterpr : ['a'], 
    SCT : ['a']
    }

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
class Optimizer():
    def __init__(self):
        self.saveTm = {}

    def modelLearningSuccFAllP(modelT, source, comms = '', adaptInTest = True, onlytrainingPhaseEval = True, onlyTestingPhaseEval = True):
        dataFileTraining = open(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + 'relational/data/' + source + '-TI.csv')
        successesInt = {}        
        peopleToModelInstances = {}
        counter = -1 
        rightAnswers = 0
        totalAnswers = 0
        trainingPhase = True
        testPhase = False
        for line in dataFileTraining:
            if counter < 0:
                indexOfId = line.split(',').index('id') if 'id' in line.split(',') else line.split(',').index('Id')
                indexOfResponse = line.split(',').index('response\n') if 'response\n' in line.split(',') else line.split(',').index('response')
                indexOfPhase = None
                for phaseWord in ['phase\n', 'phase', 'Phase\n', 'Phase']:
                    if phaseWord in line.split(','):
                        indexOfPhase = line.split(',').index(phaseWord) 
                        break
                indexOfTrial = None
                for phaseWord in ['trial\n', 'trial', 'Trial\n', 'Trial']:
                    if phaseWord in line.split(','):
                        indexOfTrial = line.split(',').index(phaseWord) 
                indexOfPhaseType = None
                for phaseWord in ['phasetype\n', 'phasetype', 'Phasetype\n', 'Phasetype', 'phaseType\n', 'phaseType', 'PhaseType\n', 'PhaseType']:
                    if phaseWord in line.split(','):
                        indexOfPhaseType = line.split(',').index(phaseWord) 
                        break
                indexOfTask = line.split(',').index('choices')
            else:
                if indexOfPhase and str(line.split(',')[indexOfPhase]) != "-":
                    if indexOfPhaseType:
                        trainingPhase = True if int(line.split(',')[indexOfPhase]) <= 2 else False
                    else:    
                        trainingPhase = True if int(line.split(',')[indexOfPhase]) % 2 == 1 else False
                elif indexOfTrial:
                    if int(line.split(',')[indexOfTrial]) < 0:
                        trainingPhase = True
                    else:
                        trainingPhase = False
                if 'isTesting' in line:
                    trainingPhase = not bool(eval(line.split(',')[line.split(',').index('isTesting')]))
                testPhase = not trainingPhase
                task = line.split(',')[indexOfTask].split('|')
                currentPerson = "personNo" + str(line.split(',')[indexOfId]) + source
                currentPerson += ';' + str(int(line.split(',')[indexOfPhase]) % 2 -(int(line.split(',')[indexOfPhase]) % 2) ) if indexOfPhase else 'noPhase'
                if currentPerson not in peopleToModelInstances.keys():
                    peopleToModelInstances[currentPerson] = modelT(commands=comms)
                if not (onlytrainingPhaseEval and testPhase):
                    pred = peopleToModelInstances[currentPerson].predictS(task)
                    rightAnswers += min(1, max(0,pred)) if int(task[0]) == int(line.split(',')[indexOfResponse]) else 1 - min(1, max(0,pred))
                    totalAnswers += 1
                if adaptInTest or trainingPhase:
                    peopleToModelInstances[currentPerson].adaptS(task)
            counter += 1
        return rightAnswers/totalAnswers if totalAnswers != 0 else 0

    def modelLearningSuccOneP(modelT, source, comms = '', adaptInTest = True, onlytrainingPhaseEval = True, pers = None):
        if not pers:
            print("No person specified")
        dataFileTraining = open(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + 'relational/data/' + source + '-TI.csv')
        successesInt = {}        
        peopleToModelInstances = {}
        counter = -1 
        rightAnswers = 0
        totalAnswers = 0
        trainingPhase = True
        testPhase = False
        for line in dataFileTraining:
            if counter < 0:
                indexOfId = line.split(',').index('id') if 'id' in line.split(',') else line.split(',').index('Id')
                indexOfResponse = line.split(',').index('response\n') if 'response\n' in line.split(',') else line.split(',').index('response')
                indexOfPhase = None
                for phaseWord in ['phase\n', 'phase', 'Phase\n', 'Phase']:
                    if phaseWord in line.split(','):
                        indexOfPhase = line.split(',').index(phaseWord) 
                        break
                indexOfMode = None
                for phaseWord in ['isTesting\n', 'isTesting']:
                    if phaseWord in line.split(','):
                        indexOfMode = line.split(',').index(phaseWord) 
                indexOfTrial = None
                for phaseWord in ['trial\n', 'trial', 'Trial\n', 'Trial']:
                    if phaseWord in line.split(','):
                        indexOfTrial = line.split(',').index(phaseWord) 
                indexOfPhaseType = None
                for phaseWord in ['phasetype\n', 'phasetype', 'Phasetype\n', 'Phasetype', 'phaseType\n', 'phaseType', 'PhaseType\n', 'PhaseType']:
                    if phaseWord in line.split(','):
                        indexOfPhaseType = line.split(',').index(phaseWord) 
                        break
                indexOfTask = line.split(',').index('choices')
            else:
                if line.split(',')[indexOfId] != pers:
                    continue
                if indexOfPhase and str(line.split(',')[indexOfPhase]) != "-":
                    if indexOfPhaseType:
                        trainingPhase = True if int(line.split(',')[indexOfPhase]) <= 2 else False
                    else:    
                        trainingPhase = True if int(line.split(',')[indexOfPhase]) % 2 == 1 else False
                elif indexOfTrial:
                    if int(line.split(',')[indexOfTrial]) < 0:
                        trainingPhase = True
                    else:
                        trainingPhase = False
                if indexOfMode:
                    trainingPhase = not bool(eval(line.split(',')[indexOfMode]))
                testPhase = not trainingPhase
                task = line.split(',')[indexOfTask].split('|')
                currentPerson = "personNo" + str(line.split(',')[indexOfId]) + source
                currentPerson += ';' + str(int(line.split(',')[indexOfPhase]) % 2 -(int(line.split(',')[indexOfPhase]) % 2) ) if indexOfPhase else 'noPhase'
                if currentPerson not in peopleToModelInstances.keys():
                    peopleToModelInstances[currentPerson] = modelT(commands=comms)
                peopleToModelInstances[currentPerson] = peopleToModelInstances[currentPerson].execute(line.split(',')[indexOfId])
                if not (onlytrainingPhaseEval and testPhase):
                    pred = peopleToModelInstances[currentPerson].predictS(task)
                    rightAnswers += min(1, max(0,pred)) if int(task[0]) == int(line.split(',')[indexOfResponse]) else 1 - min(1, max(0,pred))
                    totalAnswers += 1
                if adaptInTest or trainingPhase:
                    peopleToModelInstances[currentPerson].adaptS(task)
            counter += 1
        return rightAnswers/totalAnswers if totalAnswers != 0 else 0

    def objective(x, source, modelT, adaptInTest = True, onlytrainingPhaseEval = True):
        pCount = 0
        comms = {}
        comms[str(modelT).split('.')[-1].split('\'')[0]] = ['self.adaptInTesting = ' + str(adaptInTest)]
        for par in modelParameters[modelT]:
            comms[str(modelT).split('.')[-1].split('\'')[0]].append('self.' + par + ' = ' + str(x[pCount]))
            pCount += 1
        modelRes = Optimizer.modelLearningSuccFAllP(modelT, source, str(comms), adaptInTest=adaptInTest, onlytrainingPhaseEval=onlytrainingPhaseEval)
        return (-1)*modelRes
    def objectiveInd(x, source, modelT, adaptInTest = True, onlytrainingPhaseEval = True, thisId = None):
        pCount = 0
        comms = {}
        comms[str(modelT).split('.')[-1].split('\'')[0] + str(thisId)] = ['self.adaptInTesting = ' + str(adaptInTest)]
        for par in modelParameters[modelT]:
            comms[str(modelT).split('.')[-1].split('\'')[0] + str(thisId)].append('self.' + par + ' = ' + str(x[pCount]))
            pCount += 1
        modelRes = Optimizer.modelLearningSuccOneP(modelT, source, str(comms), adaptInTest=adaptInTest, onlytrainingPhaseEval=onlytrainingPhaseEval, pers=thisId)
        return (-1)*modelRes

    def calculateOptimizationT(tupleInp):
        print('Initialized optimization.')
        adaptInTest,onlytrainingPhaseEval, source = eval(tupleInp)
        return Optimizer.calculateOptimization(adaptInTest,onlytrainingPhaseEval, source)
    def calculateOptimization(adaptInTest,onlytrainingPhaseEval, source):
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
        print('Started optimization for ' + source + ', species: ' + sourceType)
        fileBenchmarkOptimizedpars =str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "relational/results/parametersPerPerson.csv" 
        dataFileTraining = open(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + 'relational/data/' + source + '-TI.csv')
        first = True
        listOfIds = []
        for line in dataFileTraining:
            if first:
                first = False
                idInd = line.split(',').index('id') if 'id' in line.split(',') else line.split(',').index('Id')
                continue
            newId = line.split(',')[idInd]
            if newId not in listOfIds:
                listOfIds.append(newId)
        optCommands = {}
        for model in assModels: #
            for eachId in listOfIds:
                fileparwrite = open(fileBenchmarkOptimizedpars, 'a')
                mName = str(model).split('.')[-1].split('\'')[0]
                print(str(mName))
                #print('started', eachId, source, mName, 'optimization', adaptInTest,onlytrainingPhaseEval)
                testResult = [0.5]*len(modelParameters[model])
                fileparwritechecker = open(fileBenchmarkOptimizedpars, 'r')
                #for line in fileparwritechecker:
                #    if line.split(',')[0] + line.split(',')[1] == mName + eachId:
                #        optCommands[mName + eachId] = exec(line.split(',')[6].replace('comma',','))
                if mName + eachId not in optCommands.keys():
                    if 'ando' not in mName and 'orrec' not in mName:
                        parOpt = minimize(Optimizer.objectiveInd, testResult, method='cobyla', options={'maxiter' : 20, 'tol' : 0.001}, args = (source,model, adaptInTest, onlytrainingPhaseEval, eachId))#, bounds = modelBounds[model])
                        optCommands[mName + eachId] = ['self.' + modelParameters[model][a] + ' = ' + str(parOpt.x[a]) for a in range(len(parOpt.x))] + ['self.adaptInTesting = ' + str(adaptInTest)]
                        print(source + ',' + sourceType + ',' + str(eachId) + ',' +  str(onlytrainingPhaseEval) + ',' +  mName + ',' +  str((-1)*parOpt.fun) + ',' + str(adaptInTest) + ',' + str(optCommands[mName + eachId][:-1]).replace(',','comma') + '\n')
                        fileparwrite.write(source + ',' + sourceType + ',' + str(eachId) + ',' +  str(onlytrainingPhaseEval) + ',' +  mName + ',' +  str((-1)*parOpt.fun) + ',' + str(adaptInTest) + ',' + str(optCommands[mName + eachId][:-1]).replace(',','comma') + '\n')
                    else:
                        optCommands[mName + eachId] = ['self.a = ' + '0']
                        print(source + ',' + sourceType + ',' +str(eachId) + ',' +  str(onlytrainingPhaseEval) + ',' +  mName + ',' +  str((-1)*Optimizer.objectiveInd([0], source,model, adaptInTest, onlytrainingPhaseEval, eachId)) + ',' + str(adaptInTest) + ',' + str(optCommands[mName + eachId]).replace(',','comma'))
                        fileparwrite.write(source + ',' + sourceType + ',' +str(eachId) + ',' +  str(onlytrainingPhaseEval) + ',' +  mName + ',' +  str((-1)*Optimizer.objectiveInd([0], source,model, adaptInTest, onlytrainingPhaseEval, eachId)) + ',' + str(adaptInTest) + ',' + str(optCommands[mName + eachId]).replace(',','comma') + '\n')
                fileparwritechecker.close()
                fileparwrite.close()
        fileobject=str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "relational/benchmarkFor"+ source +str(adaptInTest) + str(onlytrainingPhaseEval)+".json" 
        filetowrite = open(fileobject, 'w+')
        filetowrite.write("""{
        \"data.train\": \"data/""" + 'empty' + """-TI.csv\",
        \"data.test\": \"data/""" + source + """-TI.csv\",
        \"corresponding_data\": false,
        \"domains\": [\"spacional-relational\"],
        \"response_types\": [\"single-choice\"],
        \"models\": [
            \"models/TransitiveInference/SCT.py\",
            \"models/TransitiveInference/RLELO.py\",
            \"models/TransitiveInference/RLELO_F.py\",
            \"models/TransitiveInference/siemannDelius.py\",
            \"models/TransitiveInference/RescorlaWagnerBS.py\",
            \"models/TransitiveInference/RescorlaWagnerWynne95.py\",
            \"models/TransitiveInference/valueTransferTheoryBS.py\",
            \"models/TransitiveInference/BushMosteller.py\",
            \"models/TransitiveInference/configuralCuesWynne95.py\",
            \"models/TransitiveInference/trueAnswer.py\",
            \"models/TransitiveInference/random_model.py\",
            \"models/TransitiveInference/Trabasso.py\",
            \"models/TransitiveInference/SCTinterpr.py\",
            \"models/TransitiveInference/DeSoto.py\"
        ]}""")
        filetowrite.close()
        starter.main(str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "ccobra -p " + str(optCommands).replace(' ','X') + " -s " + str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "relational/results/resultLearningTIfor" + source +  str(False) + str(onlytrainingPhaseEval) + ".csv -o html "+ str(pathlib.Path(__file__).parent.absolute()).split('relational/')[0] + "relational/benchmarkFor"+ source + str(adaptInTest) + str(onlytrainingPhaseEval)+".json")
        print('Finished optimization for ' + source + ', species: ' + sourceType)

def main():
    print('Commenced result calculation.')
    fileBenchmarkOptimizedpars ="parametersFinalPerPerson.csv" 
    fileparwrite = open(fileBenchmarkOptimizedpars, 'w+')
    fileparwrite.write('source,type,id,onlyTrainingOptimization,model,performance,adaptModelInTesting,parameters\n')
    fileparwrite.close()
    procs = 1
    pool = Pool(procs)
    p = [] 
    for adaptInTest in [False, True]:
        continue
        for onlytrainingPhaseEval in [True]:#,False]:
            for source in sources:# ['HumScrmNew']:#
                mnipulatedForHumSpec = str(True) if 'crm' in source else str(adaptInTest)
                p += [mnipulatedForHumSpec + ',' + str(onlytrainingPhaseEval) + ',\'' + str(source) + '\'']
    pool.map(Optimizer.calculateOptimizationT, p)
    print('Generated process pool.')
    pool.close()
    pool.join() 
    print('Result calculation completed.')

    divisions = 8
    for adaptInTest in [False]:
        for onlytrainingPhaseEval in [True]:#,False]:
            makeObjectiveIntvls(adaptInTest,onlytrainingPhaseEval, sources, 1)
            makeRelForModels(adaptInTest,onlytrainingPhaseEval,sources)
            makeRelForSources(adaptInTest,onlytrainingPhaseEval,sources)
            makeRelForSpecies(adaptInTest,onlytrainingPhaseEval,sources)
            for a in [True]:
                for b in [False]:
                    makeIntvls(adaptInTest, onlytrainingPhaseEval, sources, divisions, a, b)
                    makeIntervalGraph(adaptInTest, onlytrainingPhaseEval, divisions, a, b)
                    makeRelForSwpl(adaptInTest, onlytrainingPhaseEval, sources, a, b)
                    makeBoxplots(adaptInTest, onlytrainingPhaseEval, a, b)
    makeParRelForSpecies(sources)

if __name__ == '__main__':
    main()
