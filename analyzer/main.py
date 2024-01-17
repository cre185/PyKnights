from enum import Enum
import time

def time_count(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print("Time spent in "+func.__name__+": ", time.time()-start_time)
        return result
    return wrapper


class TokenType(Enum):
    # Enumerate the token types
    reserved = 0
    identifier = 1
    constant = 2
    operator = 3
    separator = 4
    string = 5
    space = 6
    comment = 7
    error = 8
    assigner = 9

class Token:
    def __init__(self, token, tokenType):
        self.token = token
        self.tokenType = tokenType

    def __str__(self):
        return "Token: "+str(self.token)+" - Type: "+str(self.tokenType)
    
'''
Signals are used in transition list
S: start signal, representing the whole program, can be split into rows
row: representing a row, have a bunch of complex possible representations
readable: representing a readable, it must at least provide a value that can be assigned to a mutable
readable_list: representing a list of readables
readable_list_part: representing a part of a list consisting of readables
identifier_list: representing a list of identifiers
identifier_list_part: representing a part of a list consisting of identifiers
align_end: treating the possible end of an indent block, so it can be aligned with the start of the block
after_identifier: representing what a row can appear after accepting an identifier
readable_after_identifier: representing what a readable can appear after accepting an identifier
inherit: representing the inheritance of a class
import_goods: representing things that can be imported
'''
class Signal(Enum):
    S = 0
    row = 1
    readable = 2
    readable_list = 3
    readable_list_part = 4
    identifier_list = 5
    identifier_list_part = 6
    align_end = 7
    after_identifier = 8
    readable_after_identifier = 9
    inherit = 10
    import_goods = 11
    ret_instruct = 12
    array_range = 13
    all_num = 14
    before_slice = 15
    after_slice = 16
    

class ErrorType(Enum):
    # Enumerate the error types
    lexicalError = 0
    syntaxError = 1
    semanticError = 2
    warning = 3


class SymbolType(Enum):
    variable = 0
    function = 1
    package = 2 # This actually represents package or class name
    globe = 3

def generate_HTML(text, colors):
    code = ""
    color_iter = iter(colors)
    color = next(color_iter, None)

    rows = text.split("\n")

    for color in colors:
        start_row, start_row = color["startRow"] - 1, color["startRow"] - 1
        end_row, end_row = color["endRow"] - 1, color["endRow"]

        # 获取颜色块对应的文本
        if start_row == end_row:
            colored_text = rows[start_row][start_row:end_row]
            if colored_text == "":
                colored_text = "\n"
        elif start_row + 1 == end_row:
            colored_text = rows[start_row][start_row:] + "\n" + rows[end_row][:end_row]
        else:
            colored_text = rows[start_row][start_row:] + "\n" + "\n".join(rows[start_row+1:end_row]) + "\n" + rows[end_row][:end_row]

        # 将文本包裹在相应的 CSS 类中
        code += f'<span class="color{color["type"]}">{colored_text}</span>'

    # 填充 HTML 模板
    html = """<html>
<head>
    <style>
    body { background-color: #808080; }
    .color0 { color: #DA70D6; }
    .color1 { color: #00fa9a; }
    .color2 { color: black; }
    .color3 { color: #F0E68C; }
    .color4 { color: orange; }
    .color5 { color: white; }
    .color6 { color: #228B22; }
    .color7 { color: red; }
    .color8 { color: black; }
    .color9 { color: #00BFFF; }
    .color10 { color: yellow; }
    .color11 { color: #00FF00; }
    </style>
</head>
<body>
    <pre>
"""+code+"""
    </pre>
</body>
</html>
"""
    # 写入 HTML 文件
    with open("highlighted.html", "w") as f:
        f.write(html)