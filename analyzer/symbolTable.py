from utils import SymbolType

class SymbolProp:
    def __init__(self, symbolType):
        self.symbolType = symbolType
        self.content = {}

    def __str__(self):
        return str(self.symbolType)

symbolTable = {
    'print': SymbolProp(SymbolType.function),
    'len': SymbolProp(SymbolType.function),
    'range': SymbolProp(SymbolType.function),
    'input': SymbolProp(SymbolType.function),
    'list': SymbolProp(SymbolType.package),
}