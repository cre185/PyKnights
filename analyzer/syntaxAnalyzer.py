from errorHandler import ErrorType
from utils import *
from collections import deque
from treelib import Node, Tree

class Transition:
    def __init__(self, fromToken, toTokenList):
        self.fromToken = fromToken
        self.toTokenList = toTokenList

class SyntaxAnalyzer:
    def __init__(self, errorHandler):
        self.errorHandler = errorHandler
        # initialize the transitions and transition table here
        self.transitions = []
        self.transition_table = {'a':[]}

    def analyze(self, tokens):
        stack = deque()
        stack.append(Token('S', TokenType.error))
        i=0
        while stack.count() != 0:
            top = stack.pop()
            if top.islower(): # but what can imply top is a terminal?
                if tokens[i].tokenType == top: # actually how to identify a target token remain unspecified
                    i+=1
                else:
                    self.errorHandler.addError(ErrorType.syntaxError, 'Syntax Error: Unexpected token ' + top)
            else: # a non-terminal
                table_entry = self.table[top][tokens[i].tokenType]
                # push the expected transitions onto the stack