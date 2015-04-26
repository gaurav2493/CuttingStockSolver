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
 
    def __init__(self,inputDict,wasteThreshold,stocksize,algo,timestamp,slider):

        thread = threading.Thread(target=self.run, args=(inputDict,wasteThreshold,stocksize,algo,timestamp,slider))
        thread.daemon = True                            # Daemonize thread
        thread.start()                                # Start the execution
 
    def run(self,inputDict,wasteThreshold,stocksize,algo,timestamp,slider):
        waste=0
        self.algo=algo
        self.output=[]
        self.leftoverArray=[]
        currentThreads.update({timestamp:self})
        print "hello"
        print "****",wasteThreshold,inputDict,stocksize,algo,timestamp,"****"
        if(algo=="genetic"):
            print slider,1-slider
            a=GeneticSolver(inputDict,stocksize,wasteThreshold,countParam=slider,reuseParam=1-slider)
            self.solver=a
            chromo = a.getResult()
            i=1
            for gene in chromo.genes:
                res=""
                for key,value in gene.getDict().iteritems():
                    if(value>0):
                        res=res+","+str(key)+"*"+str(value)+" "
                self.output.append(res)
                self.leftoverArray.append(gene.getLeftover(stocksize))
                i+=1
            waste=chromo.waste
        else:
            a=GreedySolver(inputDict,stocksize)
            self.solver=a
            cutPatterns = a.getResult()
            i=1
            realwaste=0
            for combination in cutPatterns:
                leftover=combination.getLeftover(stocksize)
                self.leftoverArray.append(leftover)
                if(leftover<wasteThreshold):
                    realwaste+=leftover
                self.output.append( combination.printCombi())
                i+=1
            print "real waste = ",realwaste
            waste=realwaste
        a.progress=100
        self.solver.waste=waste
        
 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("UI/index.html", title="CSP Solver")

class AjaxProgressHandler(tornado.web.RequestHandler):
    def get(self):
        timestamp=self.get_cookie("userTime")
        progress=currentThreads[timestamp].solver.progress
        if(progress<100):
            self.write("progress="+str(progress))
        else:
            obj=currentThreads[timestamp]
            print obj.leftoverArray
            self.render("UI/solver.html",title="Solution",outp=obj.output,req=obj.solver.inputData,waste=obj.solver.waste,algo=obj.algo,leftovers=obj.leftoverArray)

class SolutionHandler(tornado.web.RequestHandler):
    def get(self):
        inputDict = {}
        stocksize=int(self.get_argument("stockSize", default="0", strip=False))
        wasteThreshold=int(self.get_argument("wasteThreshold", default="0", strip=False))
        slider=int(self.get_argument("range", default="20", strip=False))/100.0
        algo=self.get_argument("algoSelect", default="", strip=False)
        timestamp=str(time.time())
        self.set_cookie("userTime", timestamp)
        print algo
        for i in range(0,(len(self.request.arguments)/2)):
            if(int(self.get_argument("size"+str(i), default="0", strip=False))==0):
                continue
            inputDict.update({int(self.get_argument("size"+str(i), default="0", strip=False)):int(self.get_argument("qty"+str(i), default="0", strip=False))})

        solverThread=SolverThread(inputDict,wasteThreshold,stocksize,algo,timestamp,slider)
        self.render("UI/progress.html",title="Procressing ....")


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