import re
from enum import Enum, auto

class TokenCode(Enum):
    TOKEN_EMPTY = auto()
    TOKEN_ERROR = auto()
    TOKEN_IDENTIFIER = auto()
    TOKEN_VAR_IDENTIFIER = auto()
    TOKEN_NUMBER = auto()
    TOKEN_EOF = auto()
    TOKEN_COMMENTS = auto()
    TOKEN_UNKNOWN = auto()

    TOKEN_LPARENTHESIS = auto() 
    TOKEN_RPARENTHESIS = auto()
    TOKEN_COLON = auto()

    TOKEN_DEFINE = auto()
    TOKEN_DOMAIN = auto()
    TOKEN_REQUIREMENTS = auto()
    TOKEN_TYPES = auto()
    TOKEN_CONSTANTS = auto()
    TOKEN_PREDICATES = auto()
    TOKEN_FUNCTIONS = auto()
    TOKEN_CONSTRAINTS = auto()
    TOKEN_ACTION = auto()
    TOKEN_PARAMETERS = auto()
    TOKEN_PRECONDITION = auto()
    TOKEN_EFFECT = auto()
    TOKEN_DURATIVE_ACTION = auto()
    TOKEN_DURATION = auto()
    TOKEN_CONDITION = auto()
    TOKEN_DERIVED = auto()
    TOKEN_PROBLEM = auto()
    TOKEN_OBJECTS = auto()
    TOKEN_INIT = auto()
    TOKEN_GOAL = auto()
    TOKEN_METRIC = auto()
    TOKEN_TOTAL_TIME = auto()
    TOKEN_LENGTH = auto()
    TOKEN_SERIAL = auto()
    TOKEN_PARALLEL = auto()

    TOKEN_AND = auto()
    TOKEN_OR = auto()
    TOKEN_NOT = auto()
    TOKEN_IMPLY = auto()

    TOKEN_PLUS = auto()
    TOKEN_MINUS = auto()
    TOKEN_MULTIPLY = auto()
    TOKEN_DIVIDE = auto()
    TOKEN_LESS = auto()
    TOKEN_GREATER = auto()
    TOKEN_EQUAL = auto()
    TOKEN_LESS_EQUAL = auto()
    TOKEN_GREATER_EQUAL = auto()

    TOKEN_FORALL = auto()
    TOKEN_EXISTS = auto()

    TOKEN_WHEN = auto()

    TOKEN_ASSIGN = auto()
    TOKEN_SCALE_UP = auto()
    TOKEN_SCALE_DOWN = auto()
    TOKEN_INCREASE = auto()
    TOKEN_DECREASE = auto()

    TOKEN_AT = auto()
    TOKEN_OVER = auto()
    TOKEN_START = auto()
    TOKEN_END = auto()

    TOKEN_MINIMIZE = auto()
    TOKEN_MAXIMIZE = auto()


class Token:
    def __init__(self, content: str, code: TokenCode, line_num: int):
        self.content = content
        self.code = code
        self.line_num = line_num

KEYWORDS_MAP = {
    'define': TokenCode.TOKEN_DEFINE, 'domain': TokenCode.TOKEN_DOMAIN,
    'requirements': TokenCode.TOKEN_REQUIREMENTS, 'types': TokenCode.TOKEN_TYPES,
    'constants': TokenCode.TOKEN_CONSTANTS, 'predicates': TokenCode.TOKEN_PREDICATES,
    'functions': TokenCode.TOKEN_FUNCTIONS, 'constraints': TokenCode.TOKEN_CONSTRAINTS,
    'action': TokenCode.TOKEN_ACTION, 'parameters': TokenCode.TOKEN_PARAMETERS,
    'precondition': TokenCode.TOKEN_PRECONDITION, 'effect': TokenCode.TOKEN_EFFECT,
    'durative-action': TokenCode.TOKEN_DURATIVE_ACTION, 'duration': TokenCode.TOKEN_DURATION,
    'condition': TokenCode.TOKEN_CONDITION, 'derived': TokenCode.TOKEN_DERIVED,
    'problem': TokenCode.TOKEN_PROBLEM, 'objects': TokenCode.TOKEN_OBJECTS,
    'init': TokenCode.TOKEN_INIT, 'goal': TokenCode.TOKEN_GOAL,
    'metric': TokenCode.TOKEN_METRIC, 'total-time': TokenCode.TOKEN_TOTAL_TIME,
    'length': TokenCode.TOKEN_LENGTH, 'serial': TokenCode.TOKEN_SERIAL,
    'parallel': TokenCode.TOKEN_PARALLEL,
    'and': TokenCode.TOKEN_AND, 'or': TokenCode.TOKEN_OR, 'not': TokenCode.TOKEN_NOT, 'imply': TokenCode.TOKEN_IMPLY,
    'forall': TokenCode.TOKEN_FORALL, 'exists': TokenCode.TOKEN_EXISTS,
    'when': TokenCode.TOKEN_WHEN,
    'assign': TokenCode.TOKEN_ASSIGN, 'scale-up': TokenCode.TOKEN_SCALE_UP, 'scale-down': TokenCode.TOKEN_SCALE_DOWN,
    'increase': TokenCode.TOKEN_INCREASE, 'decrease': TokenCode.TOKEN_DECREASE,
    'at': TokenCode.TOKEN_AT, 'over': TokenCode.TOKEN_OVER, 'start': TokenCode.TOKEN_START, 'end': TokenCode.TOKEN_END,
    'minimize': TokenCode.TOKEN_MINIMIZE, 'maximize': TokenCode.TOKEN_MAXIMIZE
}

MULTI_CHAR_OPERATORS = {
    '>=': TokenCode.TOKEN_GREATER_EQUAL,
    '<=': TokenCode.TOKEN_LESS_EQUAL,
}

SINGLE_CHAR_OPERATORS = {
    '+': TokenCode.TOKEN_PLUS,
    '-': TokenCode.TOKEN_MINUS,
    '*': TokenCode.TOKEN_MULTIPLY,
    '/': TokenCode.TOKEN_DIVIDE,
    '<': TokenCode.TOKEN_LESS,
    '>': TokenCode.TOKEN_GREATER,
    '=': TokenCode.TOKEN_EQUAL,
}

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.position = 0
        self.current_line = 1

    def peek(self, offset=0) -> str:
        if self.position + offset < len(self.source_code):
            return self.source_code[self.position + offset]
        return ''

    def get_next_token(self) -> Token:
        while self.position < len(self.source_code):
            current_char = self.source_code[self.position]

            if current_char.isspace():
                if current_char == '\n':
                    self.current_line += 1
                self.position += 1
                continue

            if current_char == ';':
                while self.position < len(self.source_code) and self.source_code[self.position] != '\n':
                    self.position += 1
                if self.position < len(self.source_code) and self.source_code[self.position] == '\n':
                    self.current_line += 1
                    self.position += 1
                continue
            
            break 
        
        if self.position >= len(self.source_code):
            return Token("#EOF", TokenCode.TOKEN_EOF, self.current_line)

        start_pos = self.position
        current_char = self.source_code[self.position]

        if current_char == '(':
            self.position += 1
            return Token("(", TokenCode.TOKEN_LPARENTHESIS, self.current_line)
        if current_char == ')':
            self.position += 1
            return Token(")", TokenCode.TOKEN_RPARENTHESIS, self.current_line)
        if current_char == ':':
            self.position += 1
            return Token(":", TokenCode.TOKEN_COLON, self.current_line)

        if current_char == ';':
            while self.position < len(self.source_code) and self.source_code[self.position] != '\n':
                self.position += 1
            comment_content = self.source_code[start_pos:self.position]
            return Token(comment_content, TokenCode.TOKEN_COMMENTS, self.current_line)

        for op_str, op_code in MULTI_CHAR_OPERATORS.items():
            if self.source_code.startswith(op_str, self.position):
                self.position += len(op_str)
                return Token(op_str, op_code, self.current_line)
        
        if current_char in SINGLE_CHAR_OPERATORS:
            self.position += 1
            return Token(current_char, SINGLE_CHAR_OPERATORS[current_char], self.current_line)

        if current_char.isdigit():
            number = ''
            while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
                number += self.source_code[self.position]
                self.position += 1
            if self.position < len(self.source_code) and self.source_code[self.position] == '.':
                if self.position + 1 < len(self.source_code) and self.source_code[self.position + 1].isdigit():
                    number += self.source_code[self.position]
                    self.position += 1
                    while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
                        number += self.source_code[self.position]
                        self.position += 1
            return Token(number, TokenCode.TOKEN_NUMBER, self.current_line)
        
        if current_char.isalpha() or current_char == '?' or current_char == '-':
            atom = ""
            while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] in ['-', '_', '?']):
                atom += self.source_code[self.position]
                self.position += 1
            
            if atom.startswith('?'):
                if re.fullmatch(r'^\?[a-zA-Z][\w-]*$', atom):
                    return Token(atom, TokenCode.TOKEN_VAR_IDENTIFIER, self.current_line)
                else:
                    return Token(atom, TokenCode.TOKEN_UNKNOWN, self.current_line)
            
            if atom in KEYWORDS_MAP:
                return Token(atom, KEYWORDS_MAP[atom], self.current_line)
            
            if re.fullmatch(r'^[a-zA-Z][\w-]*$', atom):
                return Token(atom, TokenCode.TOKEN_IDENTIFIER, self.current_line)
            
            return Token(atom, TokenCode.TOKEN_UNKNOWN, self.current_line)

        self.position += 1
        return Token(current_char, TokenCode.TOKEN_UNKNOWN, self.current_line)
