from typed import *

def lexer(code: str) -> Tokens:
    tokens: Tokens = []
    context = 0  # 0-free 1-num 2-word 3-literal
    line = 0
    for i in range(len(code)):
        c = code[i]
        cb = ord(c)
        if context == 3 and c != '"':
            tokens[-1].value += c
            continue
        if c == '\n':
            line += 1
            continue
        if ord('0') <= cb <= ord('9'):
            if context == 0:
                context = 1
                tokens.append(Token(c, line, TokenType.NUMERIC))
                continue
            if context == 1 or context == 2:
                tokens[-1].value += c
                continue
            continue
        else:
            if context == 1:
                context = 0
        if c == ' ':
            if context != 0:
                context = 0
            continue
        if c in "=+-*/(){};,":
            if c == '=' and len(tokens) != 0 and tokens[-1].value in '<>=!+-*/':
                tokens[-1].value += c
                continue
            if context != 0:
                context = 0
            tokens.append(Token(c, line, TokenType.SYMBOL))
            continue
        if ord('a') <= cb <= ord('z') or ord('A') <= cb <= ord('Z') or c == '_':
            if context == 1:
                context = 0
            if context == 0:
                context = 2
                tokens.append(Token(c, line, TokenType.WORD))
                continue
            tokens[-1].value += c
            continue
        if c == '"':
            if i == 0 or code[i-1] != '\\':
                if context == 0:
                    context = 3
                    tokens.append(Token("", line, TokenType.LITERAL))
                elif context == 3:
                    context = 0
            else:
                tokens[-1].value += '"'
            continue
        if c == '\\' and context == 3:
            tokens[-1].value += '\\'
            continue
        if context == 1:
            context = 0
            continue
        if len(tokens) != 0:
            tokens[-1].value += c
                
    return tokens


if __name__ == '__main__':
    tokens = lexer(open("main.sl").read())
    for token in tokens:
        print(f'"{token.value}": {token.type_.name} at {token.line}')