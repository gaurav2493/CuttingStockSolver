'''
Created on Jun 1, 2014

@author: Gaurav
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
        self.inputData=inputDictionary
        self.maxSize=maxSize
    def combinationGenerator(self):
        pass
    
    def __getUpperLimit(self):
        limit={}
        for key,value in self.inputData.iteritems():
            limit.update({key:min(value,self.maxSize/key)})
        return limit
    
    @abstractmethod
    def getResult(self):
        pass
        