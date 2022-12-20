import re


# Pardis Zahraei 99109777 , Roya Daneshi 99101557

class Token:
    Invalid = 'Invalid'
    EndOfFile = 'EOF'
    Number = 'NUM'
    Identifier = 'ID'
    Keyword = 'KEYWORD'
    Symbol = 'SYMBOL'
    Comment = 'COMMENT'
    Whitespace = 'WHITESPACE'


class ErrorMsg:
    Invalid_input = 'Invalid input'
    Unclosed_comment = 'Unclosed comment'
    Unmatched_comment = 'Unmatched comment'
    Invalid_number = 'Invalid number'


def parser():
    # TODO implement the parser
    pass


def c_minus_grammar():
    # TODO put c-minus grammar in a 2D list
    pass


def get_LALR_table_by_bison():
    # TODO get tabel from bison
    pass


def parse_tree():
    # TODO make the parse tree and write in a output file
    pass


def syntax_errors():
    # TODO fill the output error file and panic mode
    pass


# this function reads from file character by character and finds token
# This functions returns current_position_of_cursor,Token_Type,Lexeme,current_line_position_of_cursor
def get_next_token(line_position, program):
    global line_read
    global index
    end_of_file = len(program)
    number = ""
    identifier = ""
    comment = ""
    number_pattern = re.compile("^[0-9]$")
    identifier_pattern1 = re.compile("^[A-Za-z]$")
    identifier_pattern2 = re.compile("^[A-Za-z0-9]$")
    symbol_pattern = re.compile("^[;:,+\-*<=/{}()\[\]]$")
    whitespace_pattern = re.compile("^[ \n\r\t\v\f]$")
    invalids_latter = re.compile("^[#@!$_~&]$")
    char = ""
    if index != end_of_file:
        char = program[index]
        index = index + 1

    if not char and index == end_of_file:  # end of file
        return "$", "", line_position
    # match number
    elif re.match(number_pattern, char):
        number = number + char
        while 1:
            num_char = program[index]
            index = index + 1
            if re.match(number_pattern, num_char):
                number = number + num_char
            else:
                if re.match(identifier_pattern1, num_char):
                    error_input = number + num_char
                    error_massage_table(line_position, error_input, ErrorMsg.Invalid_number)
                    return "", "", line_position
                elif re.match(invalids_latter, num_char):
                    error_input = number + num_char
                    error_massage_table(line_position, error_input, ErrorMsg.Invalid_input)
                    return "", "", line_position
                else:
                    index = index - 1  # move file pointer 1 char behind current position
                    return Token.Number, number, line_position
    # match identifier
    elif re.match(identifier_pattern1, char):
        identifier = identifier + char
        while 1:
            identifier_char = program[index]
            index = index + 1
            if re.match(identifier_pattern2, identifier_char):
                identifier = identifier + identifier_char
            elif re.match(invalids_latter, identifier_char):
                error_input = identifier + identifier_char
                error_massage_table(line_position, error_input, ErrorMsg.Invalid_input)
                return "", "", line_position
            else:
                index = index - 1  # move file pointer 1 char behind current position
                # match keywords
                if identifier == "if":
                    return Token.Keyword, "if", line_position
                elif identifier == "else":
                    return Token.Keyword, "else", line_position
                elif identifier == "void":
                    return Token.Keyword, "void", line_position
                elif identifier == "int":
                    return Token.Keyword, "int", line_position
                elif identifier == "while":
                    return Token.Keyword, "while", line_position
                elif identifier == "break":
                    return Token.Keyword, "break", line_position
                elif identifier == "switch":
                    return Token.Keyword, "switch", line_position
                elif identifier == "default":
                    return Token.Keyword, "default", line_position
                elif identifier == "case":
                    return Token.Keyword, "case", line_position
                elif identifier == "return":
                    return Token.Keyword, "return", line_position
                elif identifier == "endif":
                    return Token.Keyword, "endif", line_position
                symbol_table(t, identifier)
                return Token.Identifier, identifier, line_position
    # match symbol
    elif re.match(symbol_pattern, char):
        comment = comment + char
        if char == "=":
            next_char = program[index]
            index = index + 1
            if next_char == "=":
                return Token.Symbol, "==", line_position
            elif re.match(invalids_latter, next_char):
                error_input = comment + next_char
                error_massage_table(line_position, error_input, ErrorMsg.Invalid_input)
                return "", "", line_position
            else:
                index = index - 1  # move file pointer 1 char behind current position
                return Token.Symbol, "=", line_position
        elif char == "/":  # match comment
            next_char = program[index]
            index = index + 1
            comment = comment + next_char
            if next_char == "*":
                line_position_cpy = line_position
                while 1:
                    symbol_char = program[index]
                    index = index + 1
                    comment = comment + symbol_char
                    if ord(symbol_char) == 10:
                        line_position = line_position + 1
                    if symbol_char == "*":
                        symbol_char2 = program[index]
                        index = index + 1
                        if symbol_char2 == "/":
                            return "", "", line_position
                        continue
                    elif index == end_of_file:
                        error_massage_table(line_position_cpy, comment, ErrorMsg.Unclosed_comment)
                        return "", "", line_position
            elif next_char == "/":  # match comment
                while 1:
                    symbol_char = program[index]
                    index = index + 1

                    comment = comment + symbol_char
                    if ord(symbol_char) == 10:
                        line_position = line_position + 1  # it shows line position one more than real, when immediately EOF appears after it,but totaly works correct
                        return "", "", line_position
                    if index == end_of_file:  # end of file
                        file.close()
                        error_massage_table(line_position, comment, ErrorMsg.Unclosed_comment)
                        return "", "", line_position
                    else:
                        continue
            elif re.match(invalids_latter, next_char):
                error_input = comment
                error_massage_table(line_position, error_input, ErrorMsg.Invalid_input)
                return "", "", line_position
            else:
                index = index - 1  # move file pointer 1 char behind current position
                return Token.Symbol, char, line_position
        elif char == "*":  # match comment
            next_char = program[index]
            index = index + 1
            if next_char == "/":
                error_massage_table(line_position, "*/", ErrorMsg.Unmatched_comment)
                return "", "", line_position
            elif re.match(invalids_latter, next_char):
                error_input = comment + next_char
                error_massage_table(line_position, error_input, ErrorMsg.Invalid_input)
                return "", "", line_position
            else:
                index = index - 1  # move file pointer 1 char behind current position
                return Token.Symbol, char, line_position
        else:
            return Token.Symbol, char, line_position

    elif re.match(whitespace_pattern, char):
        if ord(char) == 10:
            line_position = line_position + 1
        return "", "", line_position
    else:
        error_massage_table(line_position, char, ErrorMsg.Invalid_input)  # did not match any pattern
        return "", "", line_position


def error_massage_table(line_number, token_until_here, error_massage):
    lexical_errors_file = open("lexical_errors.txt", "r")
    content_file = lexical_errors_file.read()
    lexical_errors_file.close()
    global error_line
    if content_file == "There is no lexical error.":
        lexical_errors_file = open("lexical_errors.txt", "w")

        if error_massage == ErrorMsg.Invalid_input:
            lexical_errors_file.write(
                str(line_number) + "." + "\t" + "(" + token_until_here + ", " + error_massage + ") ")
            error_line = line_number
        if error_massage == ErrorMsg.Invalid_number:
            lexical_errors_file.write(
                str(line_number) + "." + "\t" + "(" + token_until_here + ", " + error_massage + ") ")
            error_line = line_number
        if error_massage == ErrorMsg.Unclosed_comment:
            lexical_errors_file.write(
                str(line_number) + "." + "\t" + "(" + token_until_here[0:7] + "..., " + error_massage + ") ")
            error_line = line_number
        if error_massage == ErrorMsg.Unmatched_comment:
            lexical_errors_file.write(
                str(line_number) + "." + "\t" + "(" + token_until_here + ", " + error_massage + ") ")
            error_line = line_number
    else:

        if error_line == line_number:
            lexical_errors_file = open("lexical_errors.txt", "a")
            if error_massage == ErrorMsg.Invalid_input:
                lexical_errors_file.write(
                    "(" + token_until_here + ", " + error_massage + ") ")
            if error_massage == ErrorMsg.Invalid_number:
                lexical_errors_file.write(
                    "(" + token_until_here + ", " + error_massage + ") ")
            if error_massage == ErrorMsg.Unclosed_comment:
                lexical_errors_file.write(
                    "(" + token_until_here[0:7] + "..., " + error_massage + ") ")
            if error_massage == ErrorMsg.Unmatched_comment:
                lexical_errors_file.write(
                    "(" + token_until_here + ", " + error_massage + ") ")
            lexical_errors_file.close()
        else:
            lexical_errors_file = open("lexical_errors.txt", "a")
            error_line = line_number
            if error_massage == ErrorMsg.Invalid_input:
                lexical_errors_file.write(
                    "\n" + str(line_number) + "." + "\t" + "(" + token_until_here + ", " + error_massage + ") ")

            if error_massage == ErrorMsg.Invalid_number:
                lexical_errors_file.write(
                    "\n" + str(line_number) + "." + "\t" + "(" + token_until_here + ", " + error_massage + ") ")
            if error_massage == ErrorMsg.Unclosed_comment:
                lexical_errors_file.write(
                    "\n" + str(line_number) + "." + "\t" + "(" + token_until_here[0:7] + "..., " + error_massage + ") ")
            if error_massage == ErrorMsg.Unmatched_comment:
                lexical_errors_file.write(
                    "\n" + str(line_number) + "." + "\t" + "(" + token_until_here + ", " + error_massage + ") ")
            lexical_errors_file.close()


def symbol_table(no, lexeme):  # if symbol is new then add it to the table whit appropriate line number else don't
    symbol_table_file = open("symbol_table.txt", "a")
    if list_1.count(lexeme) == 0:
        list_1.append(lexeme)
        symbol_table_file.write("\n" + str(no) + ".\t" + lexeme)
        global t
        t = no + 1
    symbol_table_file.close()


def initialize():
    lexical_errors_file1 = open("lexical_errors.txt", "w+")
    lexical_errors_file1.write("There is no lexical error.")
    lexical_errors_file1.close()

    symbol_table_file1 = open("symbol_table.txt", "w+")
    symbol_table_file1.write("1.\tif")
    symbol_table_file1.write("\n2.\telse")
    symbol_table_file1.write("\n3.\tvoid")
    symbol_table_file1.write("\n4.\tint")
    symbol_table_file1.write("\n5.\twhile")
    symbol_table_file1.write("\n6.\tbreak")
    symbol_table_file1.write("\n7.\tswitch")
    symbol_table_file1.write("\n8.\tdefault")
    symbol_table_file1.write("\n9.\tcase")
    symbol_table_file1.write("\n10.\treturn")
    symbol_table_file1.write("\n11.\tendif")
    symbol_table_file1.close()

    tokens_table_file = open("tokens1.txt", "w+")
    tokens_table_file.close()


def printing(to):
    global current_line
    if to[0] != "":
        tokens_table_file = open("tokens1.txt", "r")
        content = str(tokens_table_file.read())
        value = '\n' + str(to[2])
        if to[2] != current_line and not value in content:
            if to[2] == 1:
                tokens_table_file = open("tokens1.txt", "a")
                tokens_table_file.write(str(to[2]) + "." + "\t" + "(" + to[0] + ", " + to[1] + ") ")
                current_line = current_line + 1
                tokens_table_file.close()
            else:
                tokens_table_file = open("tokens1.txt", "a")
                tokens_table_file.write("\n" + str(to[2]) + "." + "\t" + "(" + to[0] + ", " + to[1] + ") ")
                current_line = current_line + 1
                tokens_table_file.close()
        else:
            tokens_table_file = open("tokens1.txt", "a")
            tokens_table_file.write("(" + to[0] + ", " + to[1] + ") ")
            tokens_table_file.close()


if __name__ == '__main__':
    " DO not change these lines"
    list_1 = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return", "endif"]
    initialize()
    cursor_position = 0
    cursor_line_position = 1
    ""
    line_read = 1
    t = 12
    error_line = 0
    current_line = 0
    file = open('input.txt', 'r')
    program = file.read()
    index = 0
    " test get_token function :"
    while 1:
        ans = get_next_token(cursor_line_position, program)
        cursor_line_position = ans[2]
        if ans[0] == "$":
            break
        printing(ans)

    # for witting in tokens.txt without any empty line at top of the file
    with open('tokens1.txt', 'r') as infile, open('tokens.txt', 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output
