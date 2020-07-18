""" News Item Processing model implementation.
"""
import ccobra
from random import random 
import math

class CR(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='ClassicReas', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.parameter = {}
        self.parameter['Cr'] = 0.6 
        self.parameter['Cf'] = 0.3 
        self.parameter['Mr'] = 0.14                              
        self.parameter['Mf'] = - 0.4                           
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def predict(self, trial, **kwargs):
        return 'Accept' if 0.5 < self.predictS(trial) else 'Reject'
        


    def predictS(self, trial):
        if trial.realnews:
            threshold = self.parameter['Cr'] + self.parameter['Mr'] * trial.crt
        if trial.fakenews:
            threshold = self.parameter['Cf'] + self.parameter['Mf'] * trial.crt
        return threshold
        
        
    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        
