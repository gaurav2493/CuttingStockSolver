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
        
        combinations=self.combinationGenerator() # returns list of objects of class Combination
        self.qtyLeft=self.inputData.copy() # Type Dictionary {size:quantity}
        continueLoop=True
        while continueLoop:
            bestSum=0
            for combination in combinations:
                totalSum=combination.getCombinationSize()
                if(bestSum<totalSum):
                    bestSum=totalSum
                    selectedCombination=combination

            if(self.__isAvailable__(combination)):
                for size,qty in selectedCombination.getDict().iteritems():
                    self.qtyLeft.update({size:(self.qtyLeft.get(size)-qty)})
                print selectedCombination
            
            continueLoop=False
            for size,qty in self.qtyLeft.iteritems():
                if(qty>0):
                    continueLoop=True
                    break;                

    def __isAvailable__(self,combination):
        for size,qty in combination.getDict().iteritems():
            if(qty>self.qtyLeft.get(size)):
                return False
        return True
                