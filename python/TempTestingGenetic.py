'''
Created on Dec 16, 2014

@author: Gaurav
'''

from cuttingstock.GeneticSolver import GeneticSolver
if __name__ == '__main__':
    #inputp={1380:22,1520:25,1560:12,1710:14,1820:18,1880:18,1930:20,2000:10,2050:12,2100:14,2140:16,2150:18,2200:20}
    inputp={300:8,700:9,600:6,500:8,400:4}
    max_size=5600
    a=GeneticSolver(inputp,max_size)
    a.getResult()
    #cutPatterns = a.getResult()
    #for combination in cutPatterns:
    #    print combination," Waste = ",max_size-combination.getCombinationSize()