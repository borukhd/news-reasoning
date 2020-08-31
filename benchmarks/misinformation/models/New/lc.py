""" News Item Processing model implementation.
"""
import ccobra
from random import random 
import math
from New.sentimentanalyzer import SentimentAnalyzer
from staticCommon import Keys

class LC(ccobra.CCobraModel):
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
        for a in Keys.task:
            if a not in SentimentAnalyzer.relevant:
                self.parameter[a] = 0
        optdict =  {'Exciting_Party_Combined': -3.0933215184624734, 'Familiarity_Party_Combined': 17.83214047528395, 'Importance_Party_Combined': 3.185192558938423, 'Partisanship_All_Combined': 22.939675300159564, 'Partisanship_All_Partisan': 2.0986712022626524, 'Partisanship_Party_Combined': -15.087158032169091, 'Worrying_Party_Combined': -36.55073351519288}
        for a in optdict.keys():
            self.parameter[a] = optdict[a]
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def predictS(self, trial):
        p = 0
        for a in self.parameter.keys():
            p += trial.feature(a) * self.parameter[a] * 0.3
        #if self.thresh < p:
        if 1 < p:
            return 1
            return self.binCorrectCategorization(trial)
        else:
            return 0
            return self.binIncorrectCategorization(trial)

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass