""" News Item Processing model implementation.
"""
import ccobra
from random import random 
import math

class CRrecog(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='ClassicReas&Recog', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.parameter = {}
        self.parameter['threshH'] = 0
        self.parameter['threshL'] = 0
        #self.parameter['part'] = 0
        #self.parameter['partF'] = 0
        self.Cr = 0.6 
        self.Cf = 0.3 
        self.Mr = 0.14                              
        self.Mf = - 0.4                           
        super().__init__(name, ['misinformation'], ['single-choice'], commands)


    def predictS(self, trial):
        threshold = 0.5
        familiarity = self.pretest('Familiarity',trial)
        if familiarity > self.parameter['threshH'] :
            if trial.realnews:
                threshold = self.Cr + self.Mr * trial.crt
            if trial.fakenews:
                threshold = self.Cf + self.Mf * trial.crt
            return threshold
        if familiarity < self.parameter['threshL'] :
            return 1
        return threshold
        
    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        
