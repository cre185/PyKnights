from errorHandler import *
from lexicalAnalyzer import *
from syntaxAnalyzer import *

import argparse

errorHandler = ErrorHandler()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lexical Analyzer.')
    parser.add_argument('-f', '--file', help='Input file name')
    args = parser.parse_args()

    LA = LexicalAnalyzer(errorHandler)
    SA = SyntaxAnalyzer(errorHandler)
    with open(r"./test.py" if not args.file else args.file, "r", encoding='utf-8') as myfile:
        script = myfile.read()
        tokens = LA.analyze(script)
        errorHandler.handleError()
        errorHandler.clear()
        print('lexical analysis finished')
        parse_tree = SA.analyze(tokens)
        errorHandler.handleError()
        errorHandler.clear()
        print('syntax analysis finished')
        with open('tree.json', 'w') as outfile:
            result = parse_tree.to_json()
            outfile.write(result)