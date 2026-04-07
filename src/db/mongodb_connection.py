from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self, connection_string=None, db_name='dbprocapi'):
        self.connection_string = connection_string
        self.db_name = db_name
        self.client = None
        self.db = None

    def __enter__(self):
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.db_name]
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()
