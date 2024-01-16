class SymbolProp:
    def __init__(self, symbolType):
        self.symbolType = symbolType
        self.content = {}

    def __str__(self):
        return str(self.symbolType)

symbolTable = {}