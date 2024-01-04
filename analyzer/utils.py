from enum import Enum
import time

def time_count(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print("Time spent in "+func.__name__+": ", time.time()-start_time)
        return result
    return wrapper


class TokenType(Enum):
    # Enumerate the token types
    reserved = 0
    identifier = 1
    constant = 2
    operator = 3
    separator = 4
    string = 5
    space = 6
    comment = 7
    error = 8

class Token:
    def __init__(self, token, tokenType):
        self.token = token
        self.tokenType = tokenType

    def __str__(self):
        return "Token: "+str(self.token)+" - Type: "+str(self.tokenType)
    
'''
Signals are used in transition list

'''
class Signal(Enum):
    S = 0
    line = 2
    readable = 3
    list_part = 4
    readable_after_identifier = 5
    identifier_list_part = 6
    align_end = 7
    

class ErrorType(Enum):
    # Enumerate the error types
    lexicalError = 0
    syntaxError = 1
    semanticError = 2
    warning = 3