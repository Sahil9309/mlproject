import os
import sys
from src.logger import logging
from src.exception import CustomException

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


class TrainPipeline:
    def __init__(self):
        pass

    def start_training(self):
        """
        Start the complete ML training pipeline
        """
        try:
            logging.info("Starting the training pipeline")
            
            # Data Ingestion
            data_ingestion = DataIngestion()
            train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed successfully")
            
            # Data Transformation
            data_transformation = DataTransformation()
            train_arr, test_arr, preprocessor_path = data_transformation.initiate_data_transformation(
                train_data_path, test_data_path
            )
            logging.info("Data transformation completed successfully")
            
            # Model Training
            model_trainer = ModelTrainer()
            r2_score = model_trainer.initiate_model_trainer(train_arr, test_arr)
            logging.info(f"Model training completed successfully with R2 score: {r2_score}")
            
            return r2_score
            
        except Exception as e:
            logging.error("Error occurred in training pipeline")
            raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        pipeline = TrainPipeline()
        score = pipeline.start_training()
        print(f"Training completed successfully! R2 Score: {score}")
    except Exception as e:
        print(f"Training failed: {e}")
        raise e