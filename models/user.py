import os
import sys
import json
cuurent_dir = os.getcwd()
sys.path.append(cuurent_dir)
from database import connection

user_cache = {}

class User:
    def __init__(self, name, email, contact):
        self.name = name
        self.email = email
        self.contact = contact
        self.id = None

    @staticmethod
    def getAllUsers():
        result = []
        try:
            dbConnectionInstance = connection.MongoConnection()
            dbConnection = dbConnectionInstance.getConnection()
            database = dbConnection["setu"]
            collection = database["user"]
            data = collection.find({})
            
            data = list(data)
            for i in data:
                result.append({
                    "name": i["name"],
                    "email" : i["email"],
                    "contact" : i["contact"]
                })
            dbConnectionInstance.closeConnection()
            return result
        except Exception as e:
            return {
                "success": "false",
                "message": e
            }

    @staticmethod
    def getUserByEmail(email):
        result = []
        if email in user_cache:
            
            result.append(user_cache[email])
            return result
        else:
                
            try:
                dbConnectionInstance = connection.MongoConnection()
                dbConnection = dbConnectionInstance.getConnection()
                database = dbConnection["setu"]
                collection = database["user"]
                data = collection.find({"email": email})
                
                data = list(data)
                if len(data) > 0:
                        
                    for i in data:
                        result.append({
                            "name": i["name"],
                            "email" : i["email"],
                            "contact" : i["contact"]
                        })
                    dbConnectionInstance.closeConnection()
                    user_cache[email] = {
                            "name": i["name"],
                            "email" : i["email"],
                            "contact" : i["contact"]
                        }
                    
                    return result
                else:
                    return result
            except Exception as e:
                return {
                    "success": "false",
                    "message": e
                }

    def getName(self):
        return self.name

    def getEmail(self):
        return self.email

    def getContact(self):
        return self.contact

    def createUser(self):
        try:
            dbConnectionInstance = connection.MongoConnection()
            dbConnection = dbConnectionInstance.getConnection()
            database = dbConnection["setu"]
            collection = database["user"]
            record = {
                "name": self.name,
                "email": self.email,
                "contact": self.contact
            }
            insert_data = collection.insert_one(record)
            self.id = str(insert_data.inserted_id)
            dbConnectionInstance.closeConnection()
            return {
                "success": "true",
                "data": {
                "name": self.name,
                "email": self.email,
                "contact": self.contact
                }
            }
        except Exception as e:
            print(e)
            return {
                "success": "false",
                "message": "There seems to be some technical error at our end. Please try after sometime."
            }

    def getId(self):
        return self.id



