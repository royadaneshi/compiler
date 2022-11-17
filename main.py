import re

import Enum_classes


def get_next_token():  # this function reads from file character by character and finds token
    file = open('input.txt', 'r')
    number = ""
    identifier = ""
    keyword = ""
    symbol = ""
    comment = ""
    number_pattern = re.compile("^[0-9]$")
    identifier_pattern1 = re.compile("^[A-Za-z]$")
    identifier_pattern2 = re.compile("^[A-Za-z0-9]$")
    symbol_pattern = re.compile("^[;:,+\-*<=/{}()\[\]]$")
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
                        if not symbol_char:  # end of file
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
        elif not char:  # end of file
            file.close()
            return
        else:
            error_handling(char, Enum_classes.ErrorMsg.Invalid_input)  # did not match any pattern


# def find_line_number_of_token():

def error_massage_table(line_number, token_until_here, error_massage):
    lexical_errors_file = open("lexical_errors.txt", "r")
    content_file = lexical_errors_file.read()
    lexical_errors_file.close()

    if content_file == "There is no lexical error.":
        lexical_errors_file = open("lexical_errors.txt", "w")
        lexical_errors_file.write("lineno  Error Message")
        lexical_errors_file.write("\n" + str(line_number) + "       (" + token_until_here + ", " + error_massage + ")")
        lexical_errors_file.close()
    else:
        lexical_errors_file = open("lexical_errors.txt", "a")
        lexical_errors_file.write("\n" + str(line_number) + "       (" + token_until_here + ", " + error_massage + ")")
        lexical_errors_file.close()


def symbol_table(no, lexeme):  # if symbol is new then add it to the table whit appropriate line number else don't
    symbol_table_file = open("symbol_table.txt", "a")
    symbol_table_file.write("\n" + str(no) + "  " + lexeme)
    symbol_table_file.close()


def scanner():  # scanner
    "TO DO"


def error_handling(token_until_here, error_massage):
    "TO DO PANIC MODE"


if __name__ == '__main__':
    " DO not change these lines"
    lexical_errors_file1 = open("lexical_errors.txt", "w+")
    lexical_errors_file1.write("There is no lexical error.")
    lexical_errors_file1.close()

    symbol_table_file1 = open("symbol_table.txt", "w+")
    symbol_table_file1.write("no  lexeme")
    symbol_table_file1.write("\n1   if")
    symbol_table_file1.write("\n2   else")
    symbol_table_file1.write("\n3   void")
    symbol_table_file1.write("\n4   int")
    symbol_table_file1.write("\n5   while")
    symbol_table_file1.write("\n6   break")
    symbol_table_file1.write("\n7   switch")
    symbol_table_file1.write("\n8   default")
    symbol_table_file1.write("\n9   case")
    symbol_table_file1.write("\n10   return")
    symbol_table_file1.write("\n11   endif")
    symbol_table_file1.close()
    ""
    scanner()
