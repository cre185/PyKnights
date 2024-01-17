import copy
import json
from errorHandler import *
from lexicalAnalyzer import *
from syntaxAnalyzer import *
from semanticAnalyzer import *
from symbolTable import *
from colorTable import *
import argparse

errorHandler = ErrorHandler()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lexical Analyzer.')
    parser.add_argument('-f', '--file', help='Input file name')
    parser.add_argument('-d', '--dot', action='store_true', help='Output in dot file format')
    parser.add_argument('-t', '--text', help='Input directly in command line')
    parser.add_argument('-c', '--complete', help='Check the completion at designated position')
    args = parser.parse_args()

    LA = LexicalAnalyzer(errorHandler)
    SA = SyntaxAnalyzer(errorHandler)
    SE = SemanticAnalyzer(errorHandler)
    if args.text:
        script = args.text
    else:
        with open(r"./test.py" if not args.file else args.file, "r", encoding='utf-8') as myfile:
            script = myfile.read()
    try:
        source_script = copy.deepcopy(script)
        tokens = LA.analyze(source_script)
        errorHandler.handleError()
        errorHandler.clear()
        print('lexical analysis finished')
        parse_tokens = copy.deepcopy(tokens)
        parse_tree = SA.analyze(parse_tokens)
        errorHandler.handleError()
        errorHandler.clear()
        print('syntax analysis finished')
        if args.dot:
            parse_tree.to_graphviz('tree.dot')
        SE.analyze(parse_tree)
        print('semantic analysis finished')
    except:
        pass
    errorHandler.handleError()
    errorHandler.clear()
    colors = colorTable.getColor(tokens,symbolTable)
    with open('colors.pyknights', 'w') as f:
        f.write(json.dumps(colors))
    generate_HTML(script, colors)