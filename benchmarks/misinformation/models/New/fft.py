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

class FFTifan(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    
    def __init__(self, name='Fast-Frugal-Tree-ifan', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        SentimentAnalyzer.initialize()
        self.parameter = {}
        #self.parameter['thresh'] = 10
        self.componentKeys = Keys.person + Keys.task
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def pre_train(self, dataset):
        print('Pretrain started')
        trialList = []
        for pers in dataset:
            trialList.extend([a['item'] for a in pers if 'NoInfo' not in [a['item'].feature(f) for f in self.componentKeys]])
        return self.fitTreeOnTrials(trialList)

    def fitTreeOnTrials(self, trialList, person='global'):
        if person in FFTtool.fc.keys():
            return
        data = self.toDFFormatTruthful(trialList)
        FFTtool.fc[person] = FastFrugalTreeClassifier(max_levels=5)
        print('Started Fitting Fast-Frugal-Tree')
        FFTtool.fc[person].fit(data.drop(columns='response'), data['response'])
        print('   Done Fitting Fast-Frugal-Tree')
        #print(FFTtool.fc[person].get_tree(top10=True,decision_view=True))
        #print(FFTtool.fc[person].get_tree(decision_view=False))

    def toDFFormat(self, trialList):
        featList = []
        for item in trialList:
            newPars = [item.birep] + [item.feature(a) for a in self.componentKeys]
            featList.append(newPars)
        cat_columns = [] 
        nr_columns = [a for a in self.componentKeys
            if a not in cat_columns]
        data_columns = ['response'] +cat_columns + nr_columns
        data = pd.DataFrame(data=featList, columns=data_columns)
        for col in cat_columns:
            data[col] = data[col].astype('category')
            for col in nr_columns:
                if data[col].dtype != 'float' and data[col].dtype != 'int':
                    print('type error: ' + data[col])
                    data.loc[data[col] == '?', col] = np.nan
                    data[col] = data[col].astype('float')
        data['response'] = data['response'].apply(lambda x: True if x==1 else False).astype(bool)
        return data
        
    def toDFFormatTruthful(self, trialList):
        featList = []
        for item in trialList:
            newPars = [item.truthful] + [item.feature(a) for a in self.componentKeys]
            featList.append(newPars)
            for a in newPars[1:]:
                if type(a) == type('hi'):
                    print('FOUND ERROR:', a, type(a))
        cat_columns = [] 
        nr_columns = [a for a in self.componentKeys
            if a not in cat_columns]
        data_columns = ['response'] +cat_columns + nr_columns
        data = pd.DataFrame(data=featList, columns=data_columns)
        for col in cat_columns:
            data[col] = data[col].astype('category')
            for col in nr_columns:
                if data[col].dtype != 'float' and data[col].dtype != 'int':
                    print('type error: ' + data[col])
                    data.loc[data[col] == '?', col] = np.nan
                    data[col] = data[col].astype('float')
        data['response'] = data['response'].apply(lambda x: True if x==1 else False).astype(bool)
        return data

    def predictS(self, item, person='global'):
        pred = FFTtool.fc[person].predict(self.toDFFormat([item]))
        return int(pred[0])

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass