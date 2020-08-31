""" News Item Processing model implementation.
"""
import ccobra
from random import random 
import math
from staticCommon import Keys




class RS:
    recommendation = {}
    featuresOfAllPeople = {}
    repliesOfAllPeople = {}
    trained = False