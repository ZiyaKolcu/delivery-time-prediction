from DeliveryTimePrediction.logging.logger import logging
from DeliveryTimePrediction.config.configuration import ConfigurationManager
from DeliveryTimePrediction.components.data_validation import DataValidation

STAGE_NAME = "Data Validation Stage"


class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_validation(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()


if __name__ == "__main__":
    try:
        logging.info(f">>>>> {STAGE_NAME} started <<<<<")
        data_validation = DataValidationTrainingPipeline()
        data_validation.initiate_data_validation()
        logging.info(f">>>>> {STAGE_NAME} completed <<<<<")

    except Exception as e:
        logging.exception(e)
        raise e
