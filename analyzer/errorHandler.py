from enum import Enum
import time

def time_count(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print("Time spent in "+func.__name__+": ", time.time()-start_time)
        return result
    return wrapper

class ErrorType(Enum):
    # Enumerate the error types
    lexicalError = 0
    syntaxError = 1
    semanticError = 2
    warning = 3

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