""" News Item Processing model implementation.
"""
import ccobra
import random
import math

class CR(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='Machine-Learning-Generic', commands = []):
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
        return 'Accept' if random.random()>0.5 else 'Reject'

    def predictS(self, itemPair):
        return 0.5

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        
