import os
import sys

cuurent_dir = os.getcwd()
sys.path.append(cuurent_dir)

from models import split

class EqualSplit(split.Split):

    def __init__(self, amount, splits):
        self.amount = amount
        self.splits = splits

    def validateAndCalculateSplit(self):
        amount = self.amount
        splits = self.splits

        temp = 0.0
        for email, amt in splits.items():
            temp += amt
        print(float(temp), float(amount))
        if float(temp) == float(amount):
            return {
                "success": "true",
                "data": splits
            }
        else:
            return {
                "success": "false",
                "message": "Invalid Splits"
            }

