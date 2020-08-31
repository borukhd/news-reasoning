""" News Item Processing model implementation.
"""
import ccobra
import random
import math

class RHlinear(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='Heuristic-Recognition-linear', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.parameter = {}
        self.parameter['kappa'] = 1
        self.parameter['alpha'] = 1
        optdict = {'kappa': -5.192396551875893, 'alpha': 2.2913602334440673}
        for a in optdict.keys():
            self.parameter[a] = optdict[a]
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def predictS(self, item):
        return item.feature('Familiarity') * self.parameter['alpha'] + self.parameter['kappa']

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        
