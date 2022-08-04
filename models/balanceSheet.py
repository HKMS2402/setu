
import os
import sys

cuurent_dir = os.getcwd()
sys.path.append(cuurent_dir)
from database import connection


class BalanceSheet:
    @staticmethod
    def findBalanceSheetByUserEmail(email):
        result = []
        try:
            dbConnectionInstance = connection.MongoConnection()
            dbConnection = dbConnectionInstance.getConnection()
            database = dbConnection["setu"]
            collection = database["balanceSheet"]
            data = collection.find({"email": email})

            data = list(data)
            if len(data) > 0:

                for i in data:
                    result.append({
                        "email": i["email"],
                        "splits": i["splits"],

                    })
                dbConnectionInstance.closeConnection()
                return result
            else:
                return result
        except Exception as e:
            return {
                "success": "false",
                "message": e
            }

    @staticmethod
    def balanceSheetEntry(paid_by, split):

        dbConnectionInstance = connection.MongoConnection()
        dbConnection = dbConnectionInstance.getConnection()
        database = dbConnection["setu"]
        collection = database["balanceSheet"]
        paidUserBalanceSheet = BalanceSheet.findBalanceSheetByUserEmail(
            paid_by)

        if len(paidUserBalanceSheet) == 0:

            paidUserBalanceSheet = {}
            paidUserBalanceSheet["email"] = paid_by
            paidUserSplits = {}
            for email, amount in split.items():
                if email != paid_by:
                    paidUserSplits[email] = amount

            collection.insert_one({
                "email": paid_by,
                "splits": paidUserSplits

            })

        else:
            paidUserBalanceSheet = paidUserBalanceSheet[0]

            for email, amount in split.items():

                if email in paidUserBalanceSheet["splits"] and email != paid_by:

                    paidUserBalanceSheet["splits"][email] += amount

                elif email != paid_by:

                    paidUserBalanceSheet["splits"][email] = amount

            collection.update_one({"email": paid_by}, {
                                  "$set": {"splits": paidUserBalanceSheet["splits"]}})

        for email, amount in split.items():
            if email != paid_by:
                balanceSheet = BalanceSheet.findBalanceSheetByUserEmail(email)

                if len(balanceSheet) == 0:
                    collection.insert_one({
                        "email": email,
                        "splits": {
                            paid_by: -amount
                        }
                    })
                else:
                    balanceSheet = balanceSheet[0]

                    userSplits = balanceSheet["splits"]

                    if paid_by in userSplits:
                        userSplits[paid_by] -= amount
                    else:
                        userSplits[paid_by] = -amount
                    collection.update_one(
                        {"email": email}, {"$set": {"splits": userSplits}})
        dbConnectionInstance.closeConnection()
        return{
            "success": "true"
        }

    @staticmethod
    def settlePayment(paid_to, paid_by, amount):
        dbConnectionInstance = connection.MongoConnection()
        dbConnection = dbConnectionInstance.getConnection()
        database = dbConnection["setu"]
        collection = database["balanceSheet"]
        paid_to_user = list(collection.find({"email": paid_to}))
        paid_by_user = list(collection.find({"email": paid_by}))

        if len(paid_to_user) == 0:
            data = {
                "email": paid_to
            }
            splits = {}
            splits[paid_by] = -amount

            data["splits"]=splits
            collection.insert_one(data)
        else:
            splits=paid_to_user[0]["splits"]
            if paid_by in splits:
                splits[paid_by]-= amount
            else:
                splits[paid_by]= -amount
            collection.update_one({"email" : paid_to},{"$set": {"splits": splits}})
            
        if len(paid_by_user) == 0:
            data = {
                "email": paid_by
            }
            splits = {}
            splits[paid_to] = amount

            data["splits"]=splits
            collection.insert_one(data)
        else:
            splits=paid_by_user[0]["splits"]
            if paid_to in splits:
                splits[paid_to]+= amount
            else:
                splits[paid_to]= amount
            collection.update_one({"email" : paid_by},{"$set": {"splits": splits}})
        
        dbConnectionInstance.closeConnection()
        return {
            "success" : "true"
        }