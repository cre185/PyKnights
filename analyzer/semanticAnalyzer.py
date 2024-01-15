from utils import *
from symbolTable import *

class SemanticAnalyzer:
    def __init__(self, errorHandler):
        self.errorHandler = errorHandler

    def parse_S(self, node):
        children = self.parse_tree.children(node.tag)
        for child in children:
            if child.tag == 'line':
                self.parse_line(child)
            elif child.tag == 'S':
                self.parse_S(child)

    def parse_line(self, node):
        children = self.parse_tree.children(node.tag)
        for child in children:
            if child.tag == 'assign':
                self.parse_assign(child)
            elif child.tag == 'print':
                self.parse_print(child)
            elif child.tag == 'if':
                self.parse_if(child)
            elif child.tag == 'while':
                self.parse_while(child)

    def analyze(self, parse_tree):
        self.parse_tree = parse_tree
        self.parse_S(parse_tree.root)
