'''
Created on Jun 2, 2014

@author: Gaurav
'''
from cuttingstock.GreedySolver import *
if __name__ == '__main__':
    inputp={200:5,600:8,700:3}
    max_size=2000
    a=GreedySolver(inputp,max_size)
    a.combinationGenerator()