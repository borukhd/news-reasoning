""" News Item Processing model implementation.
"""
import ccobra
from random import random 
import math
from staticCommon import Keys
from New.RS import RS


class RecommenderP(ccobra.CCobraModel):
    """ TransitivityInt CCOBRA implementation.
    """
    def __init__(self, name='RecommenderPerson', commands = []):
        """ Initializes the TransitivityInt model.
        Parameters
        ----------
        name : str
            Unique name of the model. Will be used throughout the ORCA
            framework as a means for identifying the model.
        """
        self.parameter = {}
        self.relevant = Keys.person
        self.relevant = ['education','crt','panasPos','panasNeg']
        for a in self.relevant:
            self.parameter[a] = 0
                
        super().__init__(name, ['misinformation'], ['single-choice'], commands)

    def pre_train(self, dataset):
        print('Pretrain person started')
        trialList = []
        for pers in dataset:
            trialList.extend([a['item'] for a in pers if 'NoInfo' not in [a['item'].feature(f) for f in self.relevant]])
        return self.globalTrain(trialList)

    def globalTrain(self, trialList):
        if RS.trained:
            return
        RS.trained = True
        for item in trialList:
            if item.identifier not in RS.featuresOfAllPeople.keys():
                RS.featuresOfAllPeople[item.identifier] = item.person_features
            if item.identifier not in RS.repliesOfAllPeople.keys():
                RS.repliesOfAllPeople[item.identifier] = {}
            RS.repliesOfAllPeople[item.identifier][item.task[0][0]] = float(item.birep)
        print(len(trialList))

    def similar(self, person1, person2):
        for key in self.relevant:
            if(abs(RS.featuresOfAllPeople[person1][key] - RS.featuresOfAllPeople[person2][key]) > self.parameter[key]): 
                return False
        #print(person1, person2, key)
        return True

    def predictS(self, trial):
        if not RS.trained:
            print('Untrained Model')
            return 
        repliesOfSimilar = 0
        numberOfReplies = 0
        for person in RS.featuresOfAllPeople.keys():
            if numberOfReplies > 40:
                break
            if trial.identifier in RS.featuresOfAllPeople.keys() and self.similar(person, trial.identifier) and person != trial.identifier and trial.task_str in RS.repliesOfAllPeople[person].keys():
                repliesOfSimilar += RS.repliesOfAllPeople[person][trial.task[0][0]]
                numberOfReplies += 1
            else:
                continue
        #print(trial.identifier, repliesOfSimilar,numberOfReplies)
        if repliesOfSimilar == 0:
            return 0.5
        meanResponse = repliesOfSimilar/numberOfReplies
        return int(meanResponse > 0.5)

    def adapt(self, item, target, **kwargs):
        pass

    def adaptS(self, itemPair):
        pass
        


