import keyword # for reserved words
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

class Token:
    def __init__(self, token, tokenType):
        self.token = token
        self.tokenType = tokenType

    def __str__(self):
        return "Token: "+self.token+" - Type: "+str(self.tokenType)
    

class TokenLine:
    def __init__(self, token_list, valid):
        self.token_list = token_list
        self.valid = valid

    def __str__(self):
        return str(self.token_list)
    

class LexicalAnalyzer:
    def __init__(self):
        self.reservedWords = keyword.kwlist
        self.all_char = [chr(i) for i in range(0, 128)] # definition for characters that can be accepted
        self.init_nfa()

    def range_nfa(self, str_list):
        # Generate an NFA for a range of characters
        result_nfa = None
        for strng in str_list:
            transition = {}
            for i,c in enumerate(strng):
                transition['q'+str(i)] = {str(c):{'q'+str(i+1)}}
            transition['q'+str(len(strng))] = {}
            nfa = NFA(
                states={'q'+str(i) for i in range(len(strng)+1)},
                input_symbols={ch for ch in self.all_char},
                transitions=transition,
                initial_state='q0',
                final_states={'q'+str(len(strng))}
            )
            if result_nfa is None:
                result_nfa = nfa
            else:
                result_nfa = result_nfa.union(nfa)
        return result_nfa

    def init_nfa(self):
        # Initialize the NFA used for the lexical analyzer
        self.nfa = []
        # Reserved words
        azAZ_ = [chr(i) for i in range(ord('a'), ord('z')+1)] + [chr(i) for i in range(ord('A'), ord('Z')+1)] + ['_']
        azAZ09_ = azAZ_ + [chr(i) for i in range(ord('0'), ord('9')+1)]
        all_except = [i for i in self.all_char if i not in azAZ09_]
        self.nfa.append(NFA.from_regex('|'.join(self.reservedWords))+self.range_nfa(all_except))
        # Identifiers
        self.nfa.append(self.range_nfa(azAZ_) + self.range_nfa(azAZ09_).kleene_star()+self.range_nfa(all_except))
        # Constants
        num = self.range_nfa([chr(i) for i in range(ord('0'), ord('9')+1)])
        num_except = self.range_nfa([i for i in self.all_char if i not in num])
        self.nfa.append(num + num.kleene_star() + num_except)
        # Operators
        self.nfa.append(self.range_nfa(['+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|', '^', '~', '.'])) # incorrect! can't treat ==
        # Separators
        self.nfa.append(self.range_nfa(['(', ')', '[', ']', '{', '}', ',', ':', ';']))
        # Strings
        self.nfa.append(self.range_nfa(['\'', '\"']) + self.range_nfa(all_except) + self.range_nfa(['\'', '\"'])) # incorrect!
        # Spaces
        self.nfa.append(self.range_nfa([' ', '\t', '\n']))
        # Comments
        self.nfa.append(self.range_nfa(['#']) + self.range_nfa([chr(i) for i in range(0, 128) if chr(i) != '\n']).kleene_star() + self.range_nfa(['\n']))

    def analyze_line(self, tokens) -> TokenLine:
        # Analyze the tokens and return a Tokenline
        token_list = []
        i,j=1,0
        while i < len(tokens)+1:
            token = tokens[j:i]
            for k,nfa in enumerate(self.nfa):
                if nfa.accepts_input(token):
                    # Need to leave last character out if it's: reserved words, identifiers, constants, comments
                    if k in [0,1,2,7]:
                        i-=1
                        token = token[:-1]
                    # Generate token
                    token_list.append(Token(token, TokenType(k)))
                    j=i
                    break
            i+=1
        if j < len(tokens):
            print("Warning: Unrecognized token from: ", tokens[j:] if len(tokens[j:]) < 30 else tokens[j:j+30] + "...")
            return TokenLine(token_list, False)
        # remove spaces for testing
        # token_list = [token for token in token_list if not (token.tokenType == TokenType.space and token.token == " ")]
        return TokenLine(token_list, True)
    
    def analyze(self, tokens) -> list[TokenLine]:
        tokenline_list = []
        lines = tokens.split("\n")
        for line in lines:
            tokenline_list.append(self.analyze_line(line+'\n'))
        return tokenline_list


if __name__ == "__main__":
    analyzer = LexicalAnalyzer()
    '''with open("./test.py", "r", encoding='utf-8') as myfile:
        tokens = myfile.read()
        print(analyzer.analyze(tokens))'''
    source = """def update_clue(guessed_letter, secret_word, clue):
    index = 0
    # print(secret_word)
    while index < len(secret_word):
        if guessed_letter == secret_word[index]:
            clue[index] = guessed_letter
        index = index + 1 """
    result = analyzer.analyze(source)
    print(result)
