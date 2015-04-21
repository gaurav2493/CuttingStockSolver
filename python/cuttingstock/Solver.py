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

    def __init__(self, inputDictionary,maxSize,max_waste_size=0,countParam=0.2,reuseParam=0.8):
        '''
        Constructor
        '''
        self.inputData=inputDictionary
        self.maxSize=maxSize
        self.max_waste_size=max_waste_size
        self.countParam=countParam
        self.reuseParam=reuseParam
        for size,qty in inputDictionary.iteritems():
            if(size>maxSize):
                raise InputError("Max Size cannot be greater than cut size (", size,">",maxSize,")")
        
    def combinationGenerator(self):
        limit=self.__getUpperLimit__() # A list of maximum quantities of each size.
        
        keys=[]
        tmpCombi={}
        for key in self.inputData.keys():
            keys.append(key)
            tmpCombi.update({key:0})

        keys.sort(reverse=True)
        
        '''
        suppose length of list = 5
        for k,v in inputDictionary


        '''
        selectedIndex=len(keys)-1
        combinations=[] #A list of objects of class Combination
        while (True):
            if(selectedIndex==-1):
                break

            if selectedIndex!=len(keys)-1: # if index is not last, then make all at right of selected index as 0
                for i in range(selectedIndex+1,len(tmpCombi)):
                    key=keys[i]
                    tmpCombi.update({key:0})
                key=keys[selectedIndex]
                tmpCombi.update({key:tmpCombi[key]+1}) # increment at selected index
            else: # increment last index
                key=keys[selectedIndex]
                tmpCombi.update({key:tmpCombi[key]+1}) # increment at selected index

            if(self.__isFeasible__(tmpCombi,limit)): #check if increment possible at selected Index
                combinations.append(Combination(tmpCombi.copy()))
                selectedIndex=len(keys)-1
            else:
                selectedIndex-=1
        return combinations
                    
    
    def __getUpperLimit__(self):
        limit={}
        for key,value in self.inputData.iteritems():
            limit.update({key:min(value,self.maxSize/key)})
        return limit
        
    def __isFeasible__(self,combination,limit):
        sum=0
        for key,value in combination.iteritems():
            if(limit[key]<value):
                return False
            sum+=key*value
        if(sum<=self.maxSize):
            return True
        return False
    
    @abstractmethod
    def getResult(self):
        pass
    
class InputError(Exception):
    def __init__(self,message):
        self.message=message
        