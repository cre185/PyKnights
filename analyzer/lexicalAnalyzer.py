import keyword
from automata.fa.nfa import NFA
from enum import Enum
from errorHandler import *

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
    def __init__(self, errorHandler):
        self.reservedWords = keyword.kwlist
        self.errorHandler = errorHandler
        # Initialize some useful variables
        self.all_char = ['\0'] + [chr(i) for i in range(32, 128)] + [chr(10), chr(13), chr(9)] # definition for characters that can be accepted
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

    # @time_count
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
        self.nfa.append(self.range_nfa(['(', ')', '[', ']', '{', '}', ',', ':', ';', '\\']))
        # Strings
        def except_trans_nfa(uni_list):
            transition = {'s':{c:{'nf'} for c in uni_list}, 'nf':{}, 't':{c:{'tf'} for c in self.all_char}, 'tf':{}}
            transition['s']['\\'] = {'t'}
            return NFA(
                states={'s', 'nf', 't', 'tf'},
                input_symbols={ch for ch in self.all_char},
                transitions=transition,
                initial_state='s',
                final_states={'nf', 'tf'}
            )

        single_line_except = [i for i in self.all_char if i not in "\\\'\n"]
        double_line_except = [i for i in self.all_char if i not in "\\\"\n"]
        single_paragraph_except = [i for i in self.all_char if i not in "\\"]
        double_paragraph_except = [i for i in self.all_char if i not in "\\"]
        self.nfa.append(self.range_nfa(['\'']) + self.kleene_positive(except_trans_nfa(single_line_except)) + self.range_nfa(['\'']))
        self.nfa.append(self.range_str_nfa(["\'\'"]) + self.range_nfa([i for i in self.all_char if i != '\'']))
        self.nfa.append(self.range_str_nfa(["\'\'\'"]) + except_trans_nfa(single_paragraph_except).kleene_star() + self.range_str_nfa(["\'\'\'"]))

        self.nfa.append(self.range_nfa(['\"']) + self.kleene_positive(except_trans_nfa(double_line_except)) + self.range_nfa(['\"']))
        self.nfa.append(self.range_str_nfa(["\"\""]) + self.range_nfa([i for i in self.all_char if i != '\"']))
        self.nfa.append(self.range_str_nfa(["\"\"\""]) + except_trans_nfa(double_paragraph_except).kleene_star() + self.range_str_nfa(["\"\"\""]))
        # Spaces
        space_except = [i for i in self.all_char if i not in " \t\n"]
        self.nfa.append(self.kleene_positive(self.range_nfa([' ', '\t', '\n']))+self.range_nfa(space_except))
        # Comments
        self.nfa.append(self.range_nfa(['#']) + self.range_nfa([i for i in self.all_char if i not in ['\n']]).kleene_star() + self.range_nfa(['\n', '\0']))


    @time_count
    def analyze(self, tokens) -> list[Token]:
        result = self.analyze_tokens(tokens+'\0')
        return result[:-1] if len(result) > 0 and result[-1].tokenType == TokenType.error else result

    def analyze_tokens(self, tokens) -> list[Token]:
        # Initialize states used for emulating the NFA
        self.states = [nfa._get_lambda_closures()[nfa.initial_state] for nfa in self.nfa]
        # Analyze the tokens and return a Tokenline
        token_list = []
        i,j=0,0
        while i < len(tokens):
            flag = False
            for k,nfa in enumerate(self.nfa):
                self.states[k] = nfa._get_next_current_states(self.states[k], tokens[i])
                if len(self.states[k]) != 0:
                    flag = True
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
            if not flag:
                break
            i+=1
        if j < len(tokens) and not tokens[j:]=='\0':
            self.errorHandler.addError(ErrorType.lexicalError, "Unrecognized token at: "+tokens[j:] if len(tokens[j:]) < 30 else tokens[j:j+30]+"...")
            token_list.append(Token(tokens[j], TokenType.error))
            token_list += self.analyze_tokens(tokens[j+1:])
        return token_list
