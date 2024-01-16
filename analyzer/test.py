import random
from utils import time_count
from main import *

class MyDFA:
    def __init__(self, properties):
        self.tag = 'MyDFA'
        self.notice = 'This is a test'
        def hehe(self):
            def hoho(self):
                print('hoho')
            return self.tag

    class MyInnerDFA:
        def haha(self, properties):
            self.tag = 'MyInnerDFA'
            self.notice = 'This is a test'

    def just_a_test(self) -> str:
        print('This is just a test')
        print('If you don\'t trust me, see: ' + self.notice)
        return self.tag

def an_outer_test():
    print('This is an outer test')

an_outer_test()

aDFA = MyDFA('This is a DFA')
aDFA.just_a_test()
string_list = ['a', 'b', 'deaf\'s asdaw', '''
    This is a test''']
number_list = [1, 114514, 234.567, -18.290, 0003.40, 1., 0xAa0, 1+8.3j, 9.6e4, 8.e6]

a = [1,2,3]
b = a[1:-1]
c = a[1:]
d = a[:-1]

lives = 3

words = ['pizza', 'fairy', 'teeth', 'shirt', 'otter', 'plane']
secret_word = random.choice(words)
# print(secret_word)

clue = list('?????')
heart_symbol = '\u2764'

guessed_word_correctly = False

def update_clue(guessed_letter, secret_word, clue):
    index = 0
    while index < len(secret_word):
        if guessed_letter == secret_word[index]:
            clue[index] = guessed_letter
        index = index + 1

while lives > 0:
    print(clue)
    print('lives remain: ' + heart_symbol * lives)
    guess = input('guess a letter or the whole word: ')

    if guess == secret_word:
        guessed_word_correctly = True
        break

    if guess in secret_word:
        update_clue(guess, secret_word, clue)
    else:
        print('Error!\n')
        lives = lives - 1

def analyze_tokens(self, tokens) -> list[Token]:
    # Analyze the tokens and return a Tokenline
    token_list = []
    while i < len(tokens):
        flag = False
        for k in len(self.nfa):
            nfa = self.nfa[k]
            self.states[k] = nfa._get_next_current_states(self.states[k], tokens[i])
            if len(self.states[k]) != 0:
                flag = True
            if not self.states[k].isdisjoint(nfa.final_states):
                # Need to leave last character out if it's: reserved words, identifiers, constants, spaces, comments
                if k in [0,1,2,3,4,5,6,7,8,9,13,16,18,19]:
                    i-=1
                # Generate token
                token = tokens[j:i+1]
                if k == 0:
                    token_list.append(Token(token, TokenType(0)))
                elif k == 1:
                    if not token in symbolTable:
                        symbolTable[token] = SymbolProp(SymbolType.variable)
                    token_list.append(Token(token, TokenType(1)))
                elif k in [2, 3, 4, 5, 6, 7]:
                    token_list.append(Token(token, TokenType(2)))
                elif k in [8, 9, 10]:
                    if token[-1]=='=' and token!='==': # Then it's an assigner
                        token_list.append(Token(token, TokenType(9)))
                    else:
                        token_list.append(Token(token, TokenType(3)))
                elif k == 11:
                    token_list.append(Token(token, TokenType(4)))
                elif k in [12, 13, 14, 15, 16, 17]:
                    token_list.append(Token(token, TokenType(5)))
                elif k == 18:
                    token_list.append(Token(token, TokenType(6)))
                elif k == 19:
                    token_list.append(Token(token, TokenType(7)))
                # Reset states
                j=i+1
                break
        if not flag:
            break
        i+=1
    if j < len(tokens) and not tokens[j:]=='\0':
        token_list.append(Token(tokens[j], TokenType.error))
        token_list += self.analyze_tokens(tokens[j+1:])
    return token_list
