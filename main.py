import re
import os
import Enum_classes
import fileinput


# this function reads from file character by character and finds token
# This functions returns current_position_of_cursor,Token_Type,Lexeme,current_line_position_of_cursor
def get_next_token(current_position, line_position):
    file = open('input.txt', 'r')
    file.seek(0, os.SEEK_END)
    end_of_file = file.tell()
    file.seek(current_position)
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
    invalids_latter = re.compile("^[@!$_~]$")
    # read character by character
    char = file.read(1)
    if not char or file.tell() == end_of_file:  # end of file
        position = file.tell()
        file.close()
        return position, "EOF", "", line_position
    # match number
    elif re.match(number_pattern, char):
        number = number + char
        while 1:
            num_char = file.read(1)
            if re.match(number_pattern, num_char):
                number = number + num_char
            else:
                if re.match(identifier_pattern1, num_char):
                    error_input = number + num_char
                    error_massage_table(line_position, error_input, Enum_classes.ErrorMsg.Invalid_number)
                    return file.tell(), "", "", line_position
                elif re.match(invalids_latter, num_char):
                    error_input = number + num_char
                    error_massage_table(line_position, error_input, Enum_classes.ErrorMsg.Invalid_input)
                    return file.tell(), "", "", line_position
                else:
                    file.seek(file.tell() - 1)  # move file pointer 1 char behind current position
                    return file.tell(), Enum_classes.Token.Number, number, line_position
    # match identifier
    elif re.match(identifier_pattern1, char):
        identifier = identifier + char
        while 1:
            identifier_char = file.read(1)
            if re.match(identifier_pattern2, identifier_char):
                identifier = identifier + identifier_char
            # elif re.match(invalids_latter, identifier_char):
            #     error_input = identifier + identifier_char
            #     error_massage_table(line_position, error_input, Enum_classes.ErrorMsg.Invalid_input)
            #     return file.tell(), "", "", line_position
            else:
                file.seek(file.tell() - 1)  # move file pointer 1 char behind current position
                # match keywords
                if identifier == "if":
                    return file.tell(), Enum_classes.Token.Keyword, "if", line_position
                elif identifier == "else":
                    return file.tell(), Enum_classes.Token.Keyword, "else", line_position
                elif identifier == "void":
                    return file.tell(), Enum_classes.Token.Keyword, "void", line_position
                elif identifier == "int":
                    return file.tell(), Enum_classes.Token.Keyword, "int", line_position
                elif identifier == "while":
                    return file.tell(), Enum_classes.Token.Keyword, "while", line_position
                elif identifier == "break":
                    return file.tell(), Enum_classes.Token.Keyword, "break", line_position
                elif identifier == "switch":
                    return file.tell(), Enum_classes.Token.Keyword, "switch", line_position
                elif identifier == "default":
                    return file.tell(), Enum_classes.Token.Keyword, "default", line_position
                elif identifier == "case":
                    return file.tell(), Enum_classes.Token.Keyword, "case", line_position
                elif identifier == "return":
                    return file.tell(), Enum_classes.Token.Keyword, "return", line_position
                elif identifier == "endif":
                    return file.tell(), Enum_classes.Token.Keyword, "endif", line_position
                symbol_table(t, identifier)
                return file.tell(), Enum_classes.Token.Identifier, identifier, line_position
    # match symbol
    elif re.match(symbol_pattern, char):
        # symbol=symbol+char
        comment = comment + char
        if char == "=":
            next_char = file.read(1)
            if next_char == "=":
                return file.tell(), Enum_classes.Token.Symbol, "==", line_position
            else:
                file.seek(file.tell() - 1)  # move file pointer 1 char behind current position
                return file.tell(), Enum_classes.Token.Symbol, "=", line_position
        elif char == "/":  # match comment
            next_char = file.read(1)
            comment = comment + next_char
            if next_char == "*":
                while 1:
                    symbol_char = file.read(1)
                    comment = comment + symbol_char
                    if ord(symbol_char) == 10:
                        line_position = line_position + 1
                    if symbol_char == "*":
                        symbol_char2 = file.read(1)
                        if symbol_char2 == "/":
                            return file.tell(), "", "", line_position
                        continue
                    elif file.tell() == end_of_file:
                        error_massage_table(line_position, comment, Enum_classes.ErrorMsg.Unclosed_comment)
                        return file.tell(), "", "", line_position
            elif next_char == "/":  # match comment
                while 1:
                    symbol_char = file.read(1)
                    comment = comment + symbol_char
                    if ord(symbol_char) == 10:
                        line_position = line_position + 1  # it shows line position one more than real, when immediately EOF appears after it,but totaly works correct
                        return file.tell(), "", "", line_position
                    if file.tell() == end_of_file:  # end of file
                        file.close()
                        error_massage_table(line_position, comment, Enum_classes.ErrorMsg.Unclosed_comment)
                        return file.tell(), "", "", line_position
                    else:
                        continue
            else:
                file.seek(file.tell() - 1)  # move file pointer 1 char behind current position
                return file.tell(), Enum_classes.Token.Symbol, char, line_position
        elif char == "*":  # match comment
            next_char = file.read(1)
            if next_char == "/":
                error_massage_table(line_position, "*/", Enum_classes.ErrorMsg.Unmatched_comment)
                return file.tell(), "", "", line_position
            else:
                file.seek(file.tell() - 1)  # move file pointer 1 char behind current position
                return file.tell(), Enum_classes.Token.Symbol, char, line_position
        else:
            return file.tell(), Enum_classes.Token.Symbol, char, line_position

    elif re.match(whitespace_pattern, char):
        if ord(char) == 10:
            line_position = line_position + 1
        return file.tell(), "", "", line_position
    else:
        error_massage_table(line_position, char, Enum_classes.ErrorMsg.Invalid_input)  # did not match any pattern
        return file.tell(), "", "", line_position


def error_massage_table(line_number, token_until_here, error_massage):
    lexical_errors_file = open("lexical_errors.txt", "r")
    content_file = lexical_errors_file.read()
    lexical_errors_file.close()

    if content_file == "There is no lexical error.":
        lexical_errors_file = open("lexical_errors.txt", "w")

        if error_massage == Enum_classes.ErrorMsg.Invalid_input:
            lexical_errors_file.write(
                str(line_number) + "       (" + token_until_here + ", " + error_massage + ")")

        if error_massage == Enum_classes.ErrorMsg.Invalid_number:
            lexical_errors_file.write(
                str(line_number) + "       (" + token_until_here + ", " + error_massage + ")")
        if error_massage == Enum_classes.ErrorMsg.Unclosed_comment:
            lexical_errors_file.write(
                str(line_number) + "       (" + token_until_here[0:7] + "..., " + error_massage + ")")
        if error_massage == Enum_classes.ErrorMsg.Unmatched_comment:
            lexical_errors_file.write(
                str(line_number) + "       (" + token_until_here + ", " + error_massage + ")")
    else:
        lexical_errors_file = open("lexical_errors.txt", "a")
        if error_massage == Enum_classes.ErrorMsg.Invalid_input:
            lexical_errors_file.write(
                "\n" + str(line_number) + "       (" + token_until_here + ", " + error_massage + ")")

        if error_massage == Enum_classes.ErrorMsg.Invalid_number:
            lexical_errors_file.write(
                "\n" + str(line_number) + "       (" + token_until_here + ", " + error_massage + ")")
        if error_massage == Enum_classes.ErrorMsg.Unclosed_comment:
            lexical_errors_file.write(
                "\n" + str(line_number) + "       (" + token_until_here[0:7] + "..., " + error_massage + ")")
        if error_massage == Enum_classes.ErrorMsg.Unmatched_comment:
            lexical_errors_file.write(
                "\n" + str(line_number) + "       (" + token_until_here + ", " + error_massage + ")")
    lexical_errors_file.close()


def symbol_table(no, lexeme):  # if symbol is new then add it to the table whit appropriate line number else don't
    symbol_table_file = open("symbol_table.txt", "a")
    if list_1.count(lexeme) == 0:
        list_1.append(lexeme)
        symbol_table_file.write("\n" + str(no) + "  " + lexeme)
        global t
        t = no + 1
    symbol_table_file.close()


def initialize():
    lexical_errors_file1 = open("lexical_errors.txt", "w+")
    lexical_errors_file1.write("There is no lexical error.")
    lexical_errors_file1.close()

    symbol_table_file1 = open("symbol_table.txt", "w+")
    symbol_table_file1.write("1.   if")
    symbol_table_file1.write("\n2.   else")
    symbol_table_file1.write("\n3.   void")
    symbol_table_file1.write("\n4.   int")
    symbol_table_file1.write("\n5.   while")
    symbol_table_file1.write("\n6.   break")
    symbol_table_file1.write("\n7.   switch")
    symbol_table_file1.write("\n8.   default")
    symbol_table_file1.write("\n9.   case")
    symbol_table_file1.write("\n10.   return")
    symbol_table_file1.write("\n11.   endif")
    symbol_table_file1.close()

    tokens_table_file = open("tokens1.txt", "w+")
    tokens_table_file.close()


def printing(to):
    global current_line
    if to[1] != "":
        tokens_table_file = open("tokens1.txt", "r")
        content = str(tokens_table_file.read())
        value = '\n' + str(to[3])
        if to[3] != current_line and not value in content:
            if to[3] == 1:
                tokens_table_file = open("tokens1.txt", "a")
                tokens_table_file.write(str(to[3]) + "    " + "(" + to[1] + ", " + to[2] + ") ")
                current_line = current_line + 1
                tokens_table_file.close()
            else:
                tokens_table_file = open("tokens1.txt", "a")
                tokens_table_file.write("\n" + str(to[3]) + "    " + "(" + to[1] + ", " + to[2] + ") ")
                current_line = current_line + 1
                tokens_table_file.close()
        else:
            tokens_table_file = open("tokens1.txt", "a")
            tokens_table_file.write("(" + to[1] + ", " + to[2] + ") ")
            tokens_table_file.close()


if __name__ == '__main__':
    " DO not change these lines"
    list_1 = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return", "endif"]
    initialize()
    cursor_position = 0
    cursor_line_position = 1
    ""
    t = 12
    current_line = 0
    " test get_token function :"
    while 1:
        ans = get_next_token(cursor_position, cursor_line_position)
        cursor_position = ans[0]
        cursor_line_position = ans[3]
        if ans[1] == "EOF":
            break
        printing(ans)

    # for witting in tokens.txt without any empty line at top of the file
    with open('tokens1.txt', 'r') as infile, open('tokens.txt', 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output
