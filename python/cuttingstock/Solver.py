'''
Created on Jun 1, 2014

@author: Gaurav
'''
from abc import ABCMeta, abstractmethod 
from cuttingstock.Combination import Combination
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
        for size,qty in inputDictionary.iteritems():
            if(size>maxSize):
                raise InputError("Max Size cannot be greater than cut size")
        
    def combinationGenerator(self):
        combinations=[] #A list of objects of class Combination
        limit=self.__getUpperLimit__() # A list of maximum quantities of each size.
        qtyMax=[]
        qtyTemp=[]
        for size,qty in limit.items():
            qtyMax.append(qty)
            qtyTemp.append(0)
        
        selectedPosition=len(qtyMax)-1
        
        loopingContinue=True
        while (loopingContinue):       
            for qty in range(0,qtyMax[selectedPosition]+1):
                combinationDict={}
                k=0
                for i,j in self.inputData.iteritems():
                    combinationDict.update({i:qtyTemp[k]})
                    k+=1
                    
                size=0
                for key,value in combinationDict.iteritems():
                    size+= key*value                
                
                if(size<=self.maxSize):
                    combinations.append(Combination(combinationDict))
                    
                qtyTemp[selectedPosition]+=1
            while (True):
                qtyTemp[selectedPosition]=0
                selectedPosition-=1
                if(selectedPosition==-1):
                    loopingContinue=False
                    
                if(qtyTemp[selectedPosition]< qtyMax[selectedPosition]):
                    qtyTemp[selectedPosition]+=1
                    break
                
            selectedPosition=len(qtyMax)-1

        return combinations
                    
    
    def __getUpperLimit__(self):
        limit={}
        for key,value in self.inputData.iteritems():
            limit.update({key:min(value,self.maxSize/key)})
        return limit
    
    @abstractmethod
    def getResult(self):
        pass
    
class InputError(Exception):
    def __init__(self,message):
        self.message=message
        