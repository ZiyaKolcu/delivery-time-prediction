from DeliveryTimePrediction.config.configuration import ConfigurationManager
from DeliveryTimePrediction.components.model_trainer import ModelTrainer
from DeliveryTimePrediction.logging.logger import logging

STAGE_NAME = "Model Trainer Stage"


class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def initiate_model_trainer(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer_config = ModelTrainer(config=model_trainer_config)
        model_trainer_config.train()
