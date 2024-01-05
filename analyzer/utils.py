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
    assigner = 9

class Token:
    def __init__(self, token, tokenType):
        self.token = token
        self.tokenType = tokenType

    def __str__(self):
        return "Token: "+str(self.token)+" - Type: "+str(self.tokenType)
    
'''
Signals are used in transition list
S: start signal, representing the whole program, can be split into lines
line: representing a line, have a bunch of complex possible representations
readable: representing a readable, it must at least provide a value that can be assigned to a mutable
readable_list: representing a list of readables
readable_list_part: representing a part of a list consisting of readables
identifier_list: representing a list of identifiers
identifier_list_part: representing a part of a list consisting of identifiers
align_end: treating the possible end of an indent block, so it can be aligned with the start of the block
after_identifier: representing what a line can appear after accepting an identifier
readable_after_identifier: representing what a readable can appear after accepting an identifier
inherit: representing the inheritance of a class
import_goods: representing things that can be imported
'''
class Signal(Enum):
    S = 0
    line = 1
    readable = 2
    readable_list = 3
    readable_list_part = 4
    identifier_list = 5
    identifier_list_part = 6
    align_end = 7
    after_identifier = 8
    readable_after_identifier = 9
    inherit = 10
    import_goods = 11
    

class ErrorType(Enum):
    # Enumerate the error types
    lexicalError = 0
    syntaxError = 1
    semanticError = 2
    warning = 3