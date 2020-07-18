""" News Item Processing model implementation.
"""
import ccobra
from random import random 
import math

class CR(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='Classical-Reasoning-Generic', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.a = 0.5                              #constant
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def predict(self, item, **kwargs):
        #p = 0.0
        #threshold = 0.5
        p = 1+item.crt * 3 * self.a
        #if p >= threshold:
        #if p >= random():
        #    return self.correctCategorization(item) 
        #else:
        #    return self.incorrectCategorization(item)
        if item.truthful:
            pred = round(p)
        else:
            pred = 4-round(p)
        print(pred)
        return str(pred)


    def predictS(self, itemPair):
        return item.crt * self.a

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        
