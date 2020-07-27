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

class FFT(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    
    def __init__(self, name='Fast-Frugal-Tree', commands = []):
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
        self.componentKeys = ['Exciting_Party_Combined', 'Familiarity_Party_Combined', 'Partisanship_Party_Combined','Worrying_Party_Combined','Importance_Party_Combined',  'Partisanship_All_Combined', 'Partisanship_All_Partisan']
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def trainModel(self, trialList):
        if FFTtool.fc != None:
            return
        data = self.toDFFormat(trialList)
        compKeys = [a[:3] + a.split('_')[1][:1] + a.split('_')[2][:1] for a in self.componentKeys]
        data.columns = ['crt','ct',#'truthful',
            'cons', 'response'] + SentimentAnalyzer.relevant + compKeys
        cat_columns = ['ct'] #'truthful']
        nr_columns = ['crt', 'cons'] + compKeys  + SentimentAnalyzer.relevant
        for col in cat_columns:
            data[col] = data[col].astype('category')
            for col in nr_columns:
                if data[col].dtype != 'float' and data[col].dtype != 'int':
                    print('type error: ' + data[col])
                    data.loc[data[col] == '?', col] = np.nan
                    data[col] = data[col].astype('float')
        data['response'] = data['response'].apply(lambda x: True if x==1 else False).astype(bool)
        X_train, X_test, y_train, y_test = train_test_split(data.drop(columns='response'), data['response'], test_size= 1, random_state=0)#len(trialList)-
        FFTtool.fc = FastFrugalTreeClassifier(max_levels=5)
        print('Started Fitting Fast-Frugal-Tree')
        FFTtool.fc.fit(X_train, y_train)
        print('   Done Fitting Fast-Frugal-Tree')
        print(FFTtool.fc.get_tree(top10=True,decision_view=True))
        print(FFTtool.fc.get_tree(decision_view=False))

    def toDFFormat(self, trialList):
        featList = []
        for item in trialList:
            if item.conservatism < 3.5:
                componentKeys = [a.replace('Party','Democrats') for a in self.componentKeys]
            if item.conservatism > 3.5:
                componentKeys = [a.replace('Party','Republicans') for a in self.componentKeys]
            newPars = [item.crt, item.conservatism, #int(item.truthful), 
                item.cons, item.birep] + [SentimentAnalyzer.analysis(item)[a] for a in SentimentAnalyzer.relevant] + [item.itemComponents[a] for a in componentKeys]                    
            featList.append(newPars)
        numpy_data = np.array(featList)
        data = pd.DataFrame(data=numpy_data)
        compKeys = [a[:3] + a.split('_')[1][:1] + a.split('_')[2][:1] for a in self.componentKeys]
        data.columns = ['crt','ct',#'truthful',
            'cons', 'response'] + SentimentAnalyzer.relevant + compKeys
        cat_columns = ['ct'] #'truthful']
        nr_columns = ['crt', 'cons'] + compKeys  + SentimentAnalyzer.relevant
        for col in cat_columns:
            data[col] = data[col].astype('category')
            for col in nr_columns:
                if data[col].dtype != 'float' and data[col].dtype != 'int':
                    print('type error: ' + data[col])
                    data.loc[data[col] == '?', col] = np.nan
                    data[col] = data[col].astype('float')
        data['response'] = data['response'].apply(lambda x: True if x==1 else False).astype(bool)
        return data

    def predict(self, trial, **kwargs):
        return
        p = 0
        if self.parameter['thresh'] < p:
            return 'Accept' 
        else:
            return 'Reject'

    def predictS(self, item):
        pred = FFTtool.fc.predict(self.toDFFormat([item]))
        return int(pred[0])

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass