from abc import ABC, abstractmethod

class Split(ABC):

    @abstractmethod
    def validateAndCalculateSplit(self):
        pass

