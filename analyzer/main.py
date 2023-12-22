from errorHandler import *
from lexicalAnalyzer import *
from syntaxAnalyzer import *

import argparse

errorHandler = ErrorHandler()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lexical Analyzer.')
    parser.add_argument('-f', '--file', help='Input file name')
    args = parser.parse_args()

    analyzer = LexicalAnalyzer(errorHandler)
    with open(r"./test.py" if not args.file else args.file, "r", encoding='utf-8') as myfile:
        script = myfile.read()
        tokens = analyzer.analyze(script)
        errorHandler.handleError()
        errorHandler.clear()
        print('lexical analysis finished')