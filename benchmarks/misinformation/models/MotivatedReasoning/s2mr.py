""" News Item Processing model implementation.
"""
import ccobra
from random import random
import math

class S2MR(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='S2MR', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.parameter = {}
        #self.parameter['Dcons'] = 3
        #self.parameter['Dlib'] = 1.5

        self.parameter['Kc'] = 0.55
        self.parameter['Kl'] = 0.3
        
        self.parameter['Mc'] = 0.2
        self.parameter['Ml'] = - 0.2

        optdict = {'Kc': -0.056536155629514195, 'Kl': -0.09074348945552314, 'Mc': -0.027349753930657073, 'Ml': -0.036805428943731885}
        for a in optdict.keys():
            self.parameter[a] = optdict[a]
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def predictS(self, trial):
        conservativePerson = trial.feature('conservatism') >= 3.5#self.parameter['Dcons']
        liberalPerson = trial.feature('conservatism') <= 3.5#self.parameter['Dlib']
        #print('Freaturekeys:')
        #print([(a, trial.feature(a)) for a in trial.featurekeys()])
        if trial.feature('Partisanship')>3.8 and conservativePerson:
            threshold = self.parameter['Kc'] + trial.feature('crt') * self.parameter['Mc']
        elif trial.feature('Partisanship')<2.2 and liberalPerson:
            threshold = self.parameter['Kc'] + trial.feature('crt') * self.parameter['Mc']
        elif trial.feature('Partisanship')<2.2 and conservativePerson:
            threshold = self.parameter['Kl'] + trial.feature('crt') * self.parameter['Ml']
        elif trial.feature('Partisanship')>3.8 and liberalPerson:
            threshold = self.parameter['Kl'] + trial.feature('crt') * self.parameter['Ml']
        else:
            threshold = 0.5
        return threshold

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, item):
        pass
        
