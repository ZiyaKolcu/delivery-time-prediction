from DeliveryTimePrediction.logging.logger import logging
from DeliveryTimePrediction.pipeline.data_ingestion_pipeline import (
    DataIngestionTrainingPipeline,
)
from DeliveryTimePrediction.pipeline.data_validation_pipeline import (
    DataValidationTrainingPipeline,
)
from DeliveryTimePrediction.pipeline.data_transformation_pipeline import (
    DataTransformationTrainingPipeline,
)

STAGE_NAME = "Data Ingestion Stage"

if __name__ == "__main__":
    try:
        logging.info(f">>>>> {STAGE_NAME} started <<<<<")
        data_ingestion = DataIngestionTrainingPipeline()
        data_ingestion.initiate_data_ingestion()
        logging.info(f">>>>> {STAGE_NAME} completed <<<<<")
    except Exception as e:
        logging.exception(e)
        raise e


STAGE_NAME = "Data Validation Stage"
try:
    logging.info(f">>>>> {STAGE_NAME} started <<<<<")
    data_validation = DataValidationTrainingPipeline()
    data_validation.initiate_data_validation()
    logging.info(f">>>>> {STAGE_NAME} completed <<<<<")
except Exception as e:
    logging.exception(e)
    raise e


STAGE_NAME = "Data Transformation stage"

try:
    logging.info(f">>>>> {STAGE_NAME} started <<<<<")
    data_transformation = DataTransformationTrainingPipeline()
    data_transformation.initiate_data_transformation()
    logging.info(f">>>>> {STAGE_NAME} completed <<<<<")
except Exception as e:
    logging.exception(e)
    raise e
