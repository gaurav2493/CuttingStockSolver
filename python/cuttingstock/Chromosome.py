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
	
		self.geneticSolverObject=geneticSolverObject
		self.size = len(genes)
		self.genes = genes
		self.maxSize = geneticSolverObject.maxSize
		self.waste = self.__getTotalWaste__()
		self.fitness = self.__fitnessValue__(geneticSolverObject.minAssumptionSize)
		
	'''
	(count of combinations which contain reusable size = (no of combi with reusable extras/total combis)*0.75) => 25%
	(minimum logs required = L/P*0.75) => 75%
	'''
	def __fitnessValue__(self,min):
		a=min*1.0/self.size*self.geneticSolverObject.countParam
		b=self.geneticSolverObject.reuseParam*(min*self.geneticSolverObject.max_waste_size-self.waste)/(min*self.geneticSolverObject.max_waste_size)
		fitnessValue = a+b//min*1.0/self.size*self.geneticSolverObject.countParam + self.geneticSolverObject.reuseParam*(min*self.geneticSolverObject.max_waste_size-self.waste)/(min*self.geneticSolverObject.max_waste_size)
		#print min, self.geneticSolverObject.max_waste_size,self.waste
		return fitnessValue

	def __getGeneWaste__(self,gene):
		sum=0
		for key,value in gene.getDict().iteritems():
				sum+=key*value
		return self.maxSize-sum
	
	def __getTotalWaste__(self):

		totalSize=0
		#self.printChromo()
		for combination in self.genes:
			use=0
			for size,qty in combination.getDict().iteritems():
				use+=size*qty
			if(self.maxSize-use<self.geneticSolverObject.max_waste_size):
				totalSize+=use
			else:
				totalSize+=self.maxSize
			#print totalSize
		#print self.maxSize," * ",len(self.genes),"  ",totalSize
		return self.maxSize*len(self.genes)-totalSize

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

	def printChromo(self):
		i=1
		for gene in self.genes:
			res="("+str(i)+") "
			for key,value in gene.getDict().iteritems():
				if(value>0):
					res=res+str(value)+"*"+str(key)+","
			print res#"  fitness = ",self.fitness,self.__getGeneWaste__(gene)
			i+=1


