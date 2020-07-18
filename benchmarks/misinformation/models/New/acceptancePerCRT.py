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
        self.a = 0.5                              #constant
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def predict(self, trial, **kwargs):
        p = random()
        if trial.truthful:
            if p < 0.6 + 0.14 * trial.crt:
                return 'Accept' 
            else:
                return 'Reject'
        if not trial.truthful:
            if p < 0.7 + 0.22 * trial.crt: 
                return 'Accept'
            else:
                return 'Reject'


    def predictS(self, item):
        return item.crt * self.a

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        
