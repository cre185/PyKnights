import random
from utils import time_count
from main import *
a = [1,2,3]
b = a[:-1]
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