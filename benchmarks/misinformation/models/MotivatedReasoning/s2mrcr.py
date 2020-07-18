""" News Item Processing model implementation.
"""
import ccobra
from random import random
import math

class S2MRCR(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='S2MRCR', commands = []):
        """ Initializes the TransitivityInt model.
        parameter
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.parameter = {}

        self.parameter['Dcons'] = 3
        self.parameter['Dlib'] = 1.5

        self.parameter['Kc'] = 0.55
        self.parameter['Kl'] = 0.3
        
        self.parameter['Mc'] = 0.2
        self.parameter['Ml'] = - 0.2

        self.parameter['Cr'] = 0.6 
        self.parameter['Cf'] = 0.3 
        self.parameter['Mr'] = 0.14                              
        self.parameter['Mf'] = - 0.22      
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def predict(self, trial, **kwargs):
        return 'Accept' if 0.5 < self.predictS(trial) else 'Reject'



    def predictS(self, trial):
        conservativePerson = trial.conservatism >= self.parameter['Dcons']
        liberalPerson = trial.conservatism <= self.parameter['Dlib']
        if trial.consNews and conservativePerson:
            threshold = self.parameter['Kc'] + trial.crt * self.parameter['Mc']
        elif trial.libeNews and liberalPerson:
            threshold = self.parameter['Kl'] + trial.crt * self.parameter['Ml']
        else:
            if trial.realnews:
                threshold = self.parameter['Cr'] + self.parameter['Mr'] * trial.crt
            if trial.fakenews:
                threshold = self.parameter['Cf'] + self.parameter['Mf'] * trial.crt
        return threshold


    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, item):
        pass
        