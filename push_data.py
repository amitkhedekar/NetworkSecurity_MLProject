import os
import sys
import json

from dotenv import load_dotenv
load_dotenv() ##initialize env variable

MONGO_DB_URL = os.getenv("MONGO_DB_URL") ##parameter name is maintained in env file
# print(MONGO_DB_URL)

import certifi ##certifi is python package to estable secure HTTP connection

##get all the bundles of certificates from certifi and store in variable ca (certificate authority)
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e , sys)
        
    def csv_to_json_convertor(self, file_path):
        '''
        To convert csv datafile into json to upload into mongo db
        '''
        try:
            data = pd.read_csv(file_path)
            ##reset the index since csv file might be hving own index
            data.reset_index(drop = True, inplace= True)
            
            ##convert it into list of json records
            records = list(json.loads(data.T.to_json()).values())

            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            
            ##mongo client to connect to MomgoDB
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            
            ##connect to database within mongo
            self.database = self.mongo_client[self.database]

            ##connect to mongo collection within dabase
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            return len(self.records)
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

if __name__ ==  "__main__":
    FILE_PATH = 'Project_Data\phisingData.csv'
    DATABASE = "AmitAI"
    COLLECTION  = "NetworkProjectData"

    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_convertor(file_path = FILE_PATH)
    print(records)
    records_uploaded = network_obj.insert_data_mongodb(records = records, database=DATABASE, collection= COLLECTION)
    print(records_uploaded)