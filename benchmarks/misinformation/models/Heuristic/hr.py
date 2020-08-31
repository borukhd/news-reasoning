""" News Item Processing model implementation.
"""
import ccobra
import random
import math

class RH(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='Heuristic-Recognition', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.parameter = {}
        self.parameter['fam'] = 1
        optdict = {'fam': 2.390676377924067}
        for a in optdict.keys():
            self.parameter[a] = optdict[a]
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def predictS(self, item):
        return item.feature('Familiarity') > self.parameter['fam']

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        
