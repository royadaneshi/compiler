import re

import Enum_classes


def get_next_token():  # read from file
    file = open('input.txt', 'r')
    number = ""
    identifier = ""
    keyword = ""
    symbol = ""
    comment = ""
    number_pattern = re.compile("^[0-9]$")
    identifier_pattern1 = re.compile("^[A-Za-z]$")
    identifier_pattern2 = re.compile("^[A-Za-z0-9]$")
    symbol_pattern = re.compile("^[;:,+\-*<=/{}()\[\]]$")  # ==
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
                    if re.match(identifier_pattern1, num_char):
                        error_input = number + num_char
                        error_handling(error_input, Enum_classes.ErrorMsg.Invalid_number)
                        return
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
                    # match keywords
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
        # match symbol
        elif re.match(symbol_pattern, char):
            # symbol=symbol+char
            comment = comment + char
            if char == "=":
                next_char = file.read(1)
                if next_char == "=":
                    return Enum_classes.Token.Symbol, "=="
                else:
                    file.seek(-1, 1)  # move file pointer 1 char behind current position
                    return Enum_classes.Token.Symbol, "="
            elif char == "/":  # match comment
                next_char = file.read(1)
                comment = comment + next_char
                if next_char == "*":
                    while 1:
                        symbol_char = file.read(1)
                        comment = comment + symbol_char
                        if symbol_char == "*":
                            symbol_char2 = file.read(1)
                            if symbol_char2 == "/":
                                return
                            continue
                        elif symbol_char is None:
                            error_handling(comment, Enum_classes.ErrorMsg.Unclosed_comment)
                            continue

                elif next_char == "/":  # match comment
                    while 1:
                        symbol_char = file.read(1)
                        comment = comment + symbol_char
                        if ord(symbol_char) == 10:
                            return
                        if symbol_char is None:  # end of file
                            file.close()
                            error_handling(comment, Enum_classes.ErrorMsg.Unclosed_comment)
                        else:
                            continue
                else:
                    return Enum_classes.Token.Symbol, char
            elif char == "*":  # match comment
                next_char = file.read(1)
                if next_char == "/":
                    error_handling("*/", Enum_classes.ErrorMsg.Unmatched_comment)
                else:
                    return Enum_classes.Token.Symbol, char
            else:
                return Enum_classes.Token.Symbol, char

        elif re.match(whitespace_pattern, char):
            return
        elif char is None:  # end of file
            file.close()
            return
        else:
            error_handling(char, Enum_classes.ErrorMsg.Invalid_input)  # did not match any pattern


def scanner():  # scanner
    "TO DO"


def symbol_table():
    "TO DO"


def error_handling(token_until_here, error_massage):
    "DO TO PANIC MODE"


def error_massage_table():
    "TO DO"


if __name__ == '__main__':
    # scanner()
    # # whitespace_pattern=re.compile("^[ \n\r\t\v\f]$")
    w = "[]"
    # x = "q"
    # # re.match(pattern, w)
    # print(ord(w))

    symbol_pattern = re.compile("^[;:,+\-*<=/{}()\[\]]$")  # ==

    if re.match(symbol_pattern, w):
        print("**")
