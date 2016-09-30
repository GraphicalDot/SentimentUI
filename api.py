#!/usr/bin/env python
from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.autoreload 
import tornado.httpserver
import json
from tornado.log import enable_pretty_logging
from tornado.httpclient import AsyncHTTPClient
import pymongo
import os
import sys
from functools import update_wrapper
from functools import wraps
import time
import blessings
from concurrent.futures import ThreadPoolExecutor

Terminal = blessings.Terminal()

file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(file_path)





def cors(f):
        @wraps(f) # to preserve name, docstring, etc.
        def wrapper(self, *args, **kwargs): # **kwargs for compability with functions that use them
                self.set_header("Access-Control-Allow-Origin",  "*")
                self.set_header("Access-Control-Allow-Headers", "content-type, accept")
                self.set_header("Access-Control-Max-Age", 60)
                return f(self, *args, **kwargs)
        return wrapper
                               


def print_execution(func):
        "This decorator dumps out the arguments passed to a function before calling it"
        argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
        fname = func.func_name
        def wrapper(*args,**kwargs):
                start_time = time.time()
                print Terminal.green("Now {0} have started executing".format(func.func_name))
                result = func(*args, **kwargs)
                print Terminal.green("Total time taken by {0} for execution is--<<{1}>>\n".format(func.func_name, (time.time() - start_time)))
                return result
        return wrapper






class PostText(tornado.web.RequestHandler):


        @cors
        @print_execution
        @tornado.gen.coroutine
        def post(self):
                try:
                        text = self.get_argument("text")
                except tornado.web.MissingArgumentError:
                        self.set_status(400, "Missing Arhument")
                        self.write({"messege": "give me the money"})
                        self.finish()
                        return 
                

                if not text:
                        self.set_status(400, "Empty Text")
                        self.write({"success": False, 
                                    "error": True,
                                    "message": "Dont send empty text"})
                        self.finish()
                        return 



                self.set_status(200)
                result = [
                    {"sentence": "I will become what i deserve", "sentiment":
                        "positive", "category": "food", "sub_category": "dishes", "noun_phrases": ["deserver", "delhi", "noida", "banoffie pie"]},
                    {"sentence": "I think therefore i am", "sentiment":
                        "neutral", "category": "food", "sub_category": "dishes", "noun_phrases": ["deserver", "delhi", "noida", "banoffie pie"]},
                    {"sentence": "I want to go to paris and do somwthing worth mentioing in my later life", "sentiment":
                        "positive", "category": "food", "sub_category": "dishes", "noun_phrases": ["deserver", "delhi", "noida", "banoffie pie"]},
                    ]
                    
                self.write({"success": True, 
                            "error": False,
                            "result": result,
                            })
                self.finish()
                return






class Application(tornado.web.Application):
        def __init__(self):
                handlers = [
                    (r"/post_text", PostText),
                    (r"/images/^(.*)", tornado.web.StaticFileHandler, {"path": "./images"},),
                    (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": "/css"},),
                    (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": "/js"},),]
                settings = dict(cookie_secret="ed3fc328ab47ee27c8f6a72bd5a1b647deb24ab590e7060a803c51c6",)
                tornado.web.Application.__init__(self, handlers, **settings)
                #self.executor = ThreadPoolExecutor(max_workers=60)


def stopTornado():
        tornado.ioloop.IOLoop.instance().stop()


def main():
        http_server = tornado.httpserver.HTTPServer(Application())
        http_server.bind("8000")
        http_server.start(10)
        enable_pretty_logging()
        Terminal.green("Server is started at localhost and running at post 8000")
        tornado.ioloop.IOLoop.instance().start()




if __name__ == "__main__":
        """
        application.listen(8000)
        tornado.autoreload.start()
        tornado.ioloop.IOLoop.instance().start()
        """
        main()





