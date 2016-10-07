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
from sklearn.externals import joblib
from topia.termextract import extract  
from textblob import TextBlob
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
from configs import tags, corenlp_data


from configs import cd
import cPickle


import sys
import jsonrpc
corenlpserver = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),
                jsonrpc.TransportTcpIp(addr=(corenlp_data["ip"],
                corenlp_data["port"])))


def find_places(sentence):
        def filter_places(__list):
                location_list = list()
                i = 0
                for __tuple in __list:
                        if __tuple[1] == "LOCATION":
                                location_list.append([__tuple[0], i])
                                i += 1


                i = 0
                try:
                        new_location_list = list()
                        [first_element, i] = location_list.pop(0)
                        new_location_list.append([first_element])
                        for element in location_list:
                                if i == element[1] -1:
                                        new_location_list[-1].append(element[0])

                                else:
                                        new_location_list.append([element[0]])
                                i = element[1]

                        return list(set([" ".join(element) for element in new_location_list]))
                except Exception as e:
                        return None


        try:
                result = loads(corenlpserver.parse(sentence))
                __result = [(e[0], e[1].get("NamedEntityTag")) for e in result["sentences"][0]["words"]]
                place_name = filter_places(__result)
                print "%s in %s"%(place_name, sentence)

        except Exception as e:
                print e, "__extract_place", sentence
                place_name = []

        return place_name

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




def prediction(sentences, vocabulary, features, classifier):
                print sentences
                loaded_vectorizer= CountVectorizer(vocabulary=vocabulary) 
                
                sentences_counts = loaded_vectorizer.transform(sentences)
                
                reduced_features = features.transform(sentences_counts.toarray())
                         
                predictions = classifier.predict(reduced_features)
                print predictions
                return predictions



def filter_categories(sentences):
        """
        These sentences will be in the form (sentence, tag, sentiment)
        """
        tags = set([tag for (sentence, tag, sentiment) in sentences])
        result = dict()
        for tag in tags:
                result.update({tag: [e for e in sentences if e[1]==tag]})

        return result



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

                places = list()
                
                tokenized_sentences = sent_tokenizer.tokenize(text)
                #predicting tags
                tags = prediction(tokenized_sentences, tag_vocabulary, tag_features, tag_classifier)
                sentiments = prediction(tokenized_sentences, sentiment_vocabulary, sentiment_features, sentiment_classifier)


                #Result will be in the form of dict with each key represents
                # a category and each category will then have a list of sentence
                #tag sentiment in it
                result = filter_categories(zip(tokenized_sentences, tags,
                    sentiments))

                overall_result = list() 



                some_lambda= lambda ((sentence, category, sentiment), sub): (sentence, category, sentiment, sub) 
                other_categories = lambda (sentence, category, sentiment): (sentence, category, sentiment, None)
                
                if result.get("food"):
                        food_sentences = [sentence for (sentence, category, sentiment) in result["food"]]
                        food_subs = prediction(food_sentences, food_vocabulary,
                                food_features, food_classifier)

                        __text = " ".join(food_sentences)
                        tb_nps = TextBlob(__text)
                        topia_nps = [np[0] for np in extractor(__text)]
                        nps = list(set.union(set(tb_nps.noun_phrases), set(topia_nps)))

                        food_result = map(some_lambda, zip(result["food"], food_subs))
                        overall_result.extend(food_result)
        

                if result.get("service"):
                        service_sentences = [sentence for (sentence, category,
                            sentiment) in result["service"]]
                        service_subs = prediction(service_sentences,
                                service_vocabulary, service_features, service_classifier)
                        service_result = map(some_lambda, zip(result["service"], service_subs))
                        overall_result.extend(service_result)

                if result.get("cost"):
                        cost_sentences = [sentence for (sentence, category,
                            sentiment) in result["cost"]]
                        cost_subs = prediction(cost_sentences, cost_vocabulary,
                                cost_features, cost_classifier)
                        cost_result = map(some_lambda, zip(result["cost"], cost_subs))
                        overall_result.extend(cost_result)


                if result.get("ambience"):
                        ambience_sentences = [sentence for (sentence, category,
                            sentiment) in result["ambience"]]
                        ambience_subs = prediction(ambience_sentences,
                                ambience_vocabulary, ambience_features,
                                ambience_classifier)
                        ambience_result = map(some_lambda,
                                zip(result["ambience"], ambience_subs))
                        overall_result.extend(ambience_result)

                if result.get("menu"):
                        menu_result = map(other_categories, result["menu"])
                        overall_result.extend(food_result)

                if result.get("place"):
                        place_result = map(other_categories, result["place"])
                        overall_result.extend(place_result)
                        for (sent, _, _, _) in place_result:
                            try:
                                    places.append(find_places(sent))
                            except Exception as e:
                                    print e
                                    print "Coprenlp server is not running, so\
                                            something about it dude!"


                if result.get("overall"):
                        verall_result = map(other_categories, result["overall"])
                        overall_result.extend(verall_result)
                
                if result.get("cuisine"):
                        cuisine_result = map(other_categories, result["cuisine"])
                        overall_result.extend(cuisine_result)
                
                if result.get("null"):
                        null_result = map(other_categories, result["null"])
                        overall_result.extend(null_result)
                        
                            

                make_json = lambda (sentence, category, sentiment, sub): {"sentence": sentence, "category":
                                category, "sentiment": sentiment, "sub_category": sub}



                result = map(make_json, overall_result)
                try:
                        noun_phrases = nps
                except Exception as e:
                        noun_phrases = None


                self.set_status(200)
                print result
                print noun_phrases
                print places
                self.write({"success": True, 
                            "error": False,
                            "result": result,
                            "places": filter(None, places),
                            "noun_phrases": noun_phrases, 
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
        http_server.start()
        #enable_pretty_logging()
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
                        service_features =  joblib.load(ServiceFeatureFileName)
                        service_vocabulary = joblib.load(ServiceVocabularyFileName)
                        service_classifier= joblib.load(ServiceClassifierFileName)

        
        print Terminal.green("<<%s>> classifiers and vocabulary loaded"%"Service") 
        
        with cd(SentimentClassifiersPath(PATH_COMPILED_CLASSIFIERS)):
                        sentiment_features =  joblib.load(SentimentFeatureFileName)
                        sentiment_vocabulary = joblib.load(SentimentVocabularyFileName)
                        sentiment_classifier= joblib.load(SentimentClassifierFileName)
        print Terminal.green("<<%s>> classifiers and vocabulary loaded"%"Sentiment") 
        
        
        with cd(TagClassifiersPath(PATH_COMPILED_CLASSIFIERS)):
                        tag_features =  joblib.load(TagFeatureFileName)
                        tag_vocabulary = joblib.load(TagVocabularyFileName)
                        tag_classifier= joblib.load(TagClassifierFileName)
        print Terminal.green("<<%s>> classifiers and vocabulary loaded"%"Tag") 
        
        with cd(FoodClassifiersPath(PATH_COMPILED_CLASSIFIERS)):
                        food_features =  joblib.load(FoodFeatureFileName)
                        food_vocabulary = joblib.load(FoodVocabularyFileName)
                        food_classifier= joblib.load(FoodClassifierFileName)
        print Terminal.green("<<%s>> classifiers and vocabulary loaded"%"Food") 
        
        with cd(CostClassifiersPath(PATH_COMPILED_CLASSIFIERS)):
                        cost_features =  joblib.load(CostFeatureFileName)
                        cost_vocabulary = joblib.load(CostVocabularyFileName)
                        cost_classifier= joblib.load(CostClassifierFileName)
        print Terminal.green("<<%s>> classifiers and vocabulary loaded"%"Cost") 
        
        with cd(AmbienceClassifiersPath(PATH_COMPILED_CLASSIFIERS)):
                        ambience_features =  joblib.load(AmbienceFeatureFileName)
                        ambience_vocabulary = joblib.load(AmbienceVocabularyFileName)
                        ambience_classifier= joblib.load(AmbienceClassifierFileName)
        print Terminal.green("<<%s>> classifiers and vocabulary loaded"%"Ambience") 

        sent_tokenizer  = SentenceTokenizationOnRegexOnInterjections()
        print Terminal.green("Sentence Tokenizer has been initialized") 
        extractor = extract.TermExtractor()
        main()





