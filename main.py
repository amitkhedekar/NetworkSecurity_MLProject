import sys
from src.components.data_injestion import DataIngestion
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config = trainingpipelineconfig)
        data_ingestion = DataIngestion(data_ingestion_config = data_ingestion_config)
        logging.info("Initiate the data ingestion")

        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)


