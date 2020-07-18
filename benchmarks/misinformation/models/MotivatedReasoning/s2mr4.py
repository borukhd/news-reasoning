""" News Item Processing model implementation.
"""
import ccobra
from random import random
import math

class CR(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='S2MR-Generic', commands = []):
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
        #p = 0.0
        #threshold = 0.3
        #if item.crt > threshold:
        #    if item.c:
        #        if item.ct == 2:       
        #            return 'Accept'
        #        elif item.ct == 1:
        #            return 'Reject'
        #    if item.l:
        #        if item.ct == 1:       
        #            return 'Accept'
        #        elif item.ct == 2:
        #            return 'Reject'
        #return 'Accept' if random() < threshold else 'Reject'

        p = 1+ item.crt * 3 * self.a
        pred = 4-round(p)
        if item.truthful:
            if item.l:
                if item.ct == 1:
                    pred = round(p)
                else:
                    pred = 4 - round(p)
            if item.c:
                if item.ct == 2:
                    pred = round(p)
                else:
                    pred = round(p)
        print(pred)
        return str(pred)


    def predictS(self, item):
        return 0.5

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, item):
        pass
        
