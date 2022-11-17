import enum


class Token(enum):
    Invalid = 'Invalid'
    EndOfFile = 'EOF'
    Number = 'NUM'
    Identifier = 'ID'
    Keyword = 'KEYWORD'
    Symbol = 'SYMBOL'
    Comment = 'COMMENT'
    Whitespace = 'WHITESPACE'



