from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:
    root_dir: Path
    local_data_dir: Path


@dataclass
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    local_data_dir: Path
    all_schema: dict


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    preprocessor_path: Path


@dataclass
class ModelTrainerConfig:
    root_dir: Path
    preprocessor_path: Path
    model_dir: Path
    train_data_path: Path
    test_data_path: Path
    alpha: float
    l1_ratio: float
    max_iter: int
    tol: float
    target_column: str


@dataclass
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    all_params: dict
    metric_file_name: Path
    target_column: str
    mlflow_uri: str


@dataclass
class ModelPredictionConfig:
    root_dir: Path
    model_path: Path
    prediction_file_path: Path
