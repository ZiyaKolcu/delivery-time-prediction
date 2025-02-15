from DeliveryTimePrediction.logging.logger import logging
from DeliveryTimePrediction.pipeline.data_ingestion_pipeline import (
    DataIngestionTrainingPipeline,
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