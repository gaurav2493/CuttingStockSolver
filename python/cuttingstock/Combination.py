'''
Created on Jun 1, 2014

@author: Gaurav
'''

class Combination(object):
    '''
    classdocs
    '''
    
    def __init__(self, size_qty):
        '''
        size_qty is a dictionary containing containing {size:qty}
        '''
        self.size_qty = size_qty
        
    def getCombinationSize(self): # to get the total length occupied by this combination
        size=0
        for key,value in self.size_qty.iteritems():
            size+= key*value
        return size

    def getLeftover(self,stocksize):
        return stocksize-self.getCombinationSize()
    
    def getDict(self):
        return self.size_qty
    
    def __str__(self):
        return str(self.size_qty)

    def printCombi(self):
        res=""
        for key,value in self.size_qty.iteritems():
            if(value>0):
                res=res+","+str(key)+"*"+str(value)
        return res
        