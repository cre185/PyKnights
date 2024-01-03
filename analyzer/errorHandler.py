from enum import Enum
from utils import ErrorType

class Error:
    def __init__(self, errorType, errorText):
        self.errorType = errorType
        self.errorText = errorText

    def __str__(self):
        return self.errorType.name + ": " + self.errorText
    
class ErrorHandler:
    def __init__(self):
        self.errors = []

    def addError(self, errorType, errorText):
        self.errors.append(Error(errorType, errorText))

    def handleError(self):
        for error in self.errors:
            print(error)
    
    def clear(self):
        self.errors = []