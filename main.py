import sys
from src.components.data_injestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from src.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()

        ## Data Ingestion steps
        data_ingestion_config = DataIngestionConfig(training_pipeline_config = training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config = data_ingestion_config)
        logging.info("Initiate the data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation completed")
        print(data_ingestion_artifact)
        
        ## Data Validation steps
        data_validation_config = DataValidationConfig(training_pipeline_config = training_pipeline_config)
        data_validation = DataValidation( data_ingestion_artifact = data_ingestion_artifact,
                                          data_validation_config = data_validation_config)
        logging.info("Initiate Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation completed")
        print(data_validation_artifact)

        ## Data Transformation steps
        data_transformation_config = DataTransformationConfig( training_pipeline_config = training_pipeline_config)
        data_transformation = DataTransformation( data_validation_artficat = data_validation_artifact ,
                                                  data_transformation_config = data_transformation_config )
        logging.info("Initiate Data Transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation completed")
        print(data_transformation_artifact)

        

        

    except Exception as e:
        raise NetworkSecurityException(e, sys)


