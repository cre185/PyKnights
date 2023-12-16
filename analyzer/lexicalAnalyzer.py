from functools import wraps
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
    

def time_count(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print("Time spent in "+func.__name__+": ", time.time()-start_time)
        return result
    return wrapper


class LexicalAnalyzer:
    def __init__(self):
        self.reservedWords = keyword.kwlist
        # Initialize some useful variables
        self.all_char = [chr(i) for i in range(32, 128)] + [chr(10), chr(13), chr(9)] # definition for characters that can be accepted
        self.epsilon_nfa = NFA(
            states={'q0', 'q1'},
            input_symbols={i for i in self.all_char},
            transitions={'q0': {'': {'q1'}}},
            initial_state='q0',
            final_states={'q1'}
        )
        self.init_nfa()

    def range_nfa(self, chr_list):
        # Generate an NFA for a range of characters
        return NFA(
            states={'s', 'f'},
            input_symbols={ch for ch in self.all_char},
            transitions={'s':{c:{'f'} for c in chr_list}, 'f':{}},
            initial_state='s',
            final_states={'f'}
        )
    
    def range_str_nfa(self, str_list):
        # Generate an NFA for a range of strings
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

    @time_count
    def init_nfa(self):
        # Initialize the NFA used for the lexical analyzer
        self.nfa = []
        # Reserved words
        azAZ_ = [chr(i) for i in range(ord('a'), ord('z')+1)] + [chr(i) for i in range(ord('A'), ord('Z')+1)] + ['_']
        azAZ09_ = azAZ_ + [chr(i) for i in range(ord('0'), ord('9')+1)]
        all_except = [i for i in self.all_char if i not in azAZ09_]
        self.nfa.append(self.range_str_nfa(self.reservedWords)+self.range_nfa(all_except))
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
            self.range_nfa(['+', '-', '*', '/', '%', '=', '<', '>', '&', '|', '^', '~', '.', '@']) + self.range_nfa(
                double_operator_except))
        self.nfa.append(
            self.range_str_nfa(
                ['+=', '-=', '*=', '/=', '%=', '==', '!=', '<=', '>=', '&=', '|=', '^=', '~=', '**', '//', '>>',
                 '<<', '->']) + self.range_nfa(
                triple_operator_except))
        self.nfa.append(self.range_str_nfa(['**=', '//=', '>>=', '<<=']))
        # Separators
        self.nfa.append(self.range_nfa(['(', ')', '[', ']', '{', '}', ',', ':', ';']))
        # Strings
        escape_character = ['\\' + i for i in self.all_char]
        single_line_except = [i for i in self.all_char if i not in "\\\'\n"] + escape_character
        double_line_except = [i for i in self.all_char if i not in "\\\"\n"] + escape_character
        single_paragraph_except = [i for i in self.all_char if i not in "\\\'"] + escape_character
        double_paragraph_except = [i for i in self.all_char if i not in "\\\""] + escape_character
        self.nfa.append(self.range_nfa(['\'']) + self.kleene_positive(self.range_str_nfa(single_line_except)) + self.range_nfa(['\'']))
        self.nfa.append(self.range_str_nfa(["\'\'"]) + self.range_nfa([i for i in self.all_char if i != '\'']))
        self.nfa.append(self.range_str_nfa(["\'\'\'"]) + self.range_str_nfa(single_paragraph_except).kleene_star() + self.range_str_nfa(["\'\'\'"]))

        self.nfa.append(self.range_nfa(['\"']) + self.kleene_positive(self.range_str_nfa(double_line_except)) + self.range_nfa(['\"']))
        self.nfa.append(self.range_str_nfa(["\"\""]) + self.range_nfa([i for i in self.all_char if i != '\"']))
        self.nfa.append(self.range_str_nfa(["\"\"\""]) + self.range_str_nfa(double_paragraph_except).kleene_star() + self.range_str_nfa(["\"\"\""]))
        # Spaces
        space_except = [i for i in self.all_char if i not in " \t\n"]
        self.nfa.append(self.kleene_positive(self.range_nfa([' ', '\t', '\n']))+self.range_nfa(space_except))
        # Comments
        self.nfa.append(self.range_nfa(['#']) + self.range_nfa([i for i in self.all_char if i != '\n']).kleene_star() + self.range_nfa(['\n']))

        # Initialize states used for emulating the NFA
        self.states = [nfa._get_lambda_closures()[nfa.initial_state] for nfa in self.nfa]


    @time_count
    def analyze(self, tokens) -> list[Token]:
        result = self.analyze_tokens(tokens)
        return result[:-1] if len(result) > 0 and result[-1].tokenType == TokenType.error else result

    def analyze_tokens(self, tokens) -> list[Token]:
        # Analyze the tokens and return a Tokenline
        token_list = []
        i,j=0,0
        while i < len(tokens):
            for k,nfa in enumerate(self.nfa):
                self.states[k] = nfa._get_next_current_states(self.states[k], tokens[i])
                if not self.states[k].isdisjoint(nfa.final_states):
                    # Need to leave last character out if it's: reserved words, identifiers, constants, spaces, comments
                    if k in [0,1,2,3,4,8,11,13,14]:
                        i-=1
                    # Generate token
                    token = tokens[j:i+1]
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
                    # Reset states
                    j=i+1
                    self.states = [nfa._get_lambda_closures()[nfa.initial_state] for nfa in self.nfa]
                    break
            i+=1
        if j < len(tokens):
            print("Warning: Unrecognized token at: ", tokens[j:] if len(tokens[j:]) < 30 else tokens[j:] + "...")
            token_list.append(Token(tokens[j], TokenType.error))
            token_list += self.analyze_tokens(tokens[j+1:])
        # remove spaces for testing
        # token_list = [token for token in token_list if not (token.tokenType == TokenType.space and token.token == " ")]
        return token_list


if __name__ == "__main__":
    analyzer = LexicalAnalyzer()
    with open(r"./lexicalAnalyzer.py", "r", encoding='utf-8') as myfile:
        tokens = myfile.read()+"\x1A" # EOF
        # tokens = r"self.range_nfa(['\'']) + self.kleene_positive(self.range_nfa(single_line_except)) + self.range_nfa(['\'']))"
        result = analyzer.analyze(tokens)
        '''for token in result:
            print(token)'''
