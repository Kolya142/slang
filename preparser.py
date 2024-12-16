from lexer import lexer
from typed import *
import json

def parser(tokens: Tokens) -> List[Tuple[int, Command]]:
    commands: List[Tuple[int, Command]] = []
    context = [-1] # -1 - basic, 0 - function def, 1 - variable def, 2 - statement, 3 - function exec, 4 - statement define, 5 - function def define
    for i, token in enumerate(tokens):
        # if commands:
        #     print(context, commands[-1][1].type_, '->', ', '.join(i.value for i in commands[-1][1].args))
        # else:
        #     print(context)
        if len(context) == 0:
            context.append(-1)

        if context[-1] == 3:
            if token.value == ')':
                commands.append((len(context), Command(CommandType.WORD, [token])))
                context.pop()
                continue

        if context[-1] == 5:
            if token.value == "{":
                context.pop()
                context.append(0)
                continue
            commands[-1][1].args.append(token)
            continue

        if context[-1] == 4:
            if token.value == "{":
                context.pop()
                context.append(2)
                continue
            commands[-1][1].args.append(token)
            continue

        if context[-1] == 1:
            if token.value == ';':
                context.pop()
                continue
            commands[-1][1].args.append(token)
            continue
        if token.value in slang_types:
            # check is function define or variable define
            # something like tokens[i+2] == '='
            # and function call in another function
            j = i
            while j+1 < len(tokens) and tokens[j+1].value == '*':
                j += 1
            if j+2 < len(tokens) and tokens[j+2].value == '=':
                # a variable
                commands.append((len(context), Command(CommandType.SET, [token])))
                context.append(1)
                continue
            else:
                # a function
                if context[-1] != -1:
                    raise SyntaxError(f"idk how to name this error, so just go to line {token.line}")
                commands.append((len(context), Command(CommandType.FUNCTION_DEF, [token])))
                context.append(5)
            continue
        if (token.value == '}' and len(context) != 0 and context[-1] in [2, 0]) or (token.value == ')' and context[-1] == 3):
            context.pop()
            continue
        if token.value in statements:
            commands.append((len(context), Command(CommandType.STATEMENT, [token])))
            context.append(4)
            continue
        if token.type_ == TokenType.WORD and i < len(tokens) - 1 and tokens[i+1].value == '(':
            commands.append((len(context), Command(CommandType.FUNCTION_EXEC, [token])))
            context.append(3)
            continue
        commands.append((len(context), Command(CommandType.WORD, [token])))


    return commands

def token_to_str(token: Token) -> str:
    if token.type_ == TokenType.LITERAL:
        return f'"{token.value}"'
    else:
        return f'{token.value}'

def print_command(command: Command, tabulation: int = 0):
    a = []
    for arg in command.args:
        if type(arg) == Command:
            a.append('\n' + '    '*(1+tabulation) + print_command(arg, tabulation+1))
        else:
            if arg.type_ == TokenType.LITERAL:
                a.append(f'"{arg.value}"')
            else:
                a.append(f'{arg.value}')
    if command.type_ == CommandType.STATEMENT:
        return f"->{' '.join(a)}"
    return f"->{command.type_.name}({' '.join(a)})"

def cmd2dict(command: Command) -> dict:
    o = {}
    o["type"] = command.type_.name
    o["args"] = []
    for a in command.args:
        if type(a) == Command:
            o['args'].append(cmd2dict(a))
        elif type(a) == Token:
            o['args'].append(a.value)
        else:
            o['args'].append(f'{a}')
    return o

class ASTBuilder:  # ast builder by chatgpt
    def __init__(self):
        self.stack = [(0, Command(CommandType.STATEMENT, ["main"]))]

    def push(self, level: int, command: Command):
        while self.stack and self.stack[-1][0] >= level:
            self.stack.pop()
        self.stack[-1][1].args.append(command)
        self.stack.append((level, command))

    def current_command(self) -> Command:
        return self.stack[-1][1]

    def get_root_commands(self) -> List[Command]:
        return self.stack[0][1].args[1:]

def genast(tokens: Tokens) -> List[Command]:
    builder = ASTBuilder()
    commands = parser([Token("token", 0, TokenType.WORD)] + tokens)
    for cd, cc in commands:
        builder.push(cd, cc)
    return builder.get_root_commands()

if __name__ == '__main__':
    tokens = lexer(open("main.sl").read())
    commands = genast(tokens)
    jsonable = []
    for cmd in commands:
        jsonable.append(cmd2dict(cmd))
    with open("ast.json", 'w') as f:
        json.dump(jsonable, f, indent=4)
    print(commands, '\n\n\n\n')
    for command in commands:
        print(print_command(command))