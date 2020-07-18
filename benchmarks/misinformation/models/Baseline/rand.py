""" News Item Processing model implementation.
"""
import ccobra
import random
import math

class BaselineRandom(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='BaselineRandom', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.a = 1                              #constant
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def predict(self, item, **kwargs):
        return random.choice(item.choices)

    def predictS(self, item):
        return 1/float(len(item.choices))

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        
