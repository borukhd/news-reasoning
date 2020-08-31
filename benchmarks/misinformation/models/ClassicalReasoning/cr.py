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
        super().__init__(name, ['misinformation'], ['single-choice'], commands)


    def predictS(self, trial):
        self.parameter['Cr'] = 0.65 
        self.parameter['Cf'] = 0.2 
        self.parameter['Mr'] = 0.13                              
        self.parameter['Mf'] = - 0.12 
        if trial.realnews:
            threshold = self.parameter['Cr'] + self.parameter['Mr'] * trial.feature('crt')
        if trial.fakenews:
            threshold = self.parameter['Cf'] + self.parameter['Mf'] * trial.feature('crt')
        return threshold
        
        
    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        
