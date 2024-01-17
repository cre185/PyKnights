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
    completionTable = []
    completion = {}
    for key, value in symbolTable.items():
        if value.symbolType == SymbolType.function:
            completion['name'] = key
            completion['type'] = 'Function'
            parameter_str = 'parameter: '
            for item in value.content['parameter']:
                parameter_str += item + ', '
            parameter_str = parameter_str[:-2]
            if parameter_str == 'parameter':
                parameter_str = 'parameter: None'
            completion['detail'] = parameter_str
            completionTable.append(completion)
            completion = {}
        elif value.symbolType == SymbolType.variable:
            completion['name'] = key
            completion['type'] = 'Variable'
            completionTable.append(completion)
            completion = {}
        elif value.symbolType == SymbolType.package:
            completion['name'] = key
            completion['type'] = 'Class'
            detail_str = 'content: '
            for key in value.content:
                detail_str += key + ', '
            detail_str = detail_str[:-2]
            if detail_str == 'content':
                detail_str = 'content: None'
            completion['detail'] = detail_str
            detail_list = []
            completionTable.append(completion)
            completion = {}
    with open('completions.pyknights', 'w') as f:
        f.write(json.dumps(completionTable))
    # generate_HTML(script, colors)
