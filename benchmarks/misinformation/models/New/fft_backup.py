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
    
    def __init__(self, name='LinearCombination', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.parameter = {}
        #self.parameter['thresh'] = 10
        self.thresh = 1
        self.componentKeys = ['Exciting_Democrats_Combined', 'Exciting_Republicans_Combined', 'Familiarity_Democrats_Combined', 'Familiarity_Republicans_Combined', 'Importance_Democrats_Combined', 'Importance_Republicans_Combined', 'Likelihood_Democrats_Combined', 'Likelihood_Republicans_Combined', 'Partisanship_All_Combined', 'Partisanship_All_Partisan', 'Partisanship_Democrats_Combined', 'Partisanship_Republicans_Combined', 'Sharing_Democrats_Combined', 'Sharing_Republicans_Combined', 'Worrying_Democrats_Combined', 'Worrying_Republicans_Combined']
        self.componentKeys = ['Exciting_Democrats_Combined', 'Exciting_Republicans_Combined', 'Familiarity_Democrats_Combined', 'Familiarity_Republicans_Combined', 'Importance_Democrats_Combined', 'Importance_Republicans_Combined', 'Partisanship_All_Combined', 'Partisanship_All_Partisan', 'Partisanship_Democrats_Combined', 'Partisanship_Republicans_Combined','Worrying_Democrats_Combined', 'Worrying_Republicans_Combined']
        for a in self.componentKeys:
            self.parameter[a] = 0
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def trainModel(self, trialList):
        if FFTtool.fc != None:
            return
        writefile = open('/home/hippo/git/news-reasoning/benchmarks/misinformation/allItems.data', 'w+')
        for item in trialList:
            newPars = [item.crt, item.conservatism, #int(item.truthful), 
                item.cons, item.birep] + [SentimentAnalyzer.analysis(item)[a] for a in SentimentAnalyzer.relevant] + [item.itemComponents[a] for a in self.componentKeys]                    
            writestring = ''
            for word in newPars:
                writestring += str(word) + ','
            if len(newPars) > 50:
                print(len(newPars))
                continue
            writefile.write(writestring[:-1]+'\n')
        data = pd.read_csv('/home/hippo/git/news-reasoning/benchmarks/misinformation/allItems.data', header=None)
        compKeys = [a[:3] + a.split('_')[1][:1] + a.split('_')[2][:1] for a in self.componentKeys]
        data.columns = ['crt','ct',#'truthful',
            'cons', 'response'] + SentimentAnalyzer.relevant + compKeys
        cat_columns = ['ct']  + SentimentAnalyzer.relevant #'truthful']
            
        nr_columns = ['crt', 'cons'] + compKeys
        for col in cat_columns:
            data[col] = data[col].astype('category')
            for col in nr_columns:
                if data[col].dtype != 'float' and data[col].dtype != 'int':
                    print('type error: ' + data[col])
                    data.loc[data[col] == '?', col] = np.nan
                    data[col] = data[col].astype('float')
        data['response'] = data['response'].apply(lambda x: True if x==1 else False).astype(bool)
        X_train, X_test, y_train, y_test = train_test_split(data.drop(columns='response'), data['response'], test_size=0.3, random_state=0)
        FFTtool.fc = FastFrugalTreeClassifier()
        print('beforefit')
        FFTtool.fc.fit(X_train, y_train)
        print('afterfit')
        print(FFTtool.fc.get_tree())
        print(FFTtool.fc.score(X_test, y_test))



    def predict(self, trial, **kwargs):
        p = 0
        for a in self.componentKeys:
            p += trial.itemComponents[a] * self.parameter[a]
        if self.parameter['thresh'] < p:
            return 'Accept' 
        else:
            return 'Reject'

    def predictS(self, item):
        newPars = [item.crt, item.conservatism, int(item.truthful), item.cons, item.birep] + [SentimentAnalyzer.analysis(item)[a] for a in SentimentAnalyzer.relevant] + [item.itemComponents[a] for a in self.componentKeys]                    

        return FFT.fc.predict(item)

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass