from utils import *

getColorbyType = {
    "TokenType.reserved": 0,
    "TokenType.constant": 1,
    "TokenType.operator": 2,
    "TokenType.separator": 3,
    "TokenType.string": 4,
    "TokenType.space": 5,
    "TokenType.comment": 6,
    "TokenType.error": 7,
    "TokenType.assigner": 8,
    "SymbolType.variable": 9,
    "SymbolType.function": 10,
    "SymbolType.package": 11
}
    
class colorTable:
    def getColor(tokens,symbolTable):
        line = 1
        row = 1
        theTokens = []
        for token in tokens:
            theToken = {}
            if token.tokenType != TokenType.identifier:
                type = token.tokenType
            else:
                type = symbolTable[token.token]
            theToken["token"] = token.token
            type = str(type)
            theToken["type"] = getColorbyType[type]
            theToken["startLine"] = line
            theToken["startRow"] = row
            if token.tokenType == TokenType.space or token.tokenType == TokenType.string:
                tokenLenth = 0
                for char in token.token:
                    tokenLenth += 1
                    if tokenLenth == len(token.token):
                        theToken["endLine"] = line
                        theToken["endRow"] = row
                    if char == '\n':
                        line += 1
                        row = 1
                    else:
                        row += 1
            else:
                row += len(token.token)
                theToken["endLine"] = line
                theToken["endRow"] = row - 1
            theTokens.append(theToken)
        return theTokens
from utils import *

getColorbyType = {
    "TokenType.reserved": 0,
    "TokenType.constant": 1,
    "TokenType.operator": 2,
    "TokenType.separator": 3,
    "TokenType.string": 4,
    "TokenType.space": 5,
    "TokenType.comment": 6,
    "TokenType.error": 7,
    "TokenType.assigner": 8,
    "SymbolType.variable": 9,
    "SymbolType.function": 10,
    "SymbolType.package": 11
}
    
class colorTable:
    def getColor(tokens,symbolTable):
        line = 1
        column = 1
        theTokens = []
        for token in tokens:
            theToken = {}
            if token.tokenType != TokenType.identifier:
                type = token.tokenType
            else:
                type = symbolTable[token.token]
            theToken["token"] = token.token
            type = str(type)
            theToken["type"] = getColorbyType[type]
            theToken["startLine"] = line
            theToken["startColumn"] = column
            if token.tokenType == TokenType.space or token.tokenType == TokenType.string:
                tokenLenth = 0
                for char in token.token:
                    tokenLenth += 1
                    if tokenLenth == len(token.token):
                        theToken["endLine"] = line
                        theToken["endColumn"] = column
                    if char == '\n':
                        line += 1
                        column = 1
                    else:
                        column += 1
            else:
                column += len(token.token)
                theToken["endLine"] = line
                theToken["endColumn"] = column - 1
            theTokens.append(theToken)
        return theTokens
