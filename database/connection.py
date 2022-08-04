from pymongo import MongoClient

class MongoConnection:
    def __init(self):
        self.connection = None

    def getConnection(self):
        try:
            self.connection = MongoClient("mongodb://localhost:27017/")
            print("Connected to MongoDB")
            return self.connection
        except:  
            print("Could not connect to MongoDB")


    def closeConnection(self):
        print("Connection to MongoDB closed")
        self.connection.close()

