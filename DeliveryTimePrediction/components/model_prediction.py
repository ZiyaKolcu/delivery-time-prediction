from DeliveryTimePrediction.entity.config_entity import ModelPredictionConfig
from DeliveryTimePrediction.logging.logger import logging
from DeliveryTimePrediction.utils.common import load_bin, save_json
import pandas as pd
import numpy as np


class ModelPrediction:
    def __init__(self, config: ModelPredictionConfig):
        self.config = config

    def predict(self, data):
        df = pd.DataFrame([data])
        df["price_range"] = df["max_item_price"] - df["min_item_price"]
        df["is_weekend"] = df["day_of_week_num"].isin([5, 6]).astype(int)
        df["order_intensity"] = df["total_outstanding_orders"] / (
            df["total_busy_dashers"] + 1e-5
        )
        df["log_subtotal"] = np.log1p(df["subtotal"])
        df["log_outstanding_orders"] = np.log1p(
            df["total_outstanding_orders"].clip(lower=1e-5)
        )
        df["avg_item_price"] = df["subtotal"] / (df["total_items"] + 1e-5)
        df["price_volatility"] = df["price_range"] / (df["avg_item_price"] + 1e-5)

        model = load_bin(path=self.config.model_path)
        prediction = model.predict(df)
        # pred_dict = {"Prediction": prediction[0]}

        # save_json(path=self.config.prediction_file_path, data=pred_dict)
        return prediction[0]
