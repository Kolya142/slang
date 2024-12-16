from lexer import lexer
from preparser import genast, token_to_str
from typed import *

cc = \
"""
#include <stdio.h>
int main() {
"""
context = 0    # 0 - base, 1 - wait (;), 2 - wait ())


def translater(cmd: Command):
    global context, cc
    print(cmd.args[0])
    if context == 1:
        if cmd.type_ == CommandType.WORD and cmd.args[0].value == ";":
            context = 0
        return
    if context == 2:
        if cmd.type_ == CommandType.WORD and cmd.args[0].value == ")":
            context = 0
        return
    if cmd.type_ == CommandType.SET:
        cc += slang_types[cmd.args[0].value] + ' '
        for arg in cmd.args[1:]:
            cc += token_to_str(arg)
        cc += ';\n'
    if cmd.type_ == CommandType.WORD:
        match cmd.args[0].value:
            case 'break':
                cc += 'break'
            case ';':
                cc += ';\n'
    if cmd.type_ == CommandType.FUNCTION_EXEC:
        match cmd.args[0].value:
            case 'end':
                cc += f'exit({cmd.args[2].args[0].value})'
            case 'inc':
                cc += f'{cmd.args[2].args[0].value}++'
            case 'print':
                cc += 'printf('
                s = False
                for a in cmd.args[1:]:
                    if a.args[0].value == '(' and a.type_ == CommandType.WORD:
                        s = True
                        continue
                    if a.args[0].value == ')' and a.type_ == CommandType.WORD:
                        break
                    if not s:
                        continue
                    cc += token_to_str(a.args[0])
                cc += ')'
    if cmd.type_ == CommandType.STATEMENT:
        i = 0
        while True:
            if type(cmd.args[i]) == Command:
                break
            i += 1
        e = [i.value for i in cmd.args[:i]]
        if e[0] == 'loop':
            cc += 'for (;;) {\n'
        if e[0] == 'if':
            cc += 'if ('
            for l in e[1:]:
                cc += f'{l}'
            cc += ') {\n'
        c = cmd.args[i:]
        for cmd in c:
            translater(cmd)
        cc += '}\n'


if __name__ == '__main__':
    tokens = lexer(open("main.sl").read())
    ast = genast(tokens)
    for cmd in ast:
        translater(cmd)
    cc += '}'
    print(cc)
    with open("main.c", 'w') as f:
        f.write(cc)