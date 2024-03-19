import pandas as pd
import os
from loggingg import logging
from xgboost import XGBClassifier
import joblib
from Parkinson.entity.config_entity import ModelTrainerConfig



class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config


    
    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)
        
        # Drop the 'name' column
        train_data.drop(['name'], axis=1, inplace=True)
        test_data.drop(['name'], axis=1, inplace=True)


        train_x = train_data.drop([self.config.target_column], axis=1)
        test_x = test_data.drop([self.config.target_column], axis=1)
        train_y = train_data[[self.config.target_column]]
        test_y = test_data[[self.config.target_column]]
        
        
        

        lr = XGBClassifier()
        lr.fit(train_x, train_y)
        
        Y_pred = lr.predict(test_x)

        joblib.dump(lr, os.path.join(self.config.root_dir, self.config.model_name))

