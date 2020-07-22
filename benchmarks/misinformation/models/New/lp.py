""" News Item Processing model implementation.
"""
import ccobra
from random import random 
import math
from New.sentimentanalyzer import SentimentAnalyzer

responses = []
count = {}

class LP(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='LanguageProcessing', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.thresh = 1
        self.parameter = {}
        self.relevant = ['negative_emotion', 'health', 'dispute', 'government', 'leisure', 'healing', 'military', 'fight', 'meeting', 'shape_and_size', 'power', 'terrorism', 'competing', 'optimism', 'sexual', 'zest', 'love', 'joy', 'lust', 'office', 'money', 'aggression', 'wealthy', 'banking', 'kill', 'business', 'fabric', 'speaking', 'work', 'valuable', 'economics', 'clothing', 'payment', 'feminine', 'worship', 'affection', 'friends', 'positive_emotion', 'giving', 'help', 'school', 'college', 'real_estate', 'reading', 'gain', 'science', 'negotiate', 'law', 'crime', 'stealing', 'white_collar_job', 'weapon', 'night', 'strength']
        self.relevant = ['negative_emotion', 'fight', 'optimism', 'sexual', 'money', 'aggression', 'affection', 'positive_emotion', 'science', 'law', 'crime']
        for a in self.relevant:
            self.parameter[a] = 1
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def predict(self, trial, **kwargs):
        p = random()
        if trial.truthful:
            if p < 0.6 + 0.14 * trial.crt:
                return 'Accept' 
            else:
                return 'Reject'
        if not trial.truthful:
            if p < 0.7 + 0.22 * trial.crt: 
                return 'Accept'
            else:
                return 'Reject'


    def predictS(self, trial):
        analysis = SentimentAnalyzer.analysis(trial)
        p = 0
        for a in self.relevant:
            p += analysis[a]*  self.parameter[a]
        #print(p)
        return 1 if self.thresh < p else 0

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        


