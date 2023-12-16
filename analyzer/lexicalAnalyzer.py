import keyword
import time # for reserved words
from automata.fa.nfa import NFA # for automata
from enum import Enum

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
        return "Token: "+self.token+" - Type: "+str(self.tokenType)
    

class LexicalAnalyzer:
    def __init__(self):
        self.reservedWords = keyword.kwlist
        # Initialize some useful variables
        self.all_char = [chr(i) for i in range(0, 128)] # definition for characters that can be accepted
        self.epsilon_nfa = NFA(
            states={'q0', 'q1'},
            input_symbols={i for i in self.all_char},
            transitions={'q0': {'': {'q1'}}},
            initial_state='q0',
            final_states={'q1'}
        )
        self.init_nfa()

    def range_nfa(self, str_list):
        # Generate an NFA for a range of characters
        states = {'s'}
        transition = {'s':{'':set()}}
        final_states = set()
        for j, strng in enumerate(str_list):
            states.add('q'+str(j)+'_0')
            transition['s'][''].add('q'+str(j)+'_0')
            for i,c in enumerate(strng):
                states.add('q'+str(j)+'_'+str(i+1))
                transition['q'+str(j)+'_'+str(i)] = {str(c):{'q'+str(j)+'_'+str(i+1)}}
            final_states.add('q'+str(j)+'_'+str(len(strng)))
            transition['q'+str(j)+'_'+str(len(strng))] = {}
        return NFA(
            states=states,
            input_symbols={ch for ch in self.all_char},
            transitions=transition,
            initial_state='s',
            final_states=final_states
        )
    
    def kleene_positive(self, nfa):
        return nfa + nfa.kleene_star()

    def init_nfa(self):
        start_time = time.time()
        # Initialize the NFA used for the lexical analyzer
        self.nfa = []
        # Reserved words
        azAZ_ = [chr(i) for i in range(ord('a'), ord('z')+1)] + [chr(i) for i in range(ord('A'), ord('Z')+1)] + ['_']
        azAZ09_ = azAZ_ + [chr(i) for i in range(ord('0'), ord('9')+1)]
        all_except = [i for i in self.all_char if i not in azAZ09_]
        self.nfa.append(self.range_nfa(self.reservedWords)+self.range_nfa(all_except))
        # Identifiers
        self.nfa.append(self.range_nfa(azAZ_) + self.range_nfa(azAZ09_).kleene_star()+self.range_nfa(all_except))
        # Constants
        num = self.range_nfa([chr(i) for i in range(ord('0'), ord('9')+1)])
        num_except = self.range_nfa([i for i in self.all_char if i not in num])
        self.nfa.append(self.kleene_positive(num) + num_except)
        # Operators
        double_operator_except = [i for i in self.all_char if i not in '=*/><']
        triple_operator_except = [i for i in self.all_char if i not in '=']
        self.nfa.append(
            self.range_nfa(['+', '-', '*', '/', '%', '=', '<', '>', '&', '|', '^', '~', '.']) + self.range_nfa(
                double_operator_except))
        self.nfa.append(
            self.range_nfa(
                ['+=', '-=', '*=', '/=', '%=', '==', '!=', '<=', '>=', '&=', '|=', '^=', '~=', '**', '//', '>>',
                 '<<']) + self.range_nfa(
                triple_operator_except))
        self.nfa.append(self.range_nfa(['**=', '//=', '>>=', '<<=']))
        # Separators
        self.nfa.append(self.range_nfa(['(', ')', '[', ']', '{', '}', ',', ':', ';']))
        # Strings
        single_line_except = [i for i in self.all_char if i not in "\n"]
        double_line_except = [i for i in self.all_char if i not in '\n"']
        double_line_except.append('\\"')
        double_paragragh_except = [i for i in self.all_char if i not in '"']
        double_line_except.append('\\"')
        self.nfa.append(
            self.range_nfa(['\'']) + self.range_nfa(single_line_except).kleene_star() + self.range_nfa([i for i in single_line_except if i not in "\\"]) + self.range_nfa(['\'']))
        self.nfa.append(self.range_nfa(["\'\'"]) + self.range_nfa([i for i in self.all_char if i != '\'']))
        self.nfa.append(
            self.range_nfa(["\'\'\'"]) +(self.range_nfa(self.all_char).kleene_star()+self.range_nfa([i for i in self.all_char if i not in "\\"])).union(self.epsilon_nfa)+ self.range_nfa(
                ["\'\'\'"]))

        self.nfa.append(
            self.range_nfa(['\"']) + self.range_nfa(double_line_except).kleene_star() + self.range_nfa([i for i in single_line_except if i not in "\\"]) + self.range_nfa(['\"']))
        self.nfa.append(self.range_nfa(["\"\""]) + self.range_nfa([i for i in self.all_char if i != '\"']))
        self.nfa.append(
            self.range_nfa(["\"\"\""]) + self.range_nfa(double_paragragh_except).kleene_star() + self.range_nfa(
                ["\"\"\""]))
        # Spaces
        space_except = [i for i in self.all_char if i not in " \t\n"]
        self.nfa.append(self.kleene_positive(self.range_nfa([' ', '\t', '\n']))+self.range_nfa(space_except))
        # Comments
        self.nfa.append(self.range_nfa(['#']) + self.range_nfa([i for i in self.all_char if i != '\n']).kleene_star() + self.range_nfa(['\n']))
        print("NFA initialization time: ", time.time()-start_time)

    def analyze(self, tokens) -> list[Token]:
        time_start = time.time()
        # Analyze the tokens and return a Tokenline
        token_list = []
        i,j=1,0
        while i < len(tokens)+1:
            token = tokens[j:i]
            for k,nfa in enumerate(self.nfa):
                if nfa.accepts_input(token):
                    # Need to leave last character out if it's: reserved words, identifiers, constants, comments
                    if k in [0,1,2,3,4,8,11,13,14]:
                        i-=1
                        token = token[:-1]
                    # Generate token
                    if k in [0, 1, 2]:
                        token_list.append(Token(token, TokenType(k)))
                    elif k in [3, 4, 5]:
                        token_list.append(Token(token, TokenType(3)))
                    elif k == 6:
                        token_list.append(Token(token, TokenType(k - 2)))
                    elif k in [7, 8, 9, 10, 11, 12]:
                        token_list.append(Token(token, TokenType(5)))
                    else:
                        token_list.append(Token(token, TokenType(k-7)))
                    j=i
                    break
            i+=1
        if j < len(tokens):
            print("Warning: Unrecognized token at: ", tokens[j:] if len(tokens[j:]) < 30 else tokens[j:] + "...")
            token_list.append(Token(tokens[j], TokenType.error))
            next_token = tokens[j+1:]
            token_list += self.analyze(next_token)
        # remove spaces for testing
        # token_list = [token for token in token_list if not (token.tokenType == TokenType.space and token.token == " ")]
        print("Lexical analysis time: ", time.time()-time_start)
        return token_list


if __name__ == "__main__":
    analyzer = LexicalAnalyzer()
    with open(r"./test.py", "r", encoding='utf-8') as myfile:
        # tokens = myfile.read()
        tokens = r"self.range_nfa(['\'']) + self.kleene_positive(self.range_nfa(single_line_except)) + self.range_nfa(['\'']))"
        result = analyzer.analyze(tokens)
        for token in result:
            print(token)
