import os
import sys

cuurent_dir = os.getcwd()
sys.path.append(cuurent_dir)

from models import split

class PercentSplit(split.Split):

    def __init__(self, amount, splits):
        self.amount = amount
        self.splits = splits

    def validateAndCalculateSplit(self):
        amount = self.amount
        splits = self.splits

        temp = 0.0
        for email, percent in splits.items():
            temp += percent
        print("PERCENT SPLIT")
        print(float(temp),float(100))
        if float(temp) != float(100):
            return {
                "success": "false",
                "message": "Invalid Splits"
            }
        else:
            finalSplits = {}
            for email,percent in splits.items():
                amt = (percent/100)*amount
                finalSplits[email] = amt
            return {
                "success": "true",
                "data": finalSplits
            }

