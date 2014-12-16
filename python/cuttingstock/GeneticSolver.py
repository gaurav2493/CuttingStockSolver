'''
Created on Dec 16, 2014

@author: Gaurav
'''
import random
from cuttingstock.Solver import Solver
from cuttingstock.GreedySolver import GreedySolver
from cuttingstock.Chromosome import Chromosome

RANDOM_SPECIES_NO = 1
randomFails = 300


class GeneticSolver(Solver):
    '''
    classdocs
    '''

    def generateRandomSpecies(self,amount): # returns a list of "RANDOM_SPECIES_NO" chromosomes

        combinations=self.combinationGenerator() # returns list of objects of class Combination
        self.qtyLeft=self.inputData.copy() # Type Dictionary {size:quantity}
        speciesGenerated = 0
        
        chromosomes = []

        while(speciesGenerated!=amount):  # no of solutions != amount

            chromosomeMade = False
            qtyLeft=self.inputData.copy()

            genes=[] # List containing genes (will form a chromosome)
            while(chromosomeMade!=True and randomFails != 0):           
                combi = random.choice(combinations)
                chromosomeFeasible = True

                for size,qty in combi.getDict().iteritems():
                    if(qty>qtyLeft.get(size)):
                        --randomFails
                        chromosomeFeasible = False

                if(chromosomeFeasible):
                    genes.append(combi)
                    for size,qty in combi.getDict().iteritems():  #Reduction in quantity left
                        qtyLeft.update({size:(qtyLeft.get(size)-qty)})
                        
                chromosomeMade=True # Just an assumption
                for size,qty in qtyLeft.iteritems(): # Check if assumption was correct
                    if(qty!=0):
                        chromosomeMade=False
                        break
                
                

            # if chromosome still not made, give the remaining stock to greedy algo.
            if(chromosomeMade!=True):
                greedySolverObject = GreedySolver(qtyLeft,self.maxSize)
                cutPatterns = greedySolverObject.getResult()
                for combination in cutPatterns:
                    genes.append(combination.getdict())
                    
            chromosomes.append(Chromosome(genes, self.maxSize))
            
            speciesGenerated+=1
        return chromosomes
            
    def getResult(self):
        chromosomes = self.generateRandomSpecies(RANDOM_SPECIES_NO)
        for chromo in chromosomes:
            print chromo
        print "hello"