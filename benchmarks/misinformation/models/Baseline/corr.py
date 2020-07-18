""" News Item Processing model implementation.
"""
import ccobra
import random
import math

class CorrectReply(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='CorrectReply', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.parameter = {'a': 0}
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def predict(self, item, **kwargs):
        reply = 'Accept' if item.truthful else 'Reject'
        #print(reply, item.truthful, item.truthful == 1)
        #reply = random.choice([0,1]) if not item.truthful else random.choice([3,4])
        return str(reply)

    def predictS(self, itemPair):
        return 1

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        
