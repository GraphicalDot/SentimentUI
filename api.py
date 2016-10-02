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
import optparse
from concurrent.futures import ThreadPoolExecutor
from Sentence_Tokenization import SentenceTokenizationOnRegexOnInterjections
from nltk.stem import SnowballStemmer 
from PreProcessingText import PreProcessText
from sklearn.feature_extraction.text import CountVectorizer 
from cPickle import dump, load, HIGHEST_PROTOCOL

Terminal = blessings.Terminal()

file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(file_path)

from configs import SentimentClassifiersPath, TagClassifiersPath,\
                FoodClassifiersPath, ServiceClassifiersPath,\
                AmbienceClassifiersPath, CostClassifiersPath 


from configs import SentimentVocabularyFileName, SentimentFeatureFileName, SentimentClassifierFileName
from configs import TagVocabularyFileName, TagFeatureFileName, TagClassifierFileName
from configs import FoodVocabularyFileName, FoodFeatureFileName, FoodClassifierFileName
from configs import ServiceVocabularyFileName, ServiceFeatureFileName, ServiceClassifierFileName
from configs import CostVocabularyFileName, CostFeatureFileName, CostClassifierFileName
from configs import AmbienceVocabularyFileName, AmbienceFeatureFileName, AmbienceClassifierFileName



from configs import cd
import cPickle


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




def prediction(data, classifier, vocabulary, features):
                loaded_vectorizer= CountVectorizer(vocabulary=vocabulary) 
                sentences_counts = loaded_vectorizer.transform(sentences)
                reduced_features = features.transform(sentences_counts.toarray())
                predictions = classifier.predict(reduced_features)
                return zip(sentences, predictions)




class PostText(tornado.web.RequestHandler):


        @cors
        @print_execution
        @tornado.gen.coroutine
        def post(self):
                print PATH_COMPILED_CLASSIFIERS

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
        http_server.start(20)
        enable_pretty_logging()
        print Terminal.green("Server is started at localhost and running at post 8000")
        tornado.ioloop.IOLoop.instance().start()




if __name__ == "__main__":
        """
        application.listen(8000)
        tornado.autoreload.start()
        tornado.ioloop.IOLoop.instance().start()
        """

        parser = optparse.OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
        
        
        parser.add_option("-p", "--path_compiled_classifiers",
                      action="store", # optional because action defaults to "store"
                      dest="path_compiled_classifiers",
                      default=None,
                      help="Path for compiled classifiers",)
        
        (options, args) = parser.parse_args()
        PATH_COMPILED_CLASSIFIERS = options.path_compiled_classifiers


        with cd(ServiceClassifiersPath(PATH_COMPILED_CLASSIFIERS)):
                        service_features =  load(open(ServiceFeatureFileName, 'rb'))
                        service_vocabulary = load(open(ServiceVocabularyFileName, 'rb'))
                        service_classifier= load(open(ServiceClassifierFileName, 'rb'))

        
        print Terminal.green("<<%s>> classifiers and vocabulary loaded"%"Service") 
        
        with cd(SentimentClassifiersPath(PATH_COMPILED_CLASSIFIERS)):
                        sentiment_features =  load(open(SentimentFeatureFileName, 'rb'))
                        service_vocabulary = load(open(SentimentVocabularyFileName, 'rb'))
                        service_classifier= load(open(SentimentClassifierFileName, 'rb'))
        print Terminal.green("<<%s>> classifiers and vocabulary loaded"%"Sentiment") 
        
        
        with cd(TagClassifiersPath(PATH_COMPILED_CLASSIFIERS)):
                        tag_features =  load(open(TagFeatureFileName, 'rb'))
                        tag_vocabulary = load(open(TagVocabularyFileName, 'rb'))
                        tag_classifier= load(open(TagClassifierFileName, 'rb'))
        print Terminal.green("<<%s>> classifiers and vocabulary loaded"%"Tag") 
        
        with cd(FoodClassifiersPath(PATH_COMPILED_CLASSIFIERS)):
                        food_features =  load(open(FoodFeatureFileName, 'rb'))
                        food_vocabulary = load(open(FoodVocabularyFileName, 'rb'))
                        food_classifier= load(open(FoodClassifierFileName, 'rb'))
        print Terminal.green("<<%s>> classifiers and vocabulary loaded"%"Food") 
        
        with cd(CostClassifiersPath(PATH_COMPILED_CLASSIFIERS)):
                        cost_features =  load(open(CostFeatureFileName, 'rb'))
                        cost_vocabulary = load(open(CostVocabularyFileName, 'rb'))
                        cost_classifier= load(open(CostClassifierFileName, 'rb'))
        print Terminal.green("<<%s>> classifiers and vocabulary loaded"%"Cost") 
        
        with cd(AmbienceClassifiersPath(PATH_COMPILED_CLASSIFIERS)):
                        ambience_features =  load(open(AmbienceFeatureFileName, 'rb'))
                        ambience_vocabulary = load(open(AmbienceVocabularyFileName, 'rb'))
                        ambience_classifier= load(open(AmbienceClassifierFileName, 'rb'))
        print Terminal.green("<<%s>> classifiers and vocabulary loaded"%"Ambience") 


        main()





