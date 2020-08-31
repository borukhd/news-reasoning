""" News Item Processing model implementation.
"""
import ccobra
from random import random 
import math
import numpy as np
import pandas as pd
from New.sentimentanalyzer import SentimentAnalyzer
from fasttrees.fasttrees import FastFrugalTreeClassifier
from sklearn.model_selection import train_test_split
from New.fftTool import FFTtool
from staticCommon import Keys
from scipy.optimize import * 

class FFTzigzag(ccobra.CCobraModel):
    """ FFTzigzag CCOBRA implementation.
    """
    
    def __init__(self, name='Fast-Frugal-Tree-ZigZag(Z+)', commands = []):
        """ Initializes the model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        SentimentAnalyzer.initialize()
        self.parameter = {}
        #self.parameter['thresh'] = 1
        self.fft = None
        self.lastnode = None
        self.componentKeys = Keys.person + Keys.task 
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def pre_train(self, dataset):
        print('Pretrain started')
        trialList = []
        for pers in dataset:
            trialList.extend([a['item'] for a in pers if 'NoInfo' not in [a['item'].feature(f) for f in self.componentKeys]])
        return self.fitTreeOnTrials(trialList)

    def fitTreeOnTrials(self, trialList, maxLength=-1, person='global'):
        maxLength = -1
        predictionQuality = {}
        predictionMargin = {}
        """
        for a in self.componentKeys:
            marginOptimum = basinhopping(parametrizedPredictiveQualityLT, [0.00], niter=60, stepsize=3.0, T=.9, minimizer_kwargs={"args" : (a,trialList), "tol":0.001, "bounds" : [[0,5]]},disp=0)
            predictionMargin['>' + a] = marginOptimum.x[0]
            predictionQuality['>' + a] = marginOptimum.fun
            marginOptimum = basinhopping(parametrizedPredictiveQualityST, [0.00], niter=60, stepsize=3.0, T=.9, minimizer_kwargs={"args" : (a,trialList), "tol":0.001, "bounds" : [[0,5]]},disp=0)
            predictionMargin['<' + a] = marginOptimum.x[0]
            predictionQuality['<' + a] = marginOptimum.fun
        print(predictionQuality, predictionMargin)
        """
        predictionQuality, predictionMargin = {'>crt': -0.499969808586438, '<crt': -0.499969808586438, '>conservatism': -0.499969808586438, '<conservatism': -0.499969808586438, '>ct': -0.499969808586438, '<ct': -0.499969808586438, '>education': -0.499969808586438, '<education': -0.499969808586438, '>accimp': -0.499969808586438, '<accimp': -0.499969808586438, '>panasPos': -0.499969808586438, '<panasPos': -0.499969808586438, '>panasNeg': -0.499969808586438, '<panasNeg': -0.499969808586438, '>Exciting_Party_Combined': -0.499969808586438, '<Exciting_Party_Combined': -0.9967320261437909, '>Familiarity_Party_Combined': -0.9996378123868164, '<Familiarity_Party_Combined': -0.499969808586438, '>Importance_Party_Combined': -0.9978308026030369, '<Importance_Party_Combined': -0.7963446475195822, '>Partisanship_All_Combined': -0.9978308026030369, '<Partisanship_All_Combined': -0.777589954117363, '>Partisanship_All_Partisan': -0.9978308026030369, '<Partisanship_All_Partisan': -0.9997585124366095, '>Partisanship_Party_Combined': -0.9967845659163987, '<Partisanship_Party_Combined': -0.7990093847758082, '>Worrying_Party_Combined': -0.499969808586438, '<Worrying_Party_Combined': -0.9935897435897436}, {'>crt': 1.972872196401318, '<crt': 0.0, '>conservatism': 0.0, '<conservatism': 0.0, '>ct': 0.0, '<ct': 0.0, '>education': 0.0, '<education': 0.0, '>accimp': 0.0, '<accimp': 0.0, '>panasPos': 0.0, '<panasPos': 0.0, '>panasNeg': 0.0, '<panasNeg': 0.0, '>Exciting_Party_Combined': 0.0, '<Exciting_Party_Combined': 3.574226008657847, '>Familiarity_Party_Combined': 2.6042025215277933, '<Familiarity_Party_Combined': 0.0, '>Importance_Party_Combined': 2.2036394876853738, '<Importance_Party_Combined': 4.255574086579121, '>Partisanship_All_Combined': 1.965200689848336, '<Partisanship_All_Combined': 3.8353730503393244, '>Partisanship_All_Partisan': 1.2298451980672356, '<Partisanship_All_Partisan': 0.7176463353940941, '>Partisanship_Party_Combined': 4.223723273224007, '<Partisanship_Party_Combined': 3.885513240139143, '>Worrying_Party_Combined': 0.0, '<Worrying_Party_Combined': 1.6378138233962547}

        orderedConditionsPos = []
        orderedConditionsNeg = []
        for a in sorted(predictionQuality.items(), key=lambda x: x[1], reverse=False):
            b = a[0][1:]
            s = a[0][0]
            cond = 'item.feature(\'' + b + '\') ' + s + ' ' + str(predictionMargin[a[0]])
            newnode = Node(cond,True,False)
            rep0preds, rep1preds, length0, length1 = predictiveQuality(newnode, trialList)
            if rep1preds/length1 >= rep0preds/length0:
                if a[0][1:] not in [i[1:] for i in orderedConditionsPos + orderedConditionsNeg] and a[0][1:] in self.componentKeys:
                    orderedConditionsPos.append(a[0])
            else:
                if a[0][1:] not in [i[1:] for i in orderedConditionsNeg +orderedConditionsPos] and a[0][1:] in self.componentKeys:
                    orderedConditionsNeg.append(a[0])
        orderedConditions = []
        for i in range(max(len(orderedConditionsNeg), len(orderedConditionsPos))):
            if len(orderedConditionsNeg) > i:
                orderedConditions.append(orderedConditionsNeg[i])
            if len(orderedConditionsPos) > i:
                orderedConditions.append(orderedConditionsPos[i])
        exitLeft = True
        for sa in orderedConditions[:maxLength] if maxLength > 0 else orderedConditions:
            b = sa[1:]
            s = sa[0]
            #print('item.feature(\'', b, '\') ', s, ' ', str(predictionMargin[sa]), str(predictionQuality[sa]))
            cond = 'item.feature(\'' + b + '\') ' + s + ' ' + str(predictionMargin[sa])
            newnode = Node(cond,True,False)
            if self.fft == None:
                self.fft = newnode
                self.lastnode = self.fft
            else:
                if not exitLeft:
                    self.lastnode.left = newnode
                    self.lastnode = self.lastnode.left
                else:
                    self.lastnode.right = newnode
                    self.lastnode = self.lastnode.right
            exitLeft = not exitLeft
        FFTtool.ZIGZAG = self.fft
        print(FFTtool.ZIGZAG.getstring())

    def predictS(self, item, person='global'):
        return FFTtool.ZIGZAG.run(item)

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass

def parametrizedPredictiveQualityLT(margin, a, trialList):
    node = Node('item.feature(\'' + a + '\') > ' + str(margin[0]), True, False)
    rep0preds, rep1preds, length0, length1 = predictiveQuality(node, trialList)
    return -1*max(rep0preds/length0, rep1preds/length1)
def parametrizedPredictiveQualityST(margin, a, trialList):
    node = Node('item.feature(\'' + a + '\') < ' + str(margin[0]), True, False)
    rep0preds, rep1preds, length0, length1 = predictiveQuality(node, trialList)
    return -1*max(rep0preds/length0, rep1preds/length1)


def predictiveQuality(node, trialList):
    rep0preds = 0
    rep1preds = 0
    length0 = 1
    length1 = 1
    for item in trialList:
        if 1 == node.run(item):
            rep1preds += int(bool(item.truthful == 1))
            length1 += 1
        else:
            rep0preds += int(bool(item.truthful == 0))
            length0 += 1
    return rep0preds, rep1preds, length0, length1

class Node:
    def __init__(self, conditionstr, left, right):
        self.condition = conditionstr
        self.left = left
        self.right = right
    
    def run(self, item):
        if eval(self.condition):
            if isinstance(self.left,bool):
                return self.left
            return self.left.run(item)
        else:
            if isinstance(self.right,bool):
                return self.right
            return self.right.run(item)

    def getstring(self):
        a = ''
        if isinstance(self.left,bool):
            a = 'If ' + self.condition.split('\'')[1] + self.condition.split(')')[1] + ' then return ' + str(self.left) + ', else: ' 
            a += 'Return ' + str(self.right) if isinstance(self.right,bool) else self.right.getstring()
        else:
            a = 'If ' + self.condition.split('\'')[1] + self.condition.split(')')[1] + ' then return ' + str(self.right) + ', else: '
            a += 'Return ' + str(self.left) if isinstance(self.left,bool) else self.left.getstring()

        return a 