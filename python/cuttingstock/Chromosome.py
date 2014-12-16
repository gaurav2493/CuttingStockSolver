'''
Created on Dec 16, 2014

@author: Gaurav
'''

class Chromosome(object):

	'''
    classdocs
    '''
	
	def __init__(self,genes,maxSize):
	
		self.size = len(genes)
		self.genes = genes
		self.maxSize = maxSize
		self.waste = self.__getTotalWaste__()
		
	def fitness(self):
		pass
	
	def __getTotalWaste__(self):
		
		totalSize = 0
		for combination in self.genes:
			for size,qty in combination.getDict().iteritems():
				totalSize+=size*qty
				
		return self.maxSize-totalSize
	
	def crossOver(self,chromosome):
		pass
	
	def __str__(self):
		
		returnString = ""
		for gene in self.genes:
			returnString = returnString+str(gene)+"\n"
		return returnString + "\n size = " + str(self.size)

