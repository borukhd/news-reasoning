""" News Item Processing model implementation.
"""
import ccobra
from random import random 
import math

class LCparty(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='LinearCombinationByParty', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.parameter = {}
        #self.parameter['thresh'] = 10
        #self.componentKeys = ['Exciting_Democrats_Combined', 'Exciting_Republicans_Combined', 'Familiarity_Democrats_Combined', 'Familiarity_Republicans_Combined', 'Importance_Democrats_Combined', 'Importance_Republicans_Combined', 'Likelihood_Democrats_Combined', 'Likelihood_Republicans_Combined', 'Partisanship_All_Combined', 'Partisanship_All_Partisan', 'Partisanship_Democrats_Combined', 'Partisanship_Republicans_Combined', 'Sharing_Democrats_Combined', 'Sharing_Republicans_Combined', 'Worrying_Democrats_Combined', 'Worrying_Republicans_Combined']
        self.componentKeys = ['Exciting_Party_Combined', 'Familiarity_Party_Combined', 'Importance_Party_Combined', 'Partisanship_All_Combined', 'Partisanship_All_Partisan', 'Partisanship_Party_Combined','Worrying_Party_Combined']
        self.componentKeys=self.componentKeys[-3:]
        for a in self.componentKeys:
            self.parameter[a] = 0
        self.thresh = len(self.parameter)*3
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
        if trial.conservatism > 3.5:
            self.componentKeys = [a.replace('Party','Democrats') for a in self.componentKeys]
        if trial.conservatism < 3.5:
            self.componentKeys = [a.replace('Party','Republicans') for a in self.componentKeys]
            
        #print(trial.itemComponents)
        p = 0
        #self.parameter['thresh'] = 10
        #print(trial.task ,trial.itemComponents.values())
        for a in self.componentKeys:
            p += trial.itemComponents[a]* self.parameter[a.replace('Republicans','Party').replace('Democrats','Party')]
        #if self.thresh < p:
        if self.thresh < p:
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