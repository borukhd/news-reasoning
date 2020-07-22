""" News Item Processing model implementation.
"""
import ccobra
from random import random 
import math

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
        self.componentKeys = ['Exciting_Democrats_Combined', 'Exciting_Republicans_Combined', 'Familiarity_Democrats_Combined', 'Familiarity_Republicans_Combined', 'Importance_Democrats_Combined', 'Importance_Republicans_Combined', 'Likelihood_Democrats_Combined', 'Likelihood_Republicans_Combined', 'Partisanship_All_Combined', 'Partisanship_All_Partisan', 'Partisanship_Democrats_Combined', 'Partisanship_Republicans_Combined', 'Sharing_Democrats_Combined', 'Sharing_Republicans_Combined', 'Worrying_Democrats_Combined', 'Worrying_Republicans_Combined']
        self.componentKeys = ['Exciting_Democrats_Combined', 'Exciting_Republicans_Combined', 'Familiarity_Democrats_Combined', 'Familiarity_Republicans_Combined', 'Importance_Democrats_Combined', 'Importance_Republicans_Combined', 'Partisanship_All_Combined', 'Partisanship_All_Partisan', 'Partisanship_Democrats_Combined', 'Partisanship_Republicans_Combined','Worrying_Democrats_Combined', 'Worrying_Republicans_Combined']
        for a in self.componentKeys:
            self.parameter[a] = 0
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def predict(self, trial, **kwargs):
        p = 0
        for a in self.componentKeys:
            p += trial.itemComponents[a] * self.parameter[a]
        if self.parameter['thresh'] < p:
            return 'Accept' 
        else:
            return 'Reject'

    def predictS(self, trial):
        #print(trial.itemComponents)
        p = 0
        #self.parameter['thresh'] = 10
        #print(trial.task ,trial.itemComponents.values())
        for a in self.componentKeys:
            p += trial.itemComponents[a]* (0.2/len(self.componentKeys)) * self.parameter[a]
        #if self.thresh < p:
        if 1 < p:
            return 1
            return self.binCorrectCategorization(trial)
        else:
            return 0
            return self.binIncorrectCategorization(trial)
        #print(p)
        #if self.thresh < p:
        #    print(p, self.thresh,1 if self.thresh < p else 0)
        return 1 if self.thresh < p else 0

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass