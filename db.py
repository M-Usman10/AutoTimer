from tools import get_date, get_time
from configs import MONGODB_CONNECTION_STRING,TIMELOG_METAKEYS
from pymongo import MongoClient
import re

class Data:
    def __init__(self,db_name,collection_name):
        self.connection_string = MONGODB_CONNECTION_STRING
        self.db_name = db_name
        self.collection_name = collection_name
        self.client, self.db, self.collection = None,None,None

    def make_client(self):
        self.client = MongoClient(self.connection_string)

    def make_db(self):
        if self.client is None:
            self.make_client()
        self.db = self.client[self.db_name]

    def make_collection(self):
        if self.db is None:
            self.make_db()
        self.collection = self.db[self.collection_name]

    def insert_timelog(self, time_log):
        if set(time_log.keys()) == TIMELOG_METAKEYS:
            if self.collection:
                self.collection.insert_one(time_log)
            else:
                print("No collection exists")
        else:
            print("Keys not matching with metainfo")

    def get_timelog(self,date, activity):
        if self.collection:
            time_log = self.collection.find_one({"activity":activity,"date":date})
        else:
            print("No collection exists")
        return time_log

data = Data(db_name="time-logs",collection_name="logs-data")
data.make_collection()
record1 ={"id":1,
          "time":get_time(),
          "date":get_date(),
          "activity":"Vmware",
          "duration": 100
          }
data.insert_timelog(record1)
print(data.get_timelog(get_date(),"Vmware"))