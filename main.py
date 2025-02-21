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
from DeliveryTimePrediction.pipeline.model_trainer_pipeline import (
    ModelTrainerTrainingPipeline,
)
from DeliveryTimePrediction.pipeline.model_evaluation_pipeline import (
    ModelEvaluationTrainingPipeline,
)
from DeliveryTimePrediction.pipeline.model_prediction_pipeline import (
    ModelPredictionTrainingPipeline,
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


STAGE_NAME = "Model Trainer stage"
try:
    logging.info(f">>>>> {STAGE_NAME} started <<<<<")
    model_trainer = ModelTrainerTrainingPipeline()
    model_trainer.initiate_model_trainer()
    logging.info(f">>>>> {STAGE_NAME} completed <<<<<")
except Exception as e:
    logging.exception(e)
    raise e


STAGE_NAME = "Model Evaluation Stage"

try:
    logging.info(f">>>>> {STAGE_NAME} started <<<<<")
    data_ingestion = ModelEvaluationTrainingPipeline()
    data_ingestion.initiate_model_evaluation()
    logging.info(f">>>>> {STAGE_NAME} completed <<<<<")

except Exception as e:
    logging.exception(e)
    raise e

STAGE_NAME = "Model Prediction Stage"

example_input = {
    "store_primary_category": "american",
    "order_protocol": 1.0,  # 1 - 7
    "total_items": 3,  # 1 - 7
    "subtotal": 400,  # 400 - 6000
    "num_distinct_items": 2,  # 1 - 6
    "min_item_price": 5,  # 0 - 1999
    "max_item_price": 50,  # 100 - 2000
    "total_outstanding_orders": 3.0,  # 3 - 180
    "dasher_latency_rate": 0.5,  # 0.5 - 1.25
    "delay_time": 250,  # 250 - 1500
    "hour": 14,  # 0 - 23
    "day_of_week_num": 0,  # 0 - 6
    "dashers_per_order": 0.4,  # 0.4 - 1.4
    "%_dashers_avail": 0.4,  # 0.4 - 0.6
    "total_busy_dashers": 2,  # 0 - 150
    "delivery_difficulty": 100,  # 100 - 1500
    "historical_avg_delivery_time": 20,  # 20 - 75
    "delivery_speed": 5,  # 1 - 12
}


try:
    logging.info(f">>>>> {STAGE_NAME} started <<<<<")
    model_prediction = ModelPredictionTrainingPipeline()
    predicted_time = model_prediction.initiate_model_prediction(example_input)
    logging.info(f"Predicted Delivery Time: {predicted_time:.2f} minutes")
    logging.info(f">>>>> {STAGE_NAME} completed <<<<<")

except Exception as e:
    logging.exception(e)
    raise e
