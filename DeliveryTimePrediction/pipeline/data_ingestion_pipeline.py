from DeliveryTimePrediction.logging.logger import logging
from DeliveryTimePrediction.config.configuration import ConfigurationManager
from DeliveryTimePrediction.components.data_ingestion import DataIngestion


STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        df = data_ingestion.export_database_table_as_dataframe()
        data_ingestion.export_data_into_file(dataframe=df)

if __name__ == "__main__":
    try:
        logging.info(f">>>>> {STAGE_NAME} started <<<<<")
        data_ingestion = DataIngestionTrainingPipeline()
        data_ingestion.initiate_data_ingestion()
        logging.info(f">>>>> {STAGE_NAME} completed <<<<<")
    except Exception as e:
        logging.exception(e)
        raise e