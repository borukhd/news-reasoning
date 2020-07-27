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
        self.Cr = 0.65 
        self.Cf = 0.2 
        self.Mr = 0.13                              
        self.Mf = - 0.12                           
        super().__init__(name, ['misinformation'], ['single-choice'], commands)


    def predictS(self, trial):
        if trial.realnews:
            threshold = self.Cr + self.Mr * trial.crt
        if trial.fakenews:
            threshold = self.Cf + self.Mf * trial.crt
        return threshold
        
        
    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        
