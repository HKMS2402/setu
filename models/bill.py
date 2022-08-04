import os
import sys

cuurent_dir = os.getcwd()
sys.path.append(cuurent_dir)

from models import exactSplit, equalSplit, percentSplit, balanceSheet
from database import connection

bill_cache = {}


class Bill:
    def __init__(self, bill_no, bill_name, category, created_by, paid_by, amount, split_type, splits):
        self.id = None
        self.bill_no = bill_no
        self.bill_name = bill_name
        self.category = category
        self.created_by = created_by
        self.paid_by = paid_by
        self.amount = amount
        self.split_type = split_type
        self.splits = splits

    @staticmethod
    def getBillByBillNumber(bill_no):
        result = []
        if bill_no in bill_cache:

            result.append(bill_cache[bill_no])
            return result
        else:

            try:
                dbConnectionInstance = connection.MongoConnection()
                dbConnection = dbConnectionInstance.getConnection()
                database = dbConnection["setu"]
                collection = database["user"]
                data = collection.find({"bill_no": bill_no})

                data = list(data)
                if len(data) > 0:

                    for i in data:
                        result.append({
                            "name": i["name"],
                            "email": i["email"],
                            "contact": i["contact"]
                        })
                    dbConnectionInstance.closeConnection()
                    bill_cache[bill_no] = {
                        "name": i["name"],
                        "email": i["email"],
                        "contact": i["contact"]
                    }

                    return result
                else:
                    return result
            except Exception as e:
                return {
                    "success": "false",
                    "message": e
                }

    def createBill(self):
        split_type = self.split_type
        print("HERE", split_type)

        if(split_type == "EXACT"):

            splits = exactSplit.EqualSplit(self.amount, self.splits)
            final_splits = splits.validateAndCalculateSplit()
            print(final_splits)
            if(final_splits["success"] == "true"):
                try:
                    dbConnectionInstance = connection.MongoConnection()
                    dbConnection = dbConnectionInstance.getConnection()
                    database = dbConnection["setu"]
                    collection = database["bill"]
                    record = {
                        "bill_no": self.bill_no,
                        "bill_name": self.bill_name,
                        "category": self.category,
                        "created_by": self.created_by,
                        "paid_by": self.paid_by,
                        "amount": self.amount,
                        "split_type": self.split_type,
                        "splits": self.splits
                    }
                    insert_data = collection.insert_one(record)
                    self.id = str(insert_data.inserted_id)
                    dbConnectionInstance.closeConnection()
                    balanceSheet.BalanceSheet.balanceSheetEntry(
                        self.paid_by, self.splits)
                    return {
                        "success": "true",
                        "bill_no": self.bill_no,
                        "bill_name": self.bill_name,
                        "category": self.category,
                        "created_by": self.created_by,
                        "paid_by": self.paid_by,
                        "amount": self.amount,
                        "split_type": self.split_type,
                        "splits": self.splits
                    }
                except Exception as e:
                    return {
                        "success": "false",
                        "message": e
                    }
            else:
                return final_splits

        elif(split_type == "PERCENTAGE"):

            splits = percentSplit.PercentSplit(self.amount, self.splits)
            final_splits = splits.validateAndCalculateSplit()
            print(final_splits)
            if(final_splits["success"] == "true"):
                try:
                    dbConnectionInstance = connection.MongoConnection()
                    dbConnection = dbConnectionInstance.getConnection()
                    database = dbConnection["setu"]
                    collection = database["bill"]
                    record = {
                        "bill_no": self.bill_no,
                        "bill_name": self.bill_name,
                        "category": self.category,
                        "created_by": self.created_by,
                        "paid_by": self.paid_by,
                        "amount": self.amount,
                        "split_type": self.split_type,
                        "splits": self.splits
                    }
                    insert_data = collection.insert_one(record)
                    self.id = str(insert_data.inserted_id)
                    dbConnectionInstance.closeConnection()
                    balanceSheet.BalanceSheet.balanceSheetEntry(
                        self.paid_by, self.splits)
                    return {
                        "success": "true",
                        "bill_no": self.bill_no,
                        "bill_name": self.bill_name,
                        "category": self.category,
                        "created_by": self.created_by,
                        "paid_by": self.paid_by,
                        "amount": self.amount,
                        "split_type": self.split_type,
                        "splits": self.splits
                    }
                except Exception as e:
                    return {
                        "success": "false",
                        "message": e
                    }
            else:
                return final_splits

        elif(split_type == "EQUAL"):
            splits = equalSplit.EqualSplit(self.amount, self.splits)
            final_splits = splits.validateAndCalculateSplit()
            print(final_splits, "FINAL SPLIT")
            if(final_splits["success"] == "true"):
                try:
                    dbConnectionInstance = connection.MongoConnection()
                    dbConnection = dbConnectionInstance.getConnection()
                    database = dbConnection["setu"]
                    collection = database["bill"]
                    record = {
                        "bill_no": self.bill_no,
                        "bill_name": self.bill_name,
                        "category": self.category,
                        "created_by": self.created_by,
                        "paid_by": self.paid_by,
                        "amount": self.amount,
                        "split_type": self.split_type,
                        "splits": self.splits
                    }
                    insert_data = collection.insert_one(record)
                    self.id = str(insert_data.inserted_id)
                    dbConnectionInstance.closeConnection()
                    balanceSheet.BalanceSheet.balanceSheetEntry(
                        self.paid_by,final_splits["data"])
                    return {
                        "success": "true",
                        "bill_no": self.bill_no,
                        "bill_name": self.bill_name,
                        "category": self.category,
                        "created_by": self.created_by,
                        "paid_by": self.paid_by,
                        "amount": self.amount,
                        "split_type": self.split_type,
                        "splits": self.splits
                    }
                except Exception as e:
                    return {
                        "success": "false",
                        "message": e
                    }
            else:
                return final_splits
