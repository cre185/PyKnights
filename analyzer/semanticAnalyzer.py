from utils import *
from symbolTable import *

class SemanticAnalyzer:
    def __init__(self, errorHandler):
        self.errorHandler = errorHandler

    def parse_S(self, node):
        children = self.parse_tree.children(node.identifier)
        for child in children:
            if child.tag == 'line':
                self.parse_line(child)
            elif child.tag == 'S':
                self.parse_S(child)

    def parse_line(self, node):
        children = self.parse_tree.children(node.identifier)
        i = 0
        # print(children)
        while i < len(children):
            child = children[i]
            if child.tag == 'from':
                symbolTable[children[i+1].tag].symbolType = SymbolType.package
                i += 3 # jump over the following import
            elif child.tag == 'import':
                i += 1
                symbolTable[children[i].tag].symbolType = SymbolType.package
            elif child.tag == 'class':
                classname = children[i+1].tag
                symbolTable[classname].symbolType = SymbolType.package
                while children[i].tag != 'line':
                    i += 1
                self.parse_line_in_class(children[i], classname)
                self.parse_align_end_in_class(children[i+1], classname)
            elif child.tag == 'def':
                symbolProp = SymbolProp(SymbolType.function)
                symbolProp.content['parameter'] = self.parse_identifier_list(children[i+3])
                symbolTable[children[i+1].tag] = symbolProp
                self.parse_line(children[i+7])
                i += 8
                self.parse_align_end(children[i])
            i += 1
    
    def parse_identifier_list(self, node):
        children = self.parse_tree.children(node.identifier)
        # print(children)

    def parse_line_in_class(self, node, classname):
        children = self.parse_tree.children(node.identifier)
        i = 0
        while i < len(children):
            child = children[i]
            if child.tag == 'def':
                del symbolTable[children[i+1].tag]
                symbolProp = SymbolProp(SymbolType.function)
                symbolProp.content['parameter'] = self.parse_identifier_list(children[i+3])
                symbolTable[classname].content[children[i+1].tag] = symbolProp
                self.parse_line_in_class(children[i+7], classname)
                i += 8
                self.parse_align_end_in_class(children[i], classname)
            i += 1

    def parse_align_end(self, node):
        children = self.parse_tree.children(node.identifier)
        for child in children:
            if child.tag == 'line':
                self.parse_line(child)
            elif child.tag == 'align_end':
                self.parse_align_end(child)

    def parse_align_end_in_class(self, node, classname):
        children = self.parse_tree.children(node.identifier)
        for child in children:
            if child.tag == 'line':
                self.parse_line_in_class(child, classname)
            elif child.tag == 'align_end':
                self.parse_align_end_in_class(child, classname)

    def analyze(self, parse_tree):
        self.parse_tree = parse_tree
        self.parse_S(parse_tree[parse_tree.root])

    