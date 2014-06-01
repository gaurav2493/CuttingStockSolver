'''
Created on Jun 1, 2014

@author: Devesh
'''
from abc import ABCMeta, abstractmethod 
class Solver(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta


    def __init__(self, inputDictionary,maxSize):
        '''
        Constructor
        '''
        self.input=-inputDictionary
        self.maxSize=maxSize
    def combinationGenerator(self,combination):
        pass
    
    def __getUpperLimit(self,combination):
        pass
    
    @abstractmethod
    def getResult(self):
        pass
        