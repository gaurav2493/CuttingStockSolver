#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import threading
import time

from cuttingstock.GeneticSolver import GeneticSolver
from cuttingstock.GreedySolver import *
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
currentThreads={}
 
class SolverThread(object):
    """ Threading example class

    The run() method will be started and it will run in the background
    until the application exits.
    """
 
    def __init__(self,inputDict,wasteThreshold,stocksize,algo,timestamp):
        """ Constructor

        :type interval: int
        :param interval: Check interval, in seconds
        
        self.inputDict=inputDict
        self.wasteThreshold=wasteThreshold
        self.stocksize=stocksize
        self.algo=algo
        """
        thread = threading.Thread(target=self.run, args=(inputDict,wasteThreshold,stocksize,algo,timestamp))
        thread.daemon = True                            # Daemonize thread
        thread.start()                                # Start the execution
 
    def run(self,inputDict,wasteThreshold,stocksize,algo,timestamp):
        waste=0
        self.algo=algo
        self.output=[]
        currentThreads.update({timestamp:self})
        print "hello"
        print "****",wasteThreshold,inputDict,stocksize,algo,timestamp,"****"
        if(algo=="genetic"):
            a=GeneticSolver(inputDict,stocksize,wasteThreshold)
            self.solver=a
            chromo = a.getResult()
            i=1
            for gene in chromo.genes:
                res=""
                for key,value in gene.getDict().iteritems():
                    if(value>0):
                        res=res+","+str(key)+"*"+str(value)+" "
                self.output.append(res)
                i+=1
            waste=chromo.waste
        else:
            a=GreedySolver(inputDict,stocksize)
            self.solver=a
            cutPatterns = a.getResult()
            i=1
            realwaste=0
            for combination in cutPatterns:
                if(stocksize-combination.getCombinationSize()<waste):
                    realwaste+=stocksize-combination.getCombinationSize()
                self.output.append( str(i)+" " + combination.printCombi()) #+" waste = ",max_size-combination.getCombinationSize()
                i+=1
            print "real waste = ",realwaste
            waste=realwaste
        a.progress=100
        self.solver.waste=waste
        
 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("UI/index.html", title="My title", items=items)

class AjaxProgressHandler(tornado.web.RequestHandler):
    def get(self):
        timestamp=self.get_cookie("userTime")
        progress=currentThreads[timestamp].solver.progress
        if(progress<100):
            self.write("progress="+str(progress))
        else:
            obj=currentThreads[timestamp]
            self.render("UI/solver.html", outp=obj.output,req=obj.solver.inputData,waste=obj.solver.waste,algo=obj.algo)

class SolutionHandler(tornado.web.RequestHandler):
    def get(self):
        output=[]
        inputDict = {}
        waste=0
        stocksize=int(self.get_argument("stockSize", default="0", strip=False))
        wasteThreshold=int(self.get_argument("wasteThreshold", default="0", strip=False))
        algo=self.get_argument("algoSelect", default="", strip=False)
        timestamp=str(time.time())
        self.set_cookie("userTime", timestamp)
        solverThread=SolverThread(inputDict,wasteThreshold,stocksize,algo,timestamp)
        print algo
        for i in range(0,(len(self.request.arguments)/2)):
            if(int(self.get_argument("size"+str(i), default="0", strip=False))==0):
                continue
            inputDict.update({int(self.get_argument("size"+str(i), default="0", strip=False)):int(self.get_argument("qty"+str(i), default="0", strip=False))})
        '''
        print inputDict
        print stocksize
        print waste
        #inputDict={1380:22,1520:25,1560:12,1710:14,1820:18,1880:18,1930:20,2000:10,2050:12,2100:14,2140:16,2150:18,2200:20}
        if(algo=="genetic"):
            a=GeneticSolver(inputDict,stocksize,wasteThreshold)
            chromo = a.getResult()
            i=1
            for gene in chromo.genes:
                res=""
                for key,value in gene.getDict().iteritems():
                    if(value>0):
                        res=res+","+str(key)+"*"+str(value)+" "
                output.append(res)
                i+=1
            waste=chromo.waste
        else:
            a=GreedySolver(inputDict,stocksize)
            cutPatterns = a.getResult()
            i=1
            realwaste=0
            for combination in cutPatterns:
                if(stocksize-combination.getCombinationSize()<waste):
                    realwaste+=stocksize-combination.getCombinationSize()
                output.append( str(i)+" " + combination.printCombi()) #+" waste = ",max_size-combination.getCombinationSize()
                i+=1
            print "real waste = ",realwaste
            waste=realwaste
            self.render("UI/solver.html", outp=output,req=inputDict,waste=waste,algo=algo)
        '''
        self.render("UI/progress.html",outp=[],req={},waste=90,algo=algo)

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'UI/static/'}),
        (r"/solution",SolutionHandler),
        (r"/getProgress",AjaxProgressHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()