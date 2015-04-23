'''
Created on Dec 16, 2014

@author: Gaurav
'''
import random
import math
import copy
import sys
import os
from cuttingstock.Solver import Solver
from cuttingstock.GreedySolver import GreedySolver
from cuttingstock.Chromosome import Chromosome

RANDOM_SPECIES_NO = 2000
CROSSOVER_GENERATED_SPCEIE_NO = 800
MAX_RANDOM_TRIALS = 1

class GeneticSolver(Solver):
    '''
    classdocs
    '''

    def generateRandomSpecies(self,amount): # returns a list of "RANDOM_SPECIES_NO" chromosomes

        combinations=self.combinationGenerator() # returns list of objects of class Combination
        self.qtyLeft=self.inputData.copy() # Type Dictionary {size:quantity}
        sum=0
        for key,value in self.inputData.iteritems():
            sum+=key*value
        self.minAssumptionSize=sum/self.maxSize
        self.avgSize=-1 # will definitely be modified
        self.totalSpeciesGenerted=RANDOM_SPECIES_NO
        self.rouletteFitnessSum=0
        self.minRouletteValue=0
        self.MaxRouletteValue=100
        self.roulettePositions=[]
        self.bestSolutionIndex=0
        speciesGenerated = 0
        totalSize=0
        
        chromosomes = []

        while(speciesGenerated!=amount):  # no of solutions != amount
            self.progress=(speciesGenerated*1.0/amount)*50

            chromosomeMade = False
            qtyLeft=self.inputData.copy()
            fails=0
            genes=[] # List containing genes (will form a chromosome)
            while(chromosomeMade!=True and fails<MAX_RANDOM_TRIALS):           
                combi = random.choice(combinations)
                chromosomeFeasible = True

                for size,qty in combi.getDict().iteritems():
                    if(qty>qtyLeft.get(size)):
                        fails+=1
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
                
            #print fails
            # if chromosome still not made, give the remaining stock to greedy algo.
            if(chromosomeMade!=True):
                greedySolverObject = GreedySolver(qtyLeft,self.maxSize)
                cutPatterns = greedySolverObject.getResult()
                genes.extend(cutPatterns)

            totalSize+=len(genes)

            chromo=Chromosome(genes, self)
            self.rouletteFitnessSum+=chromo.fitness
            chromosomes.append(chromo)
            if(chromo.fitness>chromosomes[self.bestSolutionIndex].fitness): # Getting index of best chromosome
                self.bestSolutionIndex=len(chromosomes)-1
            
            speciesGenerated+=1
        self.avgSize=math.ceil(totalSize*1.0/RANDOM_SPECIES_NO)
        return chromosomes

    def prepareRouletteWheel(self,species):
        sum=0
        for specie in species:
            sum+=specie.fitness/self.rouletteFitnessSum*(self.MaxRouletteValue)
            self.roulettePositions.append(sum)


    def rouletteWheelSelector(self,species): # returns list of species of size 2
        returningList=[]
        first = random.random()*self.MaxRouletteValue
        second = random.random()*self.MaxRouletteValue
        pos=0
        for value in self.roulettePositions:
            if(first<=value):
                returningList.append(species[pos])
                break
            pos+=1
        pos=0
        for value in self.roulettePositions:
            if(second<=value):
                returningList.append(species[pos])
                break
            pos+=1

        return returningList

    def generateCrossOverSpecie(self,specie1,specie2): # return a new crossover Specie(may be not a solution)
        #REMEMBER dict.copy
        if(specie1.size>specie2.size): # swapping
            specie1,specie2 = specie2,specie1
        half = specie1.size/2
        genes=[]
        for i in range(0,half):
            genes.append(specie1.genes[i])
        for i in range(half,specie1.size):
            genes.append(specie2.genes[i])

        newSpecie = Chromosome(genes, self)

        return newSpecie


    def mutate(self,chromosome1): # return a Specie in mutated form if required
        chromosome=copy.deepcopy(chromosome1)
        try:
            KVPairSum={}
            for key in self.inputData.keys(): # kvpair initialized to 0
                KVPairSum.update({key:0})
            for key in self.inputData.keys(): #kvpair calculated 
                for combi in chromosome.genes:
                    KVPairSum.update({key:KVPairSum[key]+combi.getDict()[key]})

            for key,value in self.inputData.iteritems(): # reduction
                diff=KVPairSum[key]-value
                if(diff>0): # reducing from the combination of minimum size
                    for combi in chromosome.genes: # reducing
                        while(diff>0 and combi.getDict()[key]>0):
                            combi.getDict().update({key:combi.getDict()[key]-1})
                            diff-=1
            #fitnesss updation req

            for key,value in self.inputData.iteritems(): # increment
                diff=KVPairSum[key]-value
                if(diff<0): # reducing from the combination of minimum size
                    for combi in chromosome.genes: # reducing
                        while(diff<0 and combi.getCombinationSize()+key<=self.maxSize):
                            combi.getDict().update({key:combi.getDict()[key]+1})
                            diff+=1
                    if(diff!=0):
                        chromosome=None
            # Trying to reduce chromosome size
            if(chromosome!=None):
                for gene in chromosome.genes:
                    allzero=True
                    for value in gene.getDict().values():
                        if(value!=0):
                            allzero=False
                            break
                    if allzero:
                        chromosome.genes.remove(gene)
        except Exception as detail:
            #print str(detail),'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
            #print chromosome
            chromosome=None
        return chromosome


            
    def getResult(self):
        self.crossoverfails=0
        chromosomes = self.generateRandomSpecies(RANDOM_SPECIES_NO)
        '''for chromo in chromosomes:
            print chromo'''
        self.prepareRouletteWheel(chromosomes)
        for val in self.roulettePositions:
            print val
        for i in range(0,CROSSOVER_GENERATED_SPCEIE_NO):
            twoSelectedSpecies = self.rouletteWheelSelector(chromosomes)
            #print "\n\n----Printing 2 selected----"
            '''for j in twoSelectedSpecies:
                print j'''
            newSpecie = self.generateCrossOverSpecie(twoSelectedSpecies[0],twoSelectedSpecies[1])
            '''print "\n\n-----------result of crossover---------"
            print newSpecie            
            print "Afer mutation"'''
            newSpecie=self.mutate(newSpecie)
            if(newSpecie==None):
                print "Crossover and Mutation Failed"
                self.crossoverfails+=1
            else:
                chromosomes.append(newSpecie)
                '''if(newSpecie.fitness>chromosomes[self.bestSolutionIndex].fitness):
                    self.bestSolutionIndex=len(chromosomes)-1
                '''
                self.prepareRouletteWheel
            self.progress=50+(i*1.0/CROSSOVER_GENERATED_SPCEIE_NO)*50
        print "\n-------- solution --------"
        chromosomes[self.bestSolutionIndex].printChromo()
        print chromosomes[self.bestSolutionIndex]
        print "waste = ",chromosomes[self.bestSolutionIndex].waste
        print "crossoverfails = ",self.crossoverfails,"total species = ",len(chromosomes)
       # print self.minAssumptionSize," * ",self.max_waste_size," - ",chromosomes[self.bestSolutionIndex].waste," ",(self.minAssumptionSize*self.max_waste_size)
        counterrr=0
        for chromo in chromosomes:
            if(chromo.fitness>chromosomes[self.bestSolutionIndex].fitness):
                self.bestSolutionIndex=counterrr;
            counterrr+=1
            print "fitness = ",chromo.fitness
        chromosomes[self.bestSolutionIndex].printChromo()
        print chromosomes[self.bestSolutionIndex]
        print "waste = ",chromosomes[self.bestSolutionIndex].waste
        print "crossoverfails = ",self.crossoverfails,"total species = ",len(chromosomes)
        return chromosomes[self.bestSolutionIndex]
