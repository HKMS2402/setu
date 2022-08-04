import os
import sys

cuurent_dir = os.getcwd()
sys.path.append(cuurent_dir)

from models import split


class EqualSplit(split.Split):

    def __init__(self,amount,splits):
        self.amount = amount
        self.splits = splits

    def validateAndCalculateSplit(self):
        size = len(self.splits)
        equalAmount = self.amount/size
        result = {}
        for i in self.splits:
            result[i] = equalAmount
        
        
        return {
            "success" : "true",
            "data" : result
        }


