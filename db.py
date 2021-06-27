from collections import defaultdict
import json
import logging
import os
from pymongo import MongoClient

from tools import get_date, get_time
from configs import MONGODB_CONNECTION_STRING,TIMELOG_METAKEYS,ID

class Data:
    """
    Data class maintains timelogs locally and in the cloud database
    """
    def __init__(self,db_name,collection_name):
        self.connection_string = MONGODB_CONNECTION_STRING
        self.db_name = db_name
        self.collection_name = collection_name
        self.client, self.db, self.collection = None,None,None

    def make_client(self):
        """
        Makes a MongoDB client, an exception is thrown if connection string is not correct
        """
        self.client = MongoClient(self.connection_string)

    def make_db(self):
        """
        Initializes db object for a pre-existing database in MongoDB
        """
        if self.client is None:
            self.make_client()
        self.db = self.client[self.db_name]

    def make_collection(self):
        """
        MongoDB stores data in the form of collections, we are initializing our collection here
        """
        if self.db is None:
            self.make_db()
        self.collection = self.db[self.collection_name]

    def get_timelog(self,date, activity):
        """
        Fetches one time log entry form cloud database
        """
        if self.collection:
            time_log = self.collection.find_one({"activity":activity,"date":date})
        else:
            logging.info("No collection exists")
        return time_log

    @staticmethod
    def load_time_logs():
        """
        Loads time logs from local storage
        """
        if os.path.isfile("timelogs.json"):
            with open("timelogs.json") as file:
                time_logs = json.load(file)
            return defaultdict(lambda :{"id":ID,"duration":0,"date":get_date(),"time":get_time()},time_logs)
        return defaultdict(lambda :{"id":ID,"duration":0,"date":get_date(),"time":get_time()}, {})

    def insert_timelogs_to_db(self, time_logs):
        """
        Performs validation and Inserts one time log entry to the database
        """
        logging.info("Saving Data to Json")
        if len(time_logs):
            time_log = time_logs[0]
            if set(time_log.keys()) == TIMELOG_METAKEYS:
                if self.collection:
                    self.collection.insert_many(time_logs)
                else:
                    logging.info("No collection exists, could not save timelogs")
            else:
                logging.info("Keys not matching with metadata info")

    def save_time_logs(self,time_logs):
        """
        Saves time logs to local storage
        """
        with open("timelogs.json","w") as file:
            json.dump(time_logs, file)
        
        #Saving to cloud
        self.insert_timelogs_to_db(time_logs)

if __name__ == "__main__":
    data = Data(db_name="time-logs",collection_name="logs-data")
    record1 ={
              "id":1,
              "time":get_time(),
              "date":get_date(),
              "activity":"Vmware",
              "duration": 100
              }
    data.insert_timelog(record1)
    logging.info(data.get_timelog(get_date(),"Vmware"))