'''
Created on Dec 16, 2014

@author: Gaurav
'''

class Chromosome(object):

	'''
    classdocs
    '''
	UNDERFIT=-1
	FIT=0
	OVERFIT=1

	def __init__(self,genes,geneticSolverObject):
	
		self.size = len(genes)
		self.genes = genes
		self.maxSize = geneticSolverObject.maxSize
		self.waste = self.__getTotalWaste__()
		self.fitness = self.__fitnessValue__(geneticSolverObject.minAssumptionSize)
		self.geneticSolverObject=geneticSolverObject
		
	'''
	(count of combinations which contain reusable size = (no of combi with reusable extras/total combis)*0.75) => 25%
	(minimum logs required = L/P*0.75) => 75%
	'''
	def __fitnessValue__(self,min):
		fitnessValue = min*1.0/self.size
		return fitnessValue
	
	def __getTotalWaste__(self):
		
		totalSize = 0
		for combination in self.genes:
			for size,qty in combination.getDict().iteritems():
				totalSize+=size*qty
				
		return self.maxSize-totalSize

	def getSolutionType(self,geneticSolverObject):  # to be revised
		inputDict=geneticSolverObject.inputData.copy()
		for gene in self.genes:
			for key,value in gene.getDict().iteritems():
				inputDict.update({key:value-gene.getDict()[key]})
		for i in inputDict.iteritems():
			if(i>0):
				return "Chromosome.UNDERFIT"
			else:
				if(i<0):
					return "Chromosome.OVERFIT"
		return "Chromosome.FIT"
	
	def __str__(self):
		
		returnString = "\t"
		for key in sorted(self.geneticSolverObject.inputData):
			returnString=returnString+ str(key)+"\t"
		returnString=returnString+"\n"
		i=1
		for gene in self.genes:
			returnString=returnString+"S"+str(i)+"\t"
			for key in sorted(self.geneticSolverObject.inputData):
				returnString=returnString+str(gene.getDict()[key])+"\t"
			returnString=returnString+"\n"
			i+=1
			#returnString = returnString+str(gene)+"\n"
		return returnString + "\n size = " + str(self.size) + " fitness = " + str(self.fitness)

