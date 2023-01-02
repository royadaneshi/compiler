import re
import json

from anytree import Node


# from anytree import Node, RenderTree


# Roya Daneshi 99101557 ,Pardis Zahraei 99109777

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


class ParsErrorMsg:
    # WATCH OUT:  these two massage here not in the documentation format!
    Empty_parse_table = "Empty_parse_table_home"
    Empty_parse_table_goto = "Empty_parse_table_goto_home"
    # TODO complete error massages in panic mode here base on the documentation


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

        self.stack = []
        self.stack.append("$")  # initialize stack at start state
        self.stack.append("0")
        self.input_tokens = []
        # self.input_tokens.append("$")  # is it necessary?
        while True:
            first_token = get_next_token(cursor_line_position_scanner, program_input)
            cursor_line_position_scanner = first_token[2]
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
            input_token = self.input_tokens[-1]  # get top of the input tokens
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
                        self.syntax_errors(None, None,
                                           ParsErrorMsg.Empty_parse_table_goto)  # empty home on goto table
                    continue

                elif table_content.startswith("accept"):
                    self.sketch_tree()
                    print("parse completed!")
                    return 0  # say parse is finished

            else:  # empty home in table
                self.syntax_errors(input_token, stack_state, ParsErrorMsg.Empty_parse_table)

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
        for pre, fill, node in RenderTree(self.Program_node):
            print("%s%s" % (pre, node.name))

    # def parse_tree(self):
    #     # TODO make the parse tree and write in a output file
    #     """
    #     the given root to the function is not complete
    #     for example A -> B -> C -> D
    #     is needed to know where to put the link but only C -> D
    #     is given and some other tokens as root are not sent here like A -> B  in example above
    #     """
    #     # old code without treelib
    #     """
    #     list_all_dfs=[]
    #     print(parse_list)
    #     new_parse_list=copy.deepcopy(parse_list)
    #     top_elem = new_parse_list.pop()
    #     parent_1 = top_elem[0]
    #     child_1 = top_elem[1]
    #     child_1_without_bracket = child_1[0]
    #     if (len(child_1_without_bracket) == 3):
    #         child_1.pop()
    #     curent_list=[parent_1,child_1_without_bracket]
    #     child_1_without_bracket_before =child_1_without_bracket
    #     list_all_dfs.append(curent_list)
    #     for i in range (len(new_parse_list)):
    #         top_elem = new_parse_list.pop()
    #         parent_1 = top_elem[0]
    #         child_1 = top_elem[1]
    #         child_1_without_bracket = list(child_1[0])
    #         new_curent_list=copy.deepcopy(curent_list)
    #         if (len(child_1_without_bracket) == 3):
    #             child_1_without_bracket_before.pop()
    #         if(parent_1==child_1_without_bracket_before):
    #             new_curent_list.append(child_1_without_bracket)
    #         else:
    #             list_all_dfs.append(curent_list)
    #             for i in curent_list:
    #                 if (parent_1 == i):
    #                     curent_list=[]
    #                     curent_list.append(child_1_without_bracket)
    #         child_1_without_bracket_before=child_1_without_bracket
    #     """
    #     # method 1:
    #     # TODO if possible use treelib
    #     root = Node("program")
    #     nodes = {}
    #     nodes[root.name] = root
    #     print(parse_list)
    #     parse_list.reverse()
    #     for i in range(len(parse_list)):
    #         print(parse_list[i])
    #         top_elem = parse_list[i]
    #         parent_1 = top_elem[0]
    #         child_1 = top_elem[1]
    #         if (len(child_1) == 1):
    #             child_1_without_bracket = child_1[0]
    #             nodes[child_1_without_bracket] = Node(child_1_without_bracket, parent=nodes[parent_1])
    #         else:
    #             for i in range(len(child_1)):
    #                 child_1_without_bracket = child_1[i]
    #                 if (len(child_1_without_bracket) == 3):
    #                     l = list(child_1_without_bracket)
    #                     l.pop()
    #                     t = tuple(l)
    #                     nodes[str(t)] = Node(str(t), parent=nodes[parent_1])
    #                 else:
    #                     nodes[child_1_without_bracket] = Node(child_1_without_bracket, parent=nodes[parent_1])
    #     for pre, _, node in RenderTree(root):
    #         print("%s%s" % (pre, node.name))
    #
    #     return
    #     pass

    # method 2 draw DFS inputs
    # def add_roots(self, owner, data):
    #     o = owner.setdefault(data.pop(0), {})
    #     if data:
    #         self.add_roots(o, data)

    # def show(self, base, data):
    #     while data:
    #         k, v = data.pop(0)
    #         print('%s|-%s' % (base, k))
    #         if v:
    #             if data:
    #                 self.show(base + '| ', v.items())
    #             else:
    #                 self.show(base + '  ', v.items())

    # method 3:
    # TODO if possible use treelib
    """
    tree = Tree()
    tree.create_node("program", 0)  # root node
    id_glob = 0

    parse_list.reverse()
    for i in range(len(parse_list)):
        print(parse_list[i])
        top_elem = parse_list[i]
        id_parent = id_glob
        parent_1 = top_elem[0]
        child_1 = top_elem[1]
        if (len(child_1) == 1):
            child_1_without_bracket = child_1[0]
            id_glob = id_glob + 1
            tree.create_node(child_1_without_bracket, id_glob, parent=id_parent)
        else:
            for i in range(len(child_1)):
                id_glob = id_glob + 1
                child_1_without_bracket = child_1[i]
                if (len(child_1_without_bracket) == 3):
                    l = list(child_1_without_bracket)
                    l.pop()
                    t = tuple(l)
                    tree.create_node(str(t), id_glob, parent=id_parent)
                else:
                    tree.create_node(child_1_without_bracket, id_glob, parent=id_parent)
        tree.show()

    return
    pass
    def syntax_errors(self, input_token, stack_state, error_msg):
        # TODO fill the output error file and panic mode
        # not sure what panic mode in 3 steps mean can apply step 1 but not sure about step 2 , 3
        # will ask tas about it
        print("error")
        return
        pass
    """


"""
Scanner Part
"""


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
    global parse_list
    parse_list = []
    "Call the parser: "
    parser_obj = Parser()
    parser_obj.parser(cursor_line_position, program)

    # for witting in tokens.txt without any empty line at top of the file
    with open('tokens1.txt', 'r') as infile, open('tokens.txt', 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output
