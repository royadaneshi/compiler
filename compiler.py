import copy
import re
import json
from anytree import Node, RenderTree
# Roya Daneshi 99101557 ,Pardis Zahraei 99109777
from string import Template


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

"""
phase 3
"""



class generator:
    def __init__(self):
        self.semantic_stack = []
        self.program_block = []
        self.i = 0  # address of the first empty home in program block
        self.t = 496  # increases 4 by 4
        # WHY 496?
        pass

    def find_addr(self,input):
        pass

    def codeGen(self,Action,input):
        if Action == 'A' or Action == 'B' or Action=='C':
            p = self.find_addr(input)
            self.semantic_stack.append(p)
        elif Action == 'D':
            self.semantic_stack.append(self.i)
            self.i=self.i+1
        elif Action == 'E':
            self.program_block[self.semantic_stack[self.t]].append(f'(JPF, {self.semantic_stack[self.t-1]},{self.i},)')
            self.semantic_stack.pop()
            self.semantic_stack.pop()
        elif Action == 'F':
            self.program_block[self.semantic_stack[self.t]].append(f'(JPF, {self.semantic_stack[self.t-1]},{self.i+1},)')
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.semantic_stack.append(self.i)
            self.i=self.i+1
        elif Action == 'G':
            self.program_block[self.semantic_stack[self.t]].append(f'(JP, {self.i},,)')
            self.semantic_stack.pop()
        elif Action == 'H':
            self.semantic_stack.append(self.i)
        elif Action == 'I':
            self.program_block[self.semantic_stack[self.t]].append(f'(JPF, {self.semantic_stack[self.t-1]},{self.i+1},)')
            self.program_block[self.i].append(f'(JP, {self.semantic_stack[self.t-2]},,)')
            self.i=self.i+1
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.semantic_stack.pop()
        elif Action == 'J':
          # i implement it as minus
            temp=self.get_temp()
            self.program_block[self.i].append(f'(==, {self.semantic_stack[self.t]},{self.semantic_stack[self.t]},{self.t})')
            self.i=self.i+1
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.semantic_stack.append(temp)
        elif Action == 'K':
            self.program_block[self.i].append(f'(:=, {self.semantic_stack[self.t]},{self.semantic_stack[self.t]},)')
            self.i=self.i+1
            self.semantic_stack.pop()
            self.semantic_stack.pop()
        elif Action == 'L':
            # what does it do?
            pass
        elif Action == 'M':
            temp = self.get_temp()
            self.program_block[self.i].append(
                f'(+, {self.semantic_stack[self.t]},{self.semantic_stack[self.t]},{self.t})')
            self.i = self.i + 1
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.semantic_stack.append(temp)
        elif Action == 'N':
            temp = self.get_temp()
            self.program_block[self.i].append(
                f'(-, {self.semantic_stack[self.t]},{self.semantic_stack[self.t]},{self.t})')
            self.i = self.i + 1
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.semantic_stack.append(temp)
        elif Action == 'P':
            temp = self.get_temp()
            self.program_block[self.i].append(
                f'(*, {self.semantic_stack[self.t]},{self.semantic_stack[self.t]},{self.t})')
            self.i = self.i + 1
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.semantic_stack.append(temp)
        elif Action == 'Q':
            temp = self.get_temp()
            self.program_block[self.i].append(
                f'(\, {self.semantic_stack[self.t]},{self.semantic_stack[self.t]},{self.t})')
            self.i = self.i + 1
            self.semantic_stack.pop()
            self.semantic_stack.pop()
            self.semantic_stack.append(temp)

    def code_gen(self, action_symbol):
        if action_symbol == 'ADD':
            self.ADD()
        elif action_symbol == 'MULT':
            self.MULT()
        elif action_symbol == 'SUB':
            self.SUB()
        elif action_symbol == 'EQ':
            self.EQ()
        elif action_symbol == 'LT':
            self.LT()
        elif action_symbol == 'ASSIGN':
            self.ASSIGN()
        elif action_symbol == 'JPF':
            self.JPF()
        elif action_symbol == 'JP':
            self.JP()
        elif action_symbol == 'PRINT':
            self.PRINT()
        else:
            print("invalid_semantic_action")

    def get_temp(self):
        self.t = self.t + 4
        return self.t

    def find_addr(self, variable):
        # TODO : looks up the current variable’s address from Symbol Table.
        pass

    def ADD(self, A1, A2, R):
        # t1 = self.get_temp()
        # top = len(self.semantic_stack) - 1
        self.program_block[self.i] = ('ADD', A1, A2, R)
        self.i = self.i + 1
        # self.semantic_stack.pop()
        # self.semantic_stack.pop()
        self.semantic_stack.append(R)
        return

    def MULT(self, A1, A2, R):
        # t1 = self.get_temp()
        # top = len(self.semantic_stack) - 1
        self.program_block[self.i] = ('MULT', A1, A2, R)
        self.i = self.i + 1
        # self.semantic_stack.pop()
        # self.semantic_stack.pop()
        self.semantic_stack.append(R)
        return

    def SUB(self, A1, A2, R):
        # t1 = self.get_temp()
        # top = len(self.semantic_stack) - 1
        self.program_block[self.i] = ('SUB', A1, A2, R)
        self.i = self.i + 1
        # self.semantic_stack.pop()
        # self.semantic_stack.pop()
        self.semantic_stack.append(R)
        return

    def EQ(self, A1, A2, R):
        # t1 = self.get_temp()
        # top = len(self.semantic_stack) - 1
        self.program_block[self.i] = ('EQ', A1, A2, R)
        self.i = self.i + 1
        # self.semantic_stack.pop()
        # self.semantic_stack.pop()
        self.semantic_stack.append(R)
        return

    def LT(self, A1, A2, R):
        self.program_block[self.i] = ('LT', A1, A2, R)
        self.i = self.i + 1
        self.semantic_stack.append(R)
        return

    def ASSIGN(self, A, R):
        # top = len(self.semantic_stack) - 1
        self.program_block[self.i] = ('ASSIGN', A, R, "")
        self.i = self.i + 1
        # self.semantic_stack.pop()
        # self.semantic_stack.pop()
        return

    def JPF(self, A, L):
        top = len(self.semantic_stack) - 1  ###############################?
        self.program_block[self.semantic_stack[top]] = ('JPF', A, L, "")
        # self.semantic_stack.pop()
        self.semantic_stack.pop()
        return

    def JP(self, L):
        top = len(self.semantic_stack) - 1
        self.program_block[self.semantic_stack[top]] = ('JP', L, "", "")
        self.semantic_stack.pop()
        return

    def PRINT(self,A):
        # top = len(self.semantic_stack) - 1
        self.program_block[self.i] = ('PRINT', A, "", "")
        self.i = self.i + 1
        # self.semantic_stack.pop()
        return

    # ---------------------------------------------------------------------------------------------------------






"""
PARSER PART
"""


class Parser:

    def __init__(self):
        self.follow = None
        self.first = None
        self.grammar = None
        self.terminals = None
        self.non_terminals = None
        self.parse_table = None
        self.read_json_file()
        self.stack = None
        self.input_tokens = None
        self.Program_node = None


    def parser(self, cursor_line_position_scanner, program_input):  # DONE
        Syntax_table = open("syntax_errors.txt", "w+")
        Syntax_table.write("There is no syntax error.")
        Syntax_table.close()
        parserr_table = open("parse_tree.txt", "w+")
        parserr_table.close()
        self.stack = []
        self.stack.append("$")  # initialize stack at start state
        self.stack.append("0")
        self.input_tokens = []
        # self.input_tokens.append("$")  # is it necessary?
        while True:
            first_token = get_next_token(cursor_line_position_scanner, program_input)
            cursor_line_position_scanner = first_token[2]
            if type(first_token) is tuple:
                l_element = len(first_token) - 1
                first_token = first_token[:l_element]
            if first_token[0] == "$":
                self.input_tokens.append(first_token)
                break  # end of file
            if first_token[1] == "":
                continue
            else:
                self.input_tokens.append(first_token)
                break

        while 1:
            stack_state = self.stack[-1]  # get top of the stack
            input_token = self.input_tokens[-1]
            if type(input_token) is tuple and len(input_token) == 3:
                l_element = len(input_token) - 1
                input_token = input_token[:l_element]
            # get top of the input tokens
            # check validation of input:
            # if input_token[1] in self.terminals or input_token[0] == "ID" or input_token[0] == "NUM" or input_token[
            #     0] == "$":
            state_columns_tuple = self.parse_table[stack_state]
            if input_token[1] in state_columns_tuple.keys() or input_token[0] in state_columns_tuple.keys():
                if input_token[0] == "ID" or input_token[0] == "NUM" or input_token[0] == "$":
                    table_content = self.parse_table[stack_state][input_token[0]]
                else:
                    table_content = self.parse_table[stack_state][input_token[1]]
                if table_content.startswith("shift"):
                    shifted_token = self.input_tokens.pop()
                    state_no = table_content.replace('shift_', '')
                    self.stack.append(shifted_token)
                    self.stack.append(state_no)
                    # get nex token(call scanner):
                    while True:
                        current_token = get_next_token(cursor_line_position_scanner, program_input)
                        cursor_line_position_scanner = current_token[2]
                        if type(current_token) is tuple and len(current_token) == 3:
                            l_element = len(current_token) - 1
                            current_token = current_token[:l_element]
                        if current_token[0] == "$":
                            self.input_tokens.append(current_token)
                            break  # end of file
                        if current_token[1] == "":
                            continue
                        else:
                            self.input_tokens.append(current_token)
                            break

                    continue
                elif table_content.startswith("reduce"):
                    rule_no = table_content.replace('reduce_', '')
                    reduce_rule = self.grammar[rule_no]
                    if reduce_rule[2] == "epsilon":  # if the rule goes to epsilon shouldn't pop anything from stack
                        size_pop_stack = 0
                        non_terminal_push = reduce_rule[0]
                        reduced_elements = ["epsilon", 1]
                    else:
                        size_pop_stack = 2 * (len(reduce_rule) - 2)
                        non_terminal_push = reduce_rule[0]
                        reduced_elements = self.stack[len(self.stack) - size_pop_stack:]

                    non_terminal_push_parent = Node(non_terminal_push)
                    for child in reduced_elements[::2]:
                        if isinstance(child, Node):
                            child.parent = non_terminal_push_parent
                        else:
                            Node(child, parent=non_terminal_push_parent)

                    self.stack = self.stack[:len(self.stack) - size_pop_stack]  # pop elements from the stack
                    top_stack_no = self.stack[-1]  # get top of the stack state number
                    non_terminal_goto = self.parse_table[top_stack_no]
                    if non_terminal_push in non_terminal_goto:  # impossible error but I checked it!
                        go_to = self.parse_table[top_stack_no][non_terminal_push]
                        num_push = go_to.replace('goto_', '')
                        self.stack.append(non_terminal_push_parent)  # push non-terminal
                        self.stack.append(num_push)
                        if non_terminal_push == 'program':
                            self.Program_node = non_terminal_push_parent

                    else:
                        # self.syntax_errors(None, None,
                        #    ParsErrorMsg.Empty_parse_table_goto)  # empty home on goto table
                        pass

                    continue

                elif table_content.startswith("accept"):
                    Node('$', parent=non_terminal_push_parent)
                    self.sketch_tree()
                    return 0  # say parse is finished

            else:
                syntax_errors = open("syntax_errors.txt", "r")
                content_file = syntax_errors.read()
                syntax_errors.close()
                if content_file == "There is no syntax error.":
                    syntax_errors = open("syntax_errors.txt", "w")
                    syntax_errors.close()

                type_1_error = "#$lineno : syntax error , illegal $terminal_err"
                type_2_error = "#$lineno : syntax error , discarded $terminal2_err from input"
                type_3_error = "syntax error , discarded $discard1 from stack"
                type_4_error = "#$lineno : syntax error , missing $terminal3_err"
                type_5_error = "#$lineno : syntax error , Unexpected EOF"
                # initial
                syntax_errors_file = open("syntax_errors.txt", "a+")
                error_msg = Template(type_1_error).substitute(lineno=cursor_line_position_scanner,
                                                              terminal_err=input_token[1])
                syntax_errors_file.write(error_msg + "\n")
                syntax_errors_file.close()
                # step 1
                s_final = 0
                self.input_tokens.pop()
                while True:
                    top_stack_no = self.stack[-1]
                    top_stack_name = self.stack[-2]
                    if (isinstance(top_stack_name, Node)):
                        s_name = top_stack_name.name
                        s_name = s_name.translate({ord(i): None for i in '\''})
                    else:
                        s_name = top_stack_name
                    list_nonterminals = []
                    non_terminal_goto = self.parse_table[top_stack_no]
                    for x in non_terminal_goto:
                        A = non_terminal_goto[x]
                        b = 'goto'
                        if b in A:
                            list_nonterminals.append(x)
                        sorted_list_As = sorted(list_nonterminals)
                    if len(list_nonterminals) != 0:
                        s_final = top_stack_no
                        break
                    if isinstance(self.stack[-2], tuple):
                        discarded = "(" + s_name[0] + ", " + s_name[1] + ")"
                    else:
                        discarded=s_name
                    syntax_errors_file = open("syntax_errors.txt", "a+")
                    error_msg = Template(type_3_error).substitute(discard1=discarded)
                    syntax_errors_file.write(error_msg + "\n")
                    syntax_errors_file.close()
                    self.stack.pop()
                    self.stack.pop()
                A_step2 = ""
                # step 2
                while (True):
                    current_token = get_next_token(cursor_line_position_scanner, program_input)
                    current_input = current_token[1]
                    if current_token[0] == "ID":
                        current_input = current_token[0]
                    cursor_line_position_scanner = current_token[2]
                    if (current_token[0] == "$"):
                        syntax_errors_file = open("syntax_errors.txt", "a+")
                        error_msg = Template(type_5_error).substitute(lineno=cursor_line_position_scanner)
                        syntax_errors_file.write(error_msg + "\n")
                        syntax_errors_file.close()

                        return
                    if current_input == '':

                        continue

                    for A in sorted_list_As:
                        follows_list = self.follow[A]

                        if (current_input in follows_list):
                            A_step2 = A
                            break
                    if (len(A_step2) != 0):
                        break
                    if(current_input=="ID"):
                        current_input=current_token[1]
                    syntax_errors_file = open("syntax_errors.txt", "a+")
                    error_msg = Template(type_2_error).substitute(lineno=cursor_line_position_scanner,
                                                                  terminal2_err=current_input)
                    syntax_errors_file.write(error_msg + "\n")
                    syntax_errors_file.close()
                # step 3
                if type(current_token) is tuple and len(current_token) == 3:
                    l_element = len(current_token) - 1
                    current_token = current_token[:l_element]
                self.input_tokens.append(current_token)
                self.stack.append(A_step2)
                new_state = self.parse_table[s_final][A_step2]
                num = ""
                for c in new_state:
                    if c.isdigit():
                        num = num + c
                self.stack.append(num)
                syntax_errors_file = open("syntax_errors.txt", "a+")
                error_msg = Template(type_4_error).substitute(lineno=cursor_line_position_scanner,
                                                              terminal3_err=A_step2)
                syntax_errors_file.write(error_msg + "\n")
                syntax_errors_file.close()

    def read_json_file(self):  # DONE  # this func called in init function at first.
        f = open('table.json')
        data = json.load(f)
        self.terminals = data["terminals"]
        self.non_terminals = data["non_terminals"]
        self.first = data["first"]
        self.follow = data["follow"]
        self.grammar = data["grammar"]
        self.parse_table = data["parse_table"]
        f.close()

    def sketch_tree(self):
        # initial

        parse_tree_file = open("parse_tree.txt", "w+")
        parse_tree_file.close()
        for pre, fill, node in RenderTree(self.Program_node):
            s = ("%s%s" % (pre, node.name))
            s = s.translate({ord(i): None for i in '\''})
            parse_tree_file = open("parse_tree.txt", "a", encoding="utf-8")
            if(node.name=="$"):
                parse_tree_file.write(s)
                parse_tree_file.close()
            else:
                parse_tree_file.write(s + "\n")
                parse_tree_file.close()



# this function reads from file character by character and finds token
# This functions returns current_position_of_cursor,Token_Type,Lexeme,current_line_position_of_cursor
"""
scanner
"""


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
    "Call the parser: "
    parser_obj = Parser()
    parser_obj.parser(cursor_line_position, program)

    # for witting in tokens.txt without any empty line at top of the file
    with open('tokens1.txt', 'r') as infile, open('tokens.txt', 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output
