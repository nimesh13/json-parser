from collections import deque
from enum import Enum

class TokenType(Enum):
    JSON_OPEN_BRACE = '{'
    JSON_CLOSE_BRACE = '}'
    JSON_OPEN_BRACKET = '['
    JSON_CLOSE_BRACKET = ']'
    JSON_COLON = ':'
    JSON_QUOTE = '"'
    JSON_COMMA = ','
    JSON_NUMBER = 'NUMBER'
    JSON_STRING = 'STRING'
    JSON_NULL = None
    JSON_BOOL_TRUE = True
    JSON_BOOL_FALSE = False
    JSON_SPACE = ' '
    JSON_CARRIAGE_RETURN = '\r'
    JSON_LINEFEED = '\n'
    JSON_TAB = '\t'

class Token:
    def __init__(self, type: TokenType, value=None):
        self.type = type
        self.value = value
        if self.value == None:
            self.value = self.type.value
    
    def __repr__(self) -> str:
        return "Token(type={}, value={})".format(self.type, self.value)

class Lexer:
    def __init__(self, input: str):
        self.tokens: list[Token] = []
        self.input = input
        self.length = len(input)
    
    def tokenize(self) -> None:
        i = 0

        while i < self.length:
            char = self.input[i]
            
            match char:
                case TokenType.JSON_SPACE.value:
                    self.tokens.append(Token(TokenType.JSON_SPACE))
                case TokenType.JSON_CARRIAGE_RETURN.value:
                    self.tokens.append(Token(TokenType.JSON_CARRIAGE_RETURN))
                case TokenType.JSON_LINEFEED.value:
                    self.tokens.append(Token(TokenType.JSON_LINEFEED))
                case TokenType.JSON_TAB.value:
                    self.tokens.append(Token(TokenType.JSON_TAB)) 
                case TokenType.JSON_OPEN_BRACE.value:
                    self.tokens.append(Token(TokenType.JSON_OPEN_BRACE))
                case TokenType.JSON_CLOSE_BRACE.value:
                    self.tokens.append(Token(TokenType.JSON_CLOSE_BRACE))
                case TokenType.JSON_OPEN_BRACKET.value:
                    self.tokens.append(Token(TokenType.JSON_OPEN_BRACKET))
                case TokenType.JSON_CLOSE_BRACKET.value:
                    self.tokens.append(Token(TokenType.JSON_CLOSE_BRACKET))
                case TokenType.JSON_COLON.value:
                    self.tokens.append(Token(TokenType.JSON_COLON))
                case TokenType.JSON_COMMA.value:
                    self.tokens.append(Token(TokenType.JSON_COMMA))
                case TokenType.JSON_QUOTE.value:
                    self.tokens.append(Token(TokenType.JSON_QUOTE))
                    str_token, index = self.get_string(i)
                    self.tokens.append(Token(TokenType.JSON_STRING, str_token))
                    i = index
                    self.tokens.append(Token(TokenType.JSON_QUOTE))
                    continue
                case char if char in '-0123456789':
                    num_token, index = self.get_number(i)
                    self.tokens.append(Token(TokenType.JSON_NUMBER, num_token))
                    i = index
                    continue
                case char if char == 'n' and i + 4 < self.length and self.input[i: i + 4] == 'null':
                    self.tokens.append(Token(TokenType.JSON_NULL))
                    i += 4
                    continue
                case char if char == 't' and i + 4 < self.length and self.input[i: i + 4] == 'true':
                    self.tokens.append(Token(TokenType.JSON_BOOL_TRUE))
                    i += 4
                    continue
                case char if char == 'f' and i + 5 < self.length and self.input[i: i + 5] == 'false':
                    self.tokens.append(Token(TokenType.JSON_BOOL_FALSE))
                    i += 5
                    continue
                case ' ':
                    pass
                case _:
                    raise Exception('Unexpected character \'{}\' at index {}'.format(char, i))

            i += 1

    def get_string(self, i) -> tuple[str, int]:
        str_tokens = deque()

        # Starting character is opening quote. Move forward.
        i += 1

        while i < self.length and self.input[i] != '"':
            str_tokens.append(self.input[i])
            i += 1

        if i == self.length or self.input[i] != '"':
            raise Exception('Missing end quote.')
        
        # End character is closing quote. Move forward.
        i += 1

        return ''.join(str_tokens), i

    def get_number(self, i) -> tuple[str, int]:
        int_tokens = deque()
        
        while i < self.length and self.input[i] in '-+0123456789.eE':
            int_tokens.append(self.input[i])
            i += 1
        
        return ''.join(int_tokens), i