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

from cuttingstock.GeneticSolver import GeneticSolver

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("UI/index.html", title="My title", items=items)

class SolutionHandler(tornado.web.RequestHandler):
    def get(self):
        output=[]
        inputDict = {}
        stocksize=int(self.get_argument("max-size", default="0", strip=False))
        for i in range(0,(len(self.request.arguments)/2)):
            inputDict.update({int(self.get_argument("size"+str(i), default="0", strip=False)):int(self.get_argument("qty"+str(i), default="0", strip=False))})
        a=GeneticSolver(inputDict,stocksize)
        chromo = a.getResult()
        i=1
        for gene in chromo.genes:
            res=""
            for key,value in gene.getDict().iteritems():
                if(value>0):
                    res=res+","+str(key)+"*"+str(value)+" "
            output.append(res)
            i+=1
        self.render("UI/sol.html", outp=output,req=inputDict)

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'UI/static/'}),
        (r"/solution",SolutionHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()