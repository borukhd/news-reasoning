""" News Item Processing model implementation.
"""
import ccobra
from random import random 
import math
from New.sentimentanalyzer import SentimentAnalyzer



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
        #self.relevant = ['negative_emotion', 'optimism', 'aggression', 'positive_emotion', 'science']
        for a in self.relevant:
            self.parameter[a] = 1

        optdict = {'negative_emotion': 3.488183752051738, 'fight': 4.795255469272864, 'optimism': 5.4718777782354735, 'sexual': 3.583167795093339, 'money': 5.249519675409447, 'aggression': 5.464386990594476, 'affection': -2.3986185486873572, 'positive_emotion': -1.4074963226019577, 'science': 1.5522568483198222, 'law': 12.874721726587898, 'crime': -2.9929120337902457}
        for a in optdict.keys():
            self.parameter[a] = optdict[a]
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

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
        


