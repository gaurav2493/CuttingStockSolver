'''
Created on Jun 1, 2014

@author: Gaurav
'''
from cuttingstock.Solver import Solver

class GreedySolver(Solver):
    '''
    classdocs
    '''
    def getResult(self):
        combinations=self.combinationGenerator()
        
        bestSum=0
        for combination in combinations:
            if(combination.getCombinationSize()>bestSum):
                bestCombination=combination
        
        pass