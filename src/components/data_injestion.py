from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging

##Configuration of the Data Ingestion Config
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        '''
        takes collection from mongoDB and gives it as dataframe
        '''
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            ##when importing collection from MongoDB _id column gets added
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na" : np.nan} , inplace=True)

            return df
         
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def export_data_into_feature_store(self, dataframe : pd.DataFrame):
        '''
        store the data fetched from Mongodb as raw file in feature store folder
        '''
        try:
            feature_store_file_path  = self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path , exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def split_data_as_train_test(self, dataframe:pd.DataFrame):
        '''
        splits the raw data in train file and test file
        '''
        try:
            train_set, test_set = train_test_split(
                                                    dataframe, 
                                                    test_size=self.data_ingestion_config.train_test_split_ratio
                                                   )
            
            logging.info("Performed Train Test split on dataframe.")

            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path , exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(
                             self.data_ingestion_config.training_file_path,
                             index=False,
                             header=True
                            )

            test_set.to_csv(
                             self.data_ingestion_config.testing_file_path,
                             index=False,
                             header=True
                            )
            
            logging.info(f"Exported tarin and test file path.")

        except Exception as e:
            raise NetworkSecurityException(e , sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()  ##get data from MongoDB
            dataframe = self.export_data_into_feature_store(dataframe = dataframe) ##store data as raw 
            self.split_data_as_train_test(dataframe = dataframe)

            dataingestionartifact = DataIngestionArtifact(
                                                          trained_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path=self.data_ingestion_config.testing_file_path
                                                          )
            
            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException(e , sys)

