from errorHandler import ErrorType
from utils import *
from collections import deque
from treelib import Node, Tree


class SyntaxAnalyzer:
    def __init__(self, errorHandler):
        self.errorHandler = errorHandler
        # initialize the transitions and transition table here
        self.transitions = [
            (Signal.S, [Signal.line, Signal.S]),
            (Signal.S, []),
            (Signal.line, [Token('import', TokenType.reserved), Token('module', TokenType.identifier)]),
        ]

    def table(self, non_terminal, token):
        # return the expected transitions for the given non-terminal and token
        match non_terminal:
            case Signal.S:
                return 1 if token.tokenType == TokenType.error and token.token == '#' else 0
            case Signal.line:
                if token.tokenType == TokenType.reserved and token.token == 'import':
                    return 2
        return -1
        
    def preprocess(self, tokens):
        # return the processed tokens
        i=0
        history_space=0
        while i < len(tokens):
            if tokens[i].tokenType == TokenType.space:
                if tokens[i].token.count('\n') == 0:
                    tokens=tokens[:i]+tokens[i+1:]
                    continue
                else:
                    tmp = len(tokens[i].token.split('\n')[-1])
                    tokens[i].token=str(tmp-history_space)
                    history_space=tmp
            i+=1
        tokens.append(Token('#', TokenType.error))
        return tokens

    def analyze(self, tokens):
        tokens = self.preprocess(tokens)
        stack = deque()
        stack.append(Signal.S)
        i=0
        while len(stack) != 0:
            top = stack.pop()
            if top is Token:
                if tokens[i].tokenType == top: # actually how to identify a target token remain unspecified
                    i+=1
                else:
                    self.errorHandler.addError(ErrorType.syntaxError, 'Syntax Error: Unexpected signal ' + str(top))
            else: # a non-terminal
                table_entry = self.table(top, tokens[i])
                if table_entry == -1:
                    self.errorHandler.addError(ErrorType.syntaxError, 'Syntax Error: Unexpected token ' + str(tokens[i]))
                    continue
                for sth in reversed(self.transitions[table_entry][1]):
                    stack.append(sth)