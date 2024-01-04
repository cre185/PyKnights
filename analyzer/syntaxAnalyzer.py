from errorHandler import ErrorType
from utils import *
from collections import deque
from treelib import Node, Tree


class SyntaxAnalyzer:
    def __init__(self, errorHandler):
        self.errorHandler = errorHandler
        # initialize the transitions and transition table here
        self.transitions = [
            (Signal.S, []),
            (Signal.S, [Signal.line, Token('0', TokenType.space), Signal.S]),
            (Signal.line, [Token('import', TokenType.reserved), Token('', TokenType.identifier)]),
            (Signal.line, [Signal.readable]),
            (Signal.line, [Token('', TokenType.comment)]),
            (Signal.line, [Token('def', TokenType.reserved), Token('', TokenType.identifier), Token('(', TokenType.separator), Token('', TokenType.identifier), \
                           Signal.identifier_list_part, Token(')', TokenType.separator), Token(':', TokenType.separator), Token('+', TokenType.space), Signal.line, Signal.align_end]),
            (Signal.line, [Token('while', TokenType.reserved), Signal.readable, Token(':', TokenType.separator), Token('+', TokenType.space), Signal.line, Signal.align_end]),
            (Signal.line, [Token('if', TokenType.reserved), Signal.readable, Token(':', TokenType.separator), Token('+', TokenType.space), Signal.line, Signal.align_end]),
            (Signal.line, [Token('break', TokenType.reserved)]),
            (Signal.line, [Token('continue', TokenType.reserved)]),
            (Signal.line, [Token('pass', TokenType.reserved)]),
            (Signal.line, [Token('else', TokenType.reserved), Token(':', TokenType.separator), Token('+', TokenType.space), Signal.line, Signal.align_end]),
            (Signal.line, [Token('elif', TokenType.reserved), Signal.readable, Token(':', TokenType.separator), Token('+', TokenType.space), Signal.line, Signal.align_end]),
            (Signal.align_end, [Token('-', TokenType.space)]),
            (Signal.align_end, [Token('0', TokenType.space), Signal.line, Signal.align_end]),
            (Signal.align_end, []),
            (Signal.readable, [Token('', TokenType.identifier), Signal.readable_after_identifier]),
            (Signal.readable, [Token('', TokenType.constant), Signal.readable_after_identifier]),
            (Signal.readable, [Token('', TokenType.string), Signal.readable_after_identifier]),
            (Signal.readable, [Token('[', TokenType.separator), Signal.readable, Signal.list_part, Token(']', TokenType.separator)]),
            (Signal.readable, [Token('(', TokenType.separator), Signal.readable, Signal.list_part, Token(')', TokenType.separator)]),
            (Signal.readable, [Token('False', TokenType.reserved)]),
            (Signal.readable, [Token('True', TokenType.reserved)]),
            (Signal.readable, [Token('None', TokenType.reserved)]),
            (Signal.readable_after_identifier, []),
            (Signal.readable_after_identifier, [Token('.', TokenType.separator), Token('', TokenType.identifier), Signal.readable_after_identifier]),
            (Signal.readable_after_identifier, [Token('(', TokenType.separator), Signal.readable, Signal.list_part, Token(')', TokenType.separator), Signal.readable_after_identifier]),
            (Signal.readable_after_identifier, [Token('[', TokenType.separator), Signal.readable, Token(']', TokenType.separator), Signal.readable_after_identifier]),
            (Signal.readable_after_identifier, [Token('', TokenType.operator), Signal.readable, Signal.readable_after_identifier]),
            (Signal.readable_after_identifier, [Token('in', TokenType.reserved), Signal.readable]),
            (Signal.list_part, [Token(',', TokenType.separator), Signal.readable, Signal.list_part]),
            (Signal.list_part, []),
            (Signal.identifier_list_part, [Token(',', TokenType.separator), Token('', TokenType.identifier), Signal.identifier_list_part]),
            (Signal.identifier_list_part, []),
        ]

    def table(self, non_terminal, token):
        # return the expected transitions for the given non-terminal and token
        match non_terminal:
            case Signal.S:
                if token.tokenType == TokenType.error and token.token == '#':
                    return 0
                else:
                    return 1
            case Signal.line:
                if token.tokenType == TokenType.reserved and token.token == 'import':
                    return 2
                elif token.tokenType == TokenType.identifier:
                    return 3
                elif token.tokenType == TokenType.comment:
                    return 15
                elif token.tokenType == TokenType.reserved and token.token == 'break':
                    return 23
                elif token.tokenType == TokenType.reserved and token.token == 'continue':
                    return 24
                elif token.tokenType == TokenType.reserved and token.token == 'pass':
                    return 25
            case Signal.readable:
                if token.tokenType == TokenType.identifier:
                    return 4
                elif token.tokenType == TokenType.constant:
                    return 5
                elif token.tokenType == TokenType.string:
                    return 6
                elif token.tokenType == TokenType.separator and token.token == '[':
                    return 7
                elif token.tokenType == TokenType.separator and token.token == '(':
                    return 10
                elif token.tokenType == TokenType.reserved and token.token == 'False':
                    return 26
                elif token.tokenType == TokenType.reserved and token.token == 'True':
                    return 27
                elif token.tokenType == TokenType.reserved and token.token == 'None':
                    return 28
            case Signal.list_part:
                if token.tokenType == TokenType.separator and token.token == ',':
                    return 8
                else:
                    return 9
            case Signal.readable_after_identifier:
                if token.tokenType == TokenType.separator and token.token == '.':
                    return 12
                elif token.tokenType == TokenType.separator and token.token == '(':
                    return 13
                elif token.tokenType == TokenType.separator and token.token == '[':
                    return 14
                elif token.tokenType == TokenType.operator:
                    return 18
                elif token.tokenType == TokenType.reserved and token.token == 'in':
                    return 31
                else:
                    return 11
            case Signal.align_end:
                if token.tokenType == TokenType.space and token.token == '-':
                    return 20
                elif token.tokenType == TokenType.space and token.token == '0':
                    return 21
                elif token.tokenType == TokenType.error and token.token == '#':
                    return 37
            case Signal.identifier_list_part:
                if token.tokenType == TokenType.separator and token.token == ',':
                    return 29
                else:
                    return 30
            case Signal.line, Signal.align_end:
                if token.token == 'def' or token.token == 'while' or token.token == 'if' or token.token == 'else' or token.token == 'elif':
                    return 35
                else:
                    return 34
        return -1
        
    def preprocess(self, tokens):
        # return the processed tokens
        i=0
        history_space=0
        standard_space=4
        while i < len(tokens):
            if tokens[i].tokenType == TokenType.space:
                if tokens[i].token.count('\n') == 0:
                    tokens=tokens[:i]+tokens[i+1:]
                    continue
                else:
                    tmp = len(tokens[i].token.split('\n')[-1])
                    shift_count = (tmp-history_space)//standard_space
                    tokens[i].token = '0'
                    if shift_count!=0:
                        sig = '+' if shift_count > 0 else '-'
                        for j in range(abs(shift_count)):
                            tokens.insert(i+1, Token(sig, TokenType.space))
                        i+=shift_count
                        history_space=tmp
            i+=1
        tokens.append(Token('#', TokenType.error))
        '''for token in tokens:
            print(token)'''
        return tokens

    def analyze(self, tokens):
        tokens = self.preprocess(tokens)
        stack = deque()
        stack.append(Signal.S)
        tree = Tree()
        tree.create_node(tag='S', identifier='S')
        stack_for_tree = deque()
        stack_for_tree.append('S')
        signal_count = 0
        token_count = 0
        i=0
        while len(stack) != 0 and i < len(tokens):
            top = stack.pop()
            if isinstance(top, Token):
                if tokens[i].tokenType == top.tokenType:
                    if tokens[i].tokenType == TokenType.space or tokens[i].tokenType == TokenType.reserved or tokens[i].tokenType == TokenType.separator:
                        if tokens[i].token == top.token:
                            i+=1
                            tree.create_node(tag=top.token, identifier=top.token+str(token_count), parent=stack_for_tree.pop())
                            token_count+=1
                    else:
                        i+=1
                        tree.create_node(tag=top.token, identifier=top.token+str(token_count), parent=stack_for_tree.pop())
                        token_count+=1
                else:
                    print('Syntax Error: Unexpected token ' + str(tokens[i])+', expected '+str(top))
                    for j in range(10):
                        print(tokens[i+j])
                    # self.errorHandler.addError(ErrorType.syntaxError, 'Syntax Error: Unexpected top token ' + str(top))
            else: # a non-terminal
                table_entry = self.table(top, tokens[i])
                if table_entry == -1:
                    '''for sth in stack:
                        print(sth)'''
                    print('Syntax Error: Unexpected token ' + str(tokens[i]) + ' with ' + str(top))
                    # self.errorHandler.addError(ErrorType.syntaxError, 'Syntax Error: Unexpected table token ' + str(tokens[i]))
                    continue
                tree.create_node(tag=top.name, identifier=top.name+str(signal_count), parent=stack_for_tree.pop())
                for sth in reversed(self.transitions[table_entry][1]):
                    stack.append(sth)
                    stack_for_tree.append(top.name+str(signal_count))
                signal_count+=1
        if i != len(tokens) or len(stack) != 0:
            self.errorHandler.addError(ErrorType.syntaxError, 'Syntax Error: Unexpected end of file')
            return tree
