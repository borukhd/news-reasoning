from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, plot_tree
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
from New.dtTool import DTtool
from staticCommon import Keys
import matplotlib.pyplot as plt



class DT(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    
    def __init__(self, name='Meta-DecisionTree', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        SentimentAnalyzer.initialize()
        self.parameter = {}
        self.componentKeys = Keys.person + Keys.task
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def pre_train(self, dataset):
        print('Pretrain started')
        trialList = []
        for pers in dataset:
            trialList.extend([a['item'] for a in pers])
        print('Trial list length:',len(trialList))
        return self.fitTreeOnTrials(trialList)




    def fitTreeOnTrials(self, trialList, person='global'):
        if person in DTtool.dc.keys():
            return
        data = self.toDTormat(trialList)
        print(sorted(data.columns))
        DTtool.dc[person] = tree.DecisionTreeClassifier(max_depth=7, max_leaf_nodes=4)
        print('Started Fitting Decision-Tree')
        DTtool.dc[person].fit(data.drop(columns='response'), data['response'])
        print('   Done Fitting Decision-Tree')
        plt.figure(figsize=(20,20))
        tree.plot_tree(DTtool.dc[person], filled=True, fontsize=10, feature_names=data.drop(columns='response').keys()) 
        print('                Decision-Tree plotted')
        plt.savefig('/home/hippo/git/news-reasoning/benchmarks/misinformation/decision-tree.png')
        print('                Decision-Tree saved')





    def toDTormat(self, trialList):
        featList = []
        for item in trialList:
            newPars = [item.birep] + [item.feature(a) for a in item.featurekeys()]
            featList.append(newPars)
        cat_columns = [] 
        nr_columns = [a for a in self.componentKeys
            if a not in cat_columns]
        data_columns = ['response'] +cat_columns + nr_columns
        data = pd.DataFrame(data=featList, columns=data_columns)
        #print(data)
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
        pred = DTtool.dc[person].predict(self.toDTormat([item]).drop(columns='response'))
        return int(pred[0])

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass