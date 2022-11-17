import re

import Enum_classes


def get_next_token():  # read from file
    file = open('input.txt', 'r')
    number = ""
    identifier = ""
    symbol = ""

    number_pattern = re.compile("^[0-9]$")
    identifier_pattern1 = re.compile("^[A-Za-z]$")
    identifier_pattern2 = re.compile("^[A-Za-z0-9]$")
    symbol_pattern = re.compile("^[;:,+\-*<=/]$")  # ==
    whitespace_pattern = re.compile("^[ \n\r\t\v\f]$")

    while 1:
        # read by character
        char = file.read(1)
        # match number
        if re.match(number_pattern, char):
            number = number + char
            while 1:
                num_char = file.read(1)
                if re.match(number_pattern, num_char):
                    number = number + num_char
                else:
                    file.seek(-1, 1)  # move file pointer 1 char behind current position
                    return Enum_classes.Token.Number, number
        # match identifier
        elif re.match(identifier_pattern1, char):
            identifier = identifier + char
            while 1:
                identifier_char = file.read(1)
                if re.match(identifier_pattern2, identifier_char):
                    identifier = identifier + identifier_char
                else:
                    file.seek(-1, 1)  # move file pointer 1 char behind current position
                    if identifier == "if":
                        return Enum_classes.Token.Keyword, "if"
                    elif identifier == "else":
                        return Enum_classes.Token.Keyword, "else"
                    elif identifier == "void":
                        return Enum_classes.Token.Keyword, "void"
                    elif identifier == "int":
                        return Enum_classes.Token.Keyword, "int"
                    elif identifier == "while":
                        return Enum_classes.Token.Keyword, "while"
                    elif identifier == "break":
                        return Enum_classes.Token.Keyword, "break"
                    elif identifier == "switch":
                        return Enum_classes.Token.Keyword, "switch"
                    elif identifier == "default":
                        return Enum_classes.Token.Keyword, "default"
                    elif identifier == "case":
                        return Enum_classes.Token.Keyword, "case"
                    elif identifier == "return":
                        return Enum_classes.Token.Keyword, "return"
                    elif identifier == "endif":
                        return Enum_classes.Token.Keyword, "endif"

                    return Enum_classes.Token.Identifier, identifier
        # match keywords
        elif char == "i":
            next_char = file.read(1)
            if next_char == "f":
                return Enum_classes.Token.Keyword, "if"

            elif next_char == "n":
                next_char2 = file.read(1)
                if next_char2 == "t":
                    return Enum_classes.Token.Keyword, "int"
                else:
                    error_handling()
            else:
                error_handling()
        elif char == "e":
            next_char = file.read(1)
            if next_char == "l":
                next_char2 = file.read(1)
                if next_char2 == "s":
                    next_char3 = file.read(1)
                    if next_char3 == "e":
                        return Enum_classes.Token.Keyword, "else"
                    else:
                        error_handling()
                else:
                    error_handling()
            elif next_char == "n":
                next_char2 = file.read(1)
                if next_char2 == "d":
                    next_char3 = file.read(1)
                    if next_char3 == "i":
                        next_char4 = file.read(1)
                        if next_char4 == "f":
                            return Enum_classes.Token.Keyword, "endif"
                        else:
                            error_handling()
                    else:
                        error_handling()
                else:
                    error_handling()
            else:
                error_handling()

        elif char == "v":
            next_char = file.read(1)
            if next_char == "o":
                next_char2 = file.read(1)
                if next_char2 == "i":
                    next_char3 = file.read(1)
                    if next_char3 == "d":
                        return Enum_classes.Token.Keyword, "void"
                    else:
                        error_handling()
                else:
                    error_handling()
            else:
                error_handling()

        elif char == "w":
            next_char = file.read(1)
            if next_char == "h":
                next_char2 = file.read(1)
                if next_char2 == "i":
                    next_char3 = file.read(1)
                    if next_char3 == "l":
                        next_char4 = file.read(1)
                        if next_char4 == "e":
                            return Enum_classes.Token.Keyword, "while"
                        else:
                            error_handling()
                    else:
                        error_handling()
                else:
                    error_handling()
            else:
                error_handling()

        elif char == "b":
            next_char = file.read(1)
            if next_char == "r":
                next_char2 = file.read(1)
                if next_char2 == "e":
                    next_char3 = file.read(1)
                    if next_char3 == "a":
                        next_char4 = file.read(1)
                        if next_char4 == "k":
                            return Enum_classes.Token.Keyword, "break"
                        else:
                            error_handling()
                    else:
                        error_handling()
                else:
                    error_handling()
            else:
                error_handling()

        elif char == "s":
            next_char = file.read(1)
            if next_char == "w":
                next_char2 = file.read(1)
                if next_char2 == "i":
                    next_char3 = file.read(1)
                    if next_char3 == "t":
                        next_char4 = file.read(1)
                        if next_char4 == "c":
                            next_char5 = file.read(1)
                            if next_char5 == "h":
                                return Enum_classes.Token.Keyword, "switch"
                            else:
                                error_handling()
                        else:
                            error_handling()
                    else:
                        error_handling()
                else:
                    error_handling()
            else:
                error_handling()

        elif char == "d":
            next_char = file.read(1)
            if next_char == "e":
                next_char2 = file.read(1)
                if next_char2 == "f":
                    next_char3 = file.read(1)
                    if next_char3 == "a":
                        next_char4 = file.read(1)
                        if next_char4 == "u":
                            next_char5 = file.read(1)
                            if next_char5 == "l":
                                next_char6 = file.read(1)
                                if next_char6 == "t":
                                    return Enum_classes.Token.Keyword, "default"
                                else:
                                    error_handling()
                            else:
                                error_handling()
                        else:
                            error_handling()
                    else:
                        error_handling()
                else:
                    error_handling()
            else:
                error_handling()

        elif char == "c":
            next_char = file.read(1)
            if next_char == "a":
                next_char2 = file.read(1)
                if next_char2 == "s":
                    next_char3 = file.read(1)
                    if next_char3 == "e":
                        return Enum_classes.Token.Keyword, "case"
                    else:
                        error_handling()
                else:
                    error_handling()
            else:
                error_handling()
        elif char == "r":
            next_char = file.read(1)
            if next_char == "e":
                next_char2 = file.read(1)
                if next_char2 == "t":
                    next_char3 = file.read(1)
                    if next_char3 == "u":
                        next_char4 = file.read(1)
                        if next_char4 == "r":
                            next_char5 = file.read(1)
                            if next_char5 == "n":
                                return Enum_classes.Token.Keyword, "return"
                            else:
                                error_handling()
                        else:
                            error_handling()
                    else:
                        error_handling()
                else:
                    error_handling()
            else:
                error_handling()
        # match symbol
        elif re.match(symbol_pattern, char):
            if char == "=":
                next_char = file.read(1)
                if next_char == "=":
                    return Enum_classes.Token.Symbol, "=="
                else:
                    file.seek(-1, 1)  # move file pointer 1 char behind current position
                    return Enum_classes.Token.Symbol, "="
            elif char == "/":  # match comment
                next_char = file.read(1)
                if next_char == "*":
                    while 1:
                        symbol_char = file.read(1)
                        if symbol_char == "*":
                            symbol_char2 = file.read(1)
                            if symbol_char2 == "/":
                                return
                            continue
                        else:
                            continue

                elif next_char == "/":  # match comment
                    while 1:
                        symbol_char = file.read(1)
                        if ord(symbol_char) == 10:
                            return
                        if symbol_char is None:  # end of file
                            file.close()
                        else:
                            continue
        elif char == "[":
            symbol = symbol + char
            while 1:
                symbol_char = file.read(1)
                if symbol_char == "]":
                    symbol = symbol + symbol_char
                    return Enum_classes.Token.Symbol, symbol
                else:
                    symbol = symbol + symbol_char
                    continue
        elif char == "{":
            symbol = symbol + char
            while 1:
                symbol_char = file.read(1)
                if symbol_char == "}":
                    symbol = symbol + symbol_char
                    return Enum_classes.Token.Symbol, symbol
                else:
                    symbol = symbol + symbol_char
                    continue
        elif char == "(":
            symbol = symbol + char
            while 1:
                symbol_char = file.read(1)
                if symbol_char == ")":
                    symbol = symbol + symbol_char
                    return Enum_classes.Token.Symbol, symbol
                else:
                    symbol = symbol + symbol_char
                    continue

        elif re.match(whitespace_pattern, char):
            return
        elif char is None:  # end of file
            file.close()
            return


def scanner():  # scanner
    "TO DO"


def symbol_table():
    "TO DO"


def error_handling():
    "DO TO PANIC MODE"


def error_massage_table():
    "TO DO"


if __name__ == '__main__':
    scanner()
    # # whitespace_pattern=re.compile("^[ \n\r\t\v\f]$")
    # w = " "
    # x = "q"
    # # re.match(pattern, w)
    # print(ord(w))
    # if re.match(whitespace_pattern, w):
    #     print("**")
