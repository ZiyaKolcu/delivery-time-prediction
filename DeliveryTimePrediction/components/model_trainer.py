import pandas as pd
import os
from DeliveryTimePrediction.entity.config_entity import ModelTrainerConfig
from DeliveryTimePrediction.logging.logger import logging
from DeliveryTimePrediction.utils.common import save_bin, load_bin
from sklearn.linear_model import ElasticNet
from sklearn.pipeline import Pipeline
import joblib


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        train_x = train_data.drop([self.config.target_column], axis=1)
        train_y = train_data[[self.config.target_column]].values.ravel()

        elasticnet_model = ElasticNet(
            alpha=self.config.alpha,
            l1_ratio=self.config.l1_ratio,
            max_iter=self.config.max_iter,
            tol=self.config.tol,
        )

        preprocessor = load_bin(path=self.config.preprocessor_path)

        pipeline = Pipeline(
            steps=[("preprocessor", preprocessor), ("model", elasticnet_model)]
        )

        pipeline.fit(train_x, train_y)
        save_bin(data=pipeline, file_path=self.config.model_dir)
