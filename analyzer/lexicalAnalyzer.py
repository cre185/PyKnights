import keyword # for reserved words
from automata.fa.nfa import NFA # for automata
from enum import Enum
import re

class TokenType(Enum):
    # Enumerate the token types
    reserved = 0
    identifier = 1
    constant = 2
    operator = 3
    separator = 4

class Token:
    def __init__(self, token, tokenType):
        self.token = token
        self.tokenType = tokenType

    def __str__(self):
        return "Token: {self.token} - Type: {self.tokenType}"
    

class LexicalAnalyzer:
    def __init__(self):
        self.reservedWords = keyword.kwlist
        self.init_nfa()

    def init_nfa(self):
        # Initialize the NFA used for the lexical analyzer
        self.nfa = []
        # Reserved words
        self.nfa.append(NFA.from_regex('|'.join(self.reservedWords)))

    def analyze(self, tokens) -> list[Token]:
        # Analyze the tokens and return a list of Token objects
        token_list = []
        i,j=1,0
        while i < len(tokens)+1:
            token = tokens[j:i]
            for k,nfa in enumerate(self.nfa):
                if nfa.accepts_input(token):
                    # Generate token
                    print("Token: ", token, " - Type: ", TokenType(k))
                    token_list.append(Token(token, k))
                    j=i
                    break
            i+=1
        if j < len(tokens):
            print("Warning: Unrecognized token from: ", tokens[j:] if len(tokens[j:]) < 100 else tokens[j:j+100] + "...")
        return token_list


if __name__ == "__main__":
    analyzer = LexicalAnalyzer()
    '''with open("./test.py", "r", encoding='utf-8') as myfile:
        tokens = myfile.read()
        print(analyzer.analyze(tokens))'''
    print(analyzer.analyze("if else while for break continue pass return def"))