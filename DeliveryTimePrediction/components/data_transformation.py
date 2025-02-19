import os
import pandas as pd
import numpy as np
import joblib
from DeliveryTimePrediction.logging.logger import logging
from DeliveryTimePrediction.entity.config_entity import DataTransformationConfig
from DeliveryTimePrediction.utils.common import save_bin
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def remove_outliers_iqr(self, df):
        df_cleaned = df.copy()

        for column in df_cleaned.select_dtypes(include=["float64", "int64"]).columns:
            Q1 = df_cleaned[column].quantile(0.25)
            Q3 = df_cleaned[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_cleaned = df_cleaned[
                (df_cleaned[column] >= lower_bound)
                & (df_cleaned[column] <= upper_bound)
            ]

        return df_cleaned

    def get_data_transformation_object(self, numerical_features, categorical_features):
        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "num",
                    Pipeline(
                        steps=[
                            ("imputer", SimpleImputer(strategy="mean")),
                            ("scaler", StandardScaler()),
                            ("pca", PCA(n_components=0.95)),
                        ]
                    ),
                    numerical_features,
                ),
                (
                    "cat",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                    categorical_features,
                ),
            ]
        )

        return preprocessor

    def transform_data(self):
        data = pd.read_csv(self.config.data_path)
        logging.info(f"Data shape: {data.shape}")

        data["created_at"] = pd.to_datetime(data["created_at"])
        data["actual_delivery_time"] = pd.to_datetime(data["actual_delivery_time"])
        data["delivery_duration_minutes"] = (
            data["actual_delivery_time"] - data["created_at"]
        ).dt.total_seconds() / 60
        data["hour"] = data["created_at"].dt.hour
        data["day_of_week_num"] = data["created_at"].dt.dayofweek
        data["is_weekend"] = data["day_of_week_num"].isin([5, 6]).astype(int)
        data["total_busy_dashers"] = abs(
            data["total_busy_dashers"]
        )  # Handle negative values
        data["total_onshift_dashers"] = abs(data["total_onshift_dashers"])
        data["dashers_per_order"] = data["total_onshift_dashers"] / (
            data["total_outstanding_orders"] + 1e-5
        )
        data["%_dashers_avail"] = data["total_busy_dashers"] / (
            data["total_busy_dashers"] + data["total_onshift_dashers"] + 1e-5
        )
        data["order_intensity"] = data["total_outstanding_orders"] / (
            data["total_busy_dashers"] + 1e-5
        )
        data["delivery_difficulty"] = (
            data["order_intensity"]
            * data["estimated_store_to_consumer_driving_duration"]
        )
        data["price_range"] = data["max_item_price"] - data["min_item_price"]
        data["avg_item_price"] = data["subtotal"] / (data["total_items"] + 1e-5)
        data["price_volatility"] = data["price_range"] / (data["avg_item_price"] + 1e-5)
        data["log_subtotal"] = np.log1p(data["subtotal"])
        data["log_outstanding_orders"] = np.log1p(
            data["total_outstanding_orders"].clip(lower=1e-5)
        )
        data["historical_avg_delivery_time"] = data.groupby(["store_id", "hour"])[
            "delivery_duration_minutes"
        ].transform("mean")

        data["delivery_speed"] = data["historical_avg_delivery_time"] / (
            data["estimated_store_to_consumer_driving_duration"] / 60 + 1e-5
        )
        data = data.drop(
            columns=["market_id", "created_at", "actual_delivery_time", "store_id"],
            axis=1,
        )
        data.dropna(inplace=True)
        data["dasher_latency_rate"] = (
            data["total_busy_dashers"] / data["total_onshift_dashers"]
        )
        data["delay_time"] = (
            data["estimated_store_to_consumer_driving_duration"]
            + data["estimated_order_place_duration"]
        )
        data.drop(
            inplace=True,
            axis=1,
            columns=[
                "total_busy_dashers",
                "total_onshift_dashers",
                "estimated_store_to_consumer_driving_duration",
                "estimated_order_place_duration",
            ],
        )

        data_cleaned = self.remove_outliers_iqr(data)

        X = data_cleaned.drop(["delivery_duration_minutes"], axis=1)
        y = data_cleaned["delivery_duration_minutes"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=True, random_state=5
        )

        categorical_features = ["store_primary_category"]
        numerical_features = [
            "order_protocol",
            "total_items",
            "subtotal",
            "num_distinct_items",
            "min_item_price",
            "max_item_price",
            "total_outstanding_orders",
            "dasher_latency_rate",
            "delay_time",
            "hour",
            "day_of_week_num",
            "is_weekend",
            "dashers_per_order",
            "%_dashers_avail",
            "order_intensity",
            "delivery_difficulty",
            "price_range",
            "avg_item_price",
            "price_volatility",
            "log_subtotal",
            "log_outstanding_orders",
            "historical_avg_delivery_time",
            "delivery_speed",
        ]

        preprocessor_object = self.get_data_transformation_object(
            numerical_features, categorical_features
        )
        file_path = self.config.preprocessor_path
        save_bin(data=preprocessor_object, file_path=file_path)

        train_data = pd.concat([X_train, y_train], axis=1)
        test_data = pd.concat([X_test, y_test], axis=1)

        train_file_path = os.path.join(self.config.root_dir, "train.csv")
        test_file_path = os.path.join(self.config.root_dir, "test.csv")
        train_data.to_csv(train_file_path, index=False)
        test_data.to_csv(test_file_path, index=False)

        logging.info("Splited data into training and test sets.")
        logging.info(f"Train set shape: {train_data.shape}")
        logging.info(f"Test set shape: {test_data.shape}")
