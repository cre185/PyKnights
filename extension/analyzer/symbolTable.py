from utils import SymbolType

class SymbolProp:
    def __init__(self, symbolType):
        self.symbolType = symbolType
        if symbolType == SymbolType.function:
            self.content = {'parameter': []}
            return
        self.content = {}

    def __str__(self):
        return str(self.symbolType)

symbolTable = {
    'print': SymbolProp(SymbolType.function),
    'len': SymbolProp(SymbolType.function),
    'range': SymbolProp(SymbolType.function),
    'input': SymbolProp(SymbolType.function),
    'append': SymbolProp(SymbolType.function),
    'remove': SymbolProp(SymbolType.function),
    'pop': SymbolProp(SymbolType.function),
    'insert': SymbolProp(SymbolType.function),
    'reverse': SymbolProp(SymbolType.function),
    'sort': SymbolProp(SymbolType.function),
    'abs': SymbolProp(SymbolType.function),
    'max': SymbolProp(SymbolType.function),
    'min': SymbolProp(SymbolType.function),
    'sum': SymbolProp(SymbolType.function),
    'any': SymbolProp(SymbolType.function),
    'all': SymbolProp(SymbolType.function),
    'open': SymbolProp(SymbolType.function),
    'close': SymbolProp(SymbolType.function),
    'read': SymbolProp(SymbolType.function),
    'write': SymbolProp(SymbolType.function),
    'readline': SymbolProp(SymbolType.function),
    'readlines': SymbolProp(SymbolType.function),
    'seek': SymbolProp(SymbolType.function),
    'int': SymbolProp(SymbolType.package),
    'str': SymbolProp(SymbolType.package),
    'list': SymbolProp(SymbolType.package),
}