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

finaltree = None

class FFTmax(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    
    def __init__(self, name='Fast-Frugal-Tree-Max', commands = []):
        """ Initializes the TransitivityInt model.
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
        self.componentKeys = [a for a in self.componentKeys if 'gender' not in a and 'haring' not in a]
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
        predictionQuality, predictionMargin = {'>crt': -0.5765148663906662, '<crt': -0.5835007682307056, '>conservatism': -0.5840998087605864, '<conservatism': -0.576172936416883, '>ct': -0.5755846761552449, '<ct': -0.6117876278616659, '>education': -0.6196549137284321, '<education': -0.576172936416883, '>gender': -0.5751785605274403, '<gender': -0.6629834254143646, '>accimp': -0.6245434623813002, '<accimp': -0.576257736867164, '>panasPos': -0.423766680755993, '<panasPos': -0.576172936416883, '>panasNeg': -0.423766680755993, '<panasNeg': -0.576172936416883, '>Exciting_Party_Combined': -0.6378066378066378, '<Exciting_Party_Combined': -0.6442516268980477, '>Familiarity_Party_Combined': -0.8807965084560829, '<Familiarity_Party_Combined': -0.576172936416883, '>Importance_Party_Combined': -0.9197396963123644, '<Importance_Party_Combined': -0.7952691680261011, '>Partisanship_All_Combined': -0.824295010845987, '<Partisanship_All_Combined': -0.7604868506846337, '>Partisanship_All_Partisan': -0.824295010845987, '<Partisanship_All_Partisan': -0.7213447326474424, '>Partisanship_Party_Combined': -0.9166666666666666, '<Partisanship_Party_Combined': -0.7128539213229766, '>Worrying_Party_Combined': -0.576172936416883, '<Worrying_Party_Combined': -0.7948717948717948}, {'>crt': 0.9611886396917466, '<crt': 0.6196903610860507, '>conservatism': 3.5312980367111253, '<conservatism': 0.0, '>ct': 5.0, '<ct': 4.227544258038495, '>education': 2.2412854095104953, '<education': 0.0, '>gender': 4.550795699820794, '<gender': 5.0, '>accimp': 1.7730933959075976, '<accimp': 5.0, '>panasPos': 0.0, '<panasPos': 0.0, '>panasNeg': 0.0, '<panasNeg': 0.0, '>Exciting_Party_Combined': 1.9445809043351385, '<Exciting_Party_Combined': 3.2554860566661565, '>Familiarity_Party_Combined': 2.2340655206116744, '<Familiarity_Party_Combined': 0.0, '>Importance_Party_Combined': 2.271886359375083, '<Importance_Party_Combined': 4.180200375448119, '>Partisanship_All_Combined': 4.098278058073108, '<Partisanship_All_Combined': 3.825921609404447, '>Partisanship_All_Partisan': 1.2084637950209594, '<Partisanship_All_Partisan': 0.8947571888022123, '>Partisanship_Party_Combined': 4.263257855394618, '<Partisanship_Party_Combined': 3.8420666367941125, '>Worrying_Party_Combined': 5.0, '<Worrying_Party_Combined': 3.937920683250629}

        orderedConditions = []
        for a in sorted(predictionQuality.items(), key=lambda x: x[1], reverse=False):
            if a[0][1:] not in [i[1:] for i in orderedConditions] and a[0][1:] in self.componentKeys:
                orderedConditions.append(a[0])
        for sa in orderedConditions[:maxLength] if maxLength > 0 else orderedConditions:
            b = sa[1:]
            s = sa[0]
            #print('item.feature(\'', b, '\') ', s, ' ', str(predictionMargin[sa]), str(predictionQuality[sa]))
            cond = 'item.feature(\'' + b + '\') ' + s + ' ' + str(predictionMargin[sa])
            newnode = Node(cond,True,False)
            rep0preds, rep1preds, length0, length1 = predictiveQuality(newnode, trialList)
            #print(rep1preds/length1, rep0preds/length0, rep1preds,length1, rep0preds, length0)
            if self.fft == None:
                self.fft = newnode
                self.lastnode = self.fft
            else:
                if rep1preds/length1 >= rep0preds/length0:
                    self.lastnode.left = newnode
                    self.lastnode = self.lastnode.left
                elif rep1preds/length1 <= rep0preds/length0:
                    self.lastnode.right = newnode
                    self.lastnode = self.lastnode.right
        FFTmax.MAX = self.fft
        print(FFTmax.MAX.getstring())

    def predictS(self, item, person='global'):
        return FFTmax.MAX.run(item)

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