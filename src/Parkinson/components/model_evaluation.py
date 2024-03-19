import os
import pandas as pd
from Parkinson.utils.common import save_json
from urllib.parse import urlparse
import numpy as np
import joblib
from Parkinson.entity.config_entity import ModelEvaluationConfig
from pathlib import Path
from sklearn.metrics import accuracy_score


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self,Y_pred, actual):
        accuracy = accuracy_score(Y_pred, actual) * 100
        return accuracy
        
    
    def save_results(self):

        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)
        
        # Drop the 'name' column
        test_data.drop(['name'], axis=1, inplace=True)

        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[[self.config.target_column]]
        
        predicted_qualities = model.predict(test_x)

        (accuracy) = self.eval_metrics(test_y, predicted_qualities)
        
        # Saving metrics as local
        scores = {"accuracy":accuracy}
        save_json(path=Path(self.config.metric_file_name), data=scores)