
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



corenlp_data = dict(
        ip = "localhost",
        port = 3456,
)



SentimentClassifiersPath = lambda base_dir:  "%s/CompiledModels/SentimentClassifiers"%base_dir
TagClassifiersPath = lambda base_dir: "%s/CompiledModels/TagClassifiers"%base_dir
FoodClassifiersPath = lambda base_dir: "%s/CompiledModels/FoodClassifiers"%base_dir
ServiceClassifiersPath = lambda base_dir : "%s/CompiledModels/ServiceClassifiers"%base_dir
AmbienceClassifiersPath = lambda base_dir: "%s/CompiledModels/AmbienceClassifiers"%base_dir
CostClassifiersPath = lambda base_dir : "%s/CompiledModels/CostClassifiers"%base_dir



SentimentVocabularyFileName = "lk_vectorizer_sentiment.joblib"
SentimentFeatureFileName = "sentiment_features.joblib"
SentimentClassifierFileName = "svmlk_sentiment_classifier.joblib"

TagVocabularyFileName = "lk_vectorizer_tag.joblib"
TagFeatureFileName = "tag_features_pca_selectkbest.joblib"
TagClassifierFileName = "svmlk_tag_classifier.joblib"

FoodVocabularyFileName = "lk_vectorizer_food.joblib"
FoodFeatureFileName = "food_features_pca_selectkbest.joblib"
FoodClassifierFileName = "svmlk_food_classifier.joblib"

ServiceVocabularyFileName =  "lk_vectorizer_service.joblib"
ServiceFeatureFileName = "service_features_pca_selectkbest.joblib"
ServiceClassifierFileName = "svmlk_service_classifier.joblib"

CostVocabularyFileName = "lk_vectorizer_cost.joblib"
CostFeatureFileName =  "cost_features_pca_selectkbest.joblib"
CostClassifierFileName = "svmlk_cost_classifier.joblib"

AmbienceVocabularyFileName = "lk_vectorizer_ambience.joblib"
AmbienceFeatureFileName = "ambience_features_pca_selectkbest.joblib"
AmbienceClassifierFileName = "svmlk_ambience_classifier.joblib"

tags = ['cuisine', 'service', 'food', 'menu', 'overall', 'cost', 'place',
        'ambience', 'null']




