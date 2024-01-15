from utils import *
from collections import deque
from treelib import Tree


class SyntaxAnalyzer:
    def __init__(self, errorHandler):
        self.errorHandler = errorHandler
        # initialize the transitions and transition table here
        self.transitions = [
            (Signal.S, []),
            (Signal.S, [Signal.line, Token('0', TokenType.space), Signal.S]),
            (Signal.line, [Token('import', TokenType.reserved), Token('', TokenType.identifier)]),
            (Signal.line, [Token('from', TokenType.reserved), Token('', TokenType.identifier), Token('import', TokenType.reserved), Signal.import_goods]),
            (Signal.line, [Token('def', TokenType.reserved), Token('', TokenType.identifier), Token('(', TokenType.separator), Signal.identifier_list, \
                           Token(')', TokenType.separator), Token(':', TokenType.separator), Token('+', TokenType.space), Signal.line, Signal.align_end]),
            (Signal.line, [Token('while', TokenType.reserved), Signal.readable, Token(':', TokenType.separator), Token('+', TokenType.space), Signal.line, Signal.align_end]), # 5
            (Signal.line, [Token('if', TokenType.reserved), Signal.readable, Token(':', TokenType.separator), Token('+', TokenType.space), Signal.line, Signal.align_end]),
            (Signal.line, [Token('break', TokenType.reserved)]),
            (Signal.line, [Token('continue', TokenType.reserved)]),
            (Signal.line, [Token('pass', TokenType.reserved)]),
            (Signal.line, [Token('else', TokenType.reserved), Token(':', TokenType.separator), Token('+', TokenType.space), Signal.line, Signal.align_end]), # 10
            (Signal.line, [Token('elif', TokenType.reserved), Signal.readable, Token(':', TokenType.separator), Token('+', TokenType.space), Signal.line, Signal.align_end]),
            (Signal.line, [Token('return', TokenType.reserved), Signal.readable]),
            (Signal.line, [Token('yield', TokenType.reserved), Signal.readable]),
            (Signal.line, [Token('raise', TokenType.reserved), Signal.readable]),
            (Signal.line, [Token('class', TokenType.reserved), Token('', TokenType.identifier), Signal.inherit, Token(':', TokenType.separator), Token('+', TokenType.space), Signal.line, Signal.align_end]), # 15
            (Signal.line, [Token('', TokenType.identifier), Signal.after_identifier]),
            (Signal.inherit, [Token('(', TokenType.separator), Signal.identifier_list, Token(')', TokenType.separator)]),
            (Signal.inherit, []),
            (Signal.align_end, [Token('-', TokenType.space)]),
            (Signal.align_end, [Token('0', TokenType.space), Signal.line, Signal.align_end]), # 20
            (Signal.align_end, []),
            (Signal.readable, [Token('', TokenType.identifier), Signal.readable_after_identifier]),
            (Signal.readable, [Token('', TokenType.constant), Signal.readable_after_identifier]),
            (Signal.readable, [Token('-', TokenType.operator), Token('', TokenType.constant), Signal.readable_after_identifier]),
            (Signal.readable, [Token('', TokenType.string), Signal.readable_after_identifier]), # 25
            (Signal.readable, [Token('[', TokenType.separator), Signal.readable_list, Token(']', TokenType.separator)]),
            (Signal.readable, [Token('(', TokenType.separator), Signal.readable_list, Token(')', TokenType.separator)]),
            (Signal.readable, [Token('False', TokenType.reserved)]),
            (Signal.readable, [Token('True', TokenType.reserved)]),
            (Signal.readable, [Token('None', TokenType.reserved)]), # 30
            (Signal.readable_after_identifier, [Token('.', TokenType.separator), Token('', TokenType.identifier), Signal.readable_after_identifier]),
            (Signal.readable_after_identifier, [Token('(', TokenType.separator), Signal.readable_list, Token(')', TokenType.separator), Signal.readable_after_identifier]),
            (Signal.readable_after_identifier, [Token('[', TokenType.separator), Signal.readable, Token(']', TokenType.separator), Signal.readable_after_identifier]),
            (Signal.readable_after_identifier, [Token('', TokenType.operator), Signal.readable, Signal.readable_after_identifier]),
            (Signal.readable_after_identifier, [Token('in', TokenType.reserved), Signal.readable]), # 35
            (Signal.readable_after_identifier, []),
            (Signal.readable_list_part, [Token(',', TokenType.separator), Signal.readable, Signal.readable_list_part]),
            (Signal.readable_list_part, []),
            (Signal.identifier_list_part, [Token(',', TokenType.separator), Token('', TokenType.identifier), Signal.identifier_list_part]),
            (Signal.identifier_list_part, []), # 40
            (Signal.after_identifier, [Token('.', TokenType.separator), Token('', TokenType.identifier), Signal.after_identifier]),
            (Signal.after_identifier, [Token('[', TokenType.separator), Signal.readable, Token(']', TokenType.separator), Signal.after_identifier]),
            (Signal.after_identifier, [Token('', TokenType.assigner), Signal.readable]),
            (Signal.after_identifier, [Signal.readable_after_identifier]),
            (Signal.readable_list, []), # 45
            (Signal.readable_list, [Signal.readable, Signal.readable_list_part]),
            (Signal.identifier_list, [Token('', TokenType.identifier), Signal.identifier_list_part]),
            (Signal.identifier_list, []),
            (Signal.import_goods, [Token('', TokenType.identifier), Signal.identifier_list_part]),
            (Signal.import_goods, [Token('*', TokenType.operator)]), # 50
            (Signal.line, [Signal.readable]),
            (Signal.readable_after_identifier, [Token('and', TokenType.reserved), Signal.readable]),
            (Signal.readable_after_identifier, [Token('or', TokenType.reserved), Signal.readable]),
            (Signal.readable, [Token('not', TokenType.reserved), Signal.readable]),
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
                elif token.tokenType == TokenType.reserved and token.token == 'from':
                    return 3
                elif token.tokenType == TokenType.reserved and token.token == 'def':
                    return 4
                elif token.tokenType == TokenType.reserved and token.token == 'while':
                    return 5
                elif token.tokenType == TokenType.reserved and token.token == 'if':
                    return 6
                elif token.tokenType == TokenType.reserved and token.token == 'break':
                    return 7
                elif token.tokenType == TokenType.reserved and token.token == 'continue':
                    return 8
                elif token.tokenType == TokenType.reserved and token.token == 'pass':
                    return 9
                elif token.tokenType == TokenType.reserved and token.token == 'else':
                    return 10
                elif token.tokenType == TokenType.reserved and token.token == 'elif':
                    return 11
                elif token.tokenType == TokenType.reserved and token.token == 'return':
                    return 12
                elif token.tokenType == TokenType.reserved and token.token == 'yield':
                    return 13
                elif token.tokenType == TokenType.reserved and token.token == 'raise':
                    return 14
                elif token.tokenType == TokenType.reserved and token.token == 'class':
                    return 15
                elif token.tokenType == TokenType.identifier:
                    return 16
                else:
                    return 51
            case Signal.inherit:
                if token.tokenType == TokenType.separator and token.token == '(':
                    return 17
                else:
                    return 18
            case Signal.align_end:
                if token.tokenType == TokenType.space and token.token == '-':
                    return 19
                elif token.tokenType == TokenType.space and token.token == '0':
                    return 20
                elif token.tokenType == TokenType.error and token.token == '#':
                    return 21
            case Signal.readable:
                if token.tokenType == TokenType.identifier:
                    return 22
                elif token.tokenType == TokenType.constant:
                    return 23
                elif token.tokenType == TokenType.operator and token.token == '-':
                    return 24
                elif token.tokenType == TokenType.string:
                    return 25
                elif token.tokenType == TokenType.separator and token.token == '[':
                    return 26
                elif token.tokenType == TokenType.separator and token.token == '(':
                    return 27
                elif token.tokenType == TokenType.reserved and token.token == 'False':
                    return 28
                elif token.tokenType == TokenType.reserved and token.token == 'True':
                    return 29
                elif token.tokenType == TokenType.reserved and token.token == 'None':
                    return 30
                elif token.tokenType == TokenType.reserved and token.token == 'not':
                    return 54
            case Signal.readable_after_identifier:
                if token.tokenType == TokenType.separator and token.token == '.':
                    return 31
                elif token.tokenType == TokenType.separator and token.token == '(':
                    return 32
                elif token.tokenType == TokenType.separator and token.token == '[':
                    return 33
                elif token.tokenType == TokenType.operator:
                    return 34
                elif token.tokenType == TokenType.reserved and token.token == 'in':
                    return 35
                elif token.tokenType == TokenType.reserved and token.token == 'and':
                    return 52
                elif token.tokenType == TokenType.reserved and token.token == 'or':
                    return 53
                else:
                    return 36
            case Signal.readable_list_part:
                if token.tokenType == TokenType.separator and token.token == ',':
                    return 37
                else:
                    return 38
            case Signal.identifier_list_part:
                if token.tokenType == TokenType.separator and token.token == ',':
                    return 39
                else:
                    return 40
            case Signal.after_identifier:
                if token.tokenType == TokenType.separator and token.token == '.':
                    return 41
                elif token.tokenType == TokenType.separator and token.token == '[':
                    return 42
                elif token.tokenType == TokenType.assigner:
                    return 43
                else:
                    return 44
            case Signal.readable_list:
                if token.tokenType == TokenType.separator and (token.token == ']' or token.token == ')'):
                    return 45
                else:
                    return 46
            case Signal.identifier_list:
                if token.tokenType == TokenType.identifier:
                    return 47
                else:
                    return 48
            case Signal.import_goods:
                if token.tokenType == TokenType.identifier:
                    return 49
                elif token.tokenType == TokenType.operator and token.token == '*':
                    return 50
        return -1
        
    def preprocess(self, tokens):
        # return the processed tokens
        i=0
        history_space=0
        standard_space=4
        if len(tokens)!=0 and tokens[-1].tokenType != TokenType.space:
            tokens.append(Token('\n', TokenType.space))
        elif len(tokens)!=0 and tokens[-1].tokenType == TokenType.space:
            tokens[-1].token = '\n'
        while i < len(tokens):
            if tokens[i].tokenType == TokenType.space:
                if tokens[i].token.count('\n') == 0:
                    tokens=tokens[:i]+tokens[i+1:]
                    continue
                else:
                    tmp = len(tokens[i].token.split('\n')[-1])
                    shift_count = (tmp-history_space)//standard_space
                    if shift_count!=0:
                        sig = '+' if shift_count > 0 else '-'
                        tokens=tokens[:i]+tokens[i+1:]
                        if shift_count<0:
                            tokens.insert(i, Token('0', TokenType.space))
                        for j in range(abs(shift_count)):
                            tokens.insert(i, Token(sig, TokenType.space))
                        i+=abs(shift_count)
                        history_space=tmp
                    else:
                        tokens[i].token = '0'
            elif tokens[i].tokenType == TokenType.comment:
                tokens=tokens[:i]+tokens[i+1:]
                if tokens[i].tokenType == TokenType.space and i>0 and tokens[i-1].tokenType == TokenType.space:
                    tokens=tokens[:i-1]+tokens[i:]
                    i-=1
                continue
            i+=1
        while len(tokens)>0 and tokens[0].tokenType == TokenType.space:
            tokens=tokens[1:]
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
                if tokens[i].tokenType == top.tokenType and (top.token == '' or top.token == tokens[i].token):
                    tree.create_node(tag=tokens[i].token, identifier=top.token+str(token_count), parent=stack_for_tree.pop())
                    token_count+=1
                    i+=1
                else:
                    self.errorHandler.addError(ErrorType.syntaxError, 'Syntax Error: Unexpected token ' + str(tokens[i]))
                    i+=1
            else: # a non-terminal
                table_entry = self.table(top, tokens[i])
                if table_entry == -1:
                    self.errorHandler.addError(ErrorType.syntaxError, 'Syntax Error: Unexpected top token ' + str(top))
                    continue
                tree.create_node(tag=top.name, identifier=top.name+str(signal_count), parent=stack_for_tree.pop())
                for sth in reversed(self.transitions[table_entry][1]):
                    stack.append(sth)
                    stack_for_tree.append(top.name+str(signal_count))
                signal_count+=1
        if i != len(tokens)-1 or len(stack) != 0:
            self.errorHandler.addError(ErrorType.syntaxError, 'Syntax Error: Unexpected end of file')
        return tree
