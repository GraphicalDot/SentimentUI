
import os
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)




SentimentClassifiersPath = lambda base_dir:  "%s/CompiledModels/SentimentClassifiers"%base_dir
TagClassifiersPath = lambda base_dir: "%s/CompiledModels/TagClassifiers"%base_dir
FoodClassifiersPath = lambda base_dir: "%s/CompiledModels/FoodClassifiers"%base_dir
ServiceClassifiersPath = lambda base_dir : "%s/CompiledModels/ServiceClassifiers"%base_dir
AmbienceClassifiersPath = lambda base_dir: "%s/CompiledModels/AmbienceClassifiers"%base_dir
CostClassifiersPath = lambda base_dir : "%s/CompiledModels/CostClassifiers"%base_dir



SentimentVocabularyFileName = "lk_vectorizer_sentiment.pkl"
SentimentFeatureFileName = "sentiment_features.pkl"
SentimentClassifierFileName = "svmlk_sentiment_classifier.pkl"

TagVocabularyFileName = "lk_vectorizer_tag.pkl"
TagFeatureFileName = "tag_features_pca_selectkbest.pkl"
TagClassifierFileName = "svmlk_tag_classifier.pkl"

FoodVocabularyFileName = "lk_vectorizer_food.pkl"
FoodFeatureFileName = "food_features_pca_selectkbest.pkl"
FoodClassifierFileName = "svmlk_food_classifier.pkl" 

ServiceVocabularyFileName =  "lk_vectorizer_service.pkl"
ServiceFeatureFileName = "service_features_pca_selectkbest.pkl"
ServiceClassifierFileName = "svmlk_service_classifier.pkl"

CostVocabularyFileName = "lk_vectorizer_cost.pkl"
CostFeatureFileName =  "cost_features_pca_selectkbest.pkl"
CostClassifierFileName = "svmlk_cost_classifier.pkl"

AmbienceVocabularyFileName = "lk_vectorizer_ambience.pkl"
AmbienceFeatureFileName = "ambience_features_pca_selectkbest.pkl"
AmbienceClassifierFileName = "svmlk_ambience_classifier.pkl"


tags = ['cuisine', 'service', 'food', 'menu', 'overall', 'cost', 'place',
        'ambience', 'null']




