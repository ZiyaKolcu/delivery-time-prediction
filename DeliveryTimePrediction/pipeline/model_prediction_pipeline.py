from DeliveryTimePrediction.config.configuration import ConfigurationManager
from DeliveryTimePrediction.components.model_prediction import ModelPrediction
from DeliveryTimePrediction.logging.logger import logging

class ModelPredictionTrainingPipeline:
    def __init__(self):
        pass

    def initiate_model_prediction(self, data):
        config = ConfigurationManager()
        model_prediction_config = config.get_model_prediction_config()
        model_prediction_config = ModelPrediction(config=model_prediction_config)
        return model_prediction_config.predict(data)
