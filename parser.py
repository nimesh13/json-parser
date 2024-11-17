from collections import deque
from math import inf
from lexer import Lexer
from lexer import TokenType, Token

JSON_WHITESPACE = [TokenType.JSON_SPACE, TokenType.JSON_CARRIAGE_RETURN, TokenType.JSON_LINEFEED, TokenType.JSON_TAB]

class Parser:
    def __init__(self, str: str):
        self.str = str
        self.lexer = Lexer(str)
        self.lexer.tokenize()
        
        self.pointer = 0
        self.json = self.parse()

    def parse(self):
        token = self.lexer.tokens[self.pointer]
        match token.type:
            case TokenType.JSON_OPEN_BRACE:
                return self.parse_object()
            case TokenType.JSON_OPEN_BRACKET:
                return self.parse_array()
            case _:
                raise Exception(f"Unexpected token '{token.value}' at index {self.pointer}")

    def parse_object(self):
        obj = {}
        states = [
            {'open_brace': 1},
            {'whitespace': 2, 'close_brace': 3, 'quote': 4},
            {'whitespace': 2, 'close_brace': 3, 'quote': 4},
            {},
            {'whitespace': 5, 'colon': 6},
            {'whitespace': 5, 'colon': 6},
            {'value': 8, 'whitespace': 7},
            {'value': 8, 'whitespace': 7},
            {'whitespace': 9, 'close_brace': 3, 'comma': 10},
            {'whitespace': 9, 'close_brace': 3, 'comma': 10},
            {'whitespace': 11, 'quote': 4},
            {'whitespace': 11, 'quote': 4}
        ]
        current_state = 0
        key = None
        value = inf
        
        while self.pointer < len(self.lexer.tokens):
            token: Token = self.lexer.tokens[self.pointer]
            
            if current_state == 0 and token.type == TokenType.JSON_OPEN_BRACE:
                group = 'open_brace'
            elif token.type == TokenType.JSON_CLOSE_BRACE:
                group = 'close_brace'
            elif token.type == TokenType.JSON_COMMA:
                group = 'comma'
            elif token.type == TokenType.JSON_COLON:
                group = 'colon'
            elif token.type in JSON_WHITESPACE:
                group = 'whitespace'
            elif token.type == TokenType.JSON_QUOTE and not key:
                group = 'quote'
                key = self.parse_string()
            else:
                group = 'value'
                value = self.parse_value()
            
            if group not in states[current_state]:
                raise Exception(f"Unexpected token '{token.value}' at index {self.pointer}")
            
            current_state = states[current_state][group]
            
            # If we've reached the end state (state 2), stop processing
            if current_state == 3:
                break
            
            if key is not None and value != inf:
                obj[key] = value
                key = None
                value = inf
            self.pointer += 1
        
        if current_state != 3:
            raise Exception('Unexpected character \'{}\' at index {}'.format(self.str[self.pointer], self.pointer))
        
        return obj

    def parse_array(self):
        array = deque()
        states = [
            {'open_bracket': 1},
            {'close_bracket': 2, 'whitespace': 3, 'value': 4 },
            {},
            {'close_bracket': 2, 'whitespace': 3, 'value': 4},
            {'comma': 6, 'close_bracket': 2, 'whitespace': 5},
            {'comma': 6, 'close_bracket': 2, 'whitespace': 5},
            {'value': 4, 'whitespace': 3}
        ]
        current_state = 0
        
        while self.pointer < len(self.lexer.tokens):
            token: Token = self.lexer.tokens[self.pointer]
            
            if current_state == 0 and token.type == TokenType.JSON_OPEN_BRACKET:
                group = 'open_bracket'
            elif token.type == TokenType.JSON_CLOSE_BRACKET:
                group = 'close_bracket'
            elif token.type in JSON_WHITESPACE:
                group = 'whitespace'
            elif token.type == TokenType.JSON_COMMA:
                group = 'comma'
            else:
                group = 'value'
                value = self.parse_value()
                array.append(value)
            
            if group not in states[current_state]:
                raise Exception(f"Unexpected character '{token.value}' at index {self.pointer}")
            
            current_state = states[current_state][group]
            
            # If we've reached the end state (state 2), stop processing
            if current_state == 2:
                break
            
            self.pointer += 1
        
        if current_state != 2:
            raise Exception('Unexpected character \'{}\' at index {}'.format(self.lexer.tokens[self.pointer], self.pointer))
        
        return list(array)
    
    def parse_number(self):
        token_value = self.lexer.tokens[self.pointer].value
        int_tokens = ""
        states = [
            # State 0: Initial state
            # If the character is a minus sign, transition to state 1
            # If the character is '0', transition to state 2
            # If the character is a digit between 1-9, transition to state 3
            {'minus': 1, 'zero': 2, 'digits_1_to_9': 3},
            
            # State 1: After encountering a minus sign
            # If the character is '0', transition to state 2
            # If the character is a digit between 1-9, transition to state 3
            {'zero': 2, 'digits_1_to_9': 3},
            
            # State 2: After encountering '0'
            # If the character is a dot (.), transition to state 5 (start of a decimal part)
            # If the character is an exponent ('e' or 'E'), transition to state 6 (start of exponent part)
            {'dot': 5, 'exponent': 6},
            
            # State 3: After encountering a digit from 1-9
            # If the character is a dot (.), transition to state 5 (start of a decimal part)
            # If the character is an exponent ('e' or 'E'), transition to state 6 (start of exponent part)
            # If the character is a digit (0-9), remain in state 4 (continue reading digits)
            {'dot': 5, 'exponent': 6, 'digits_0_to_9': 4},
            
            # State 4: After encountering additional digits
            # If the character is a digit (0-9), remain in state 4 (continue reading digits)
            # If the character is a dot (.), transition to state 5 (start of decimal part)
            # If the character is an exponent ('e' or 'E'), transition to state 6 (start of exponent part)
            {'digits_0_to_9': 4, 'dot': 5, 'exponent': 6},
        
            # State 5: After encountering a dot (decimal point)
            # If the character is a digit (0-9), transition to state 7 (start of the fractional part)
            {'digits_0_to_9': 7},
            
            # State 6: After encountering an exponent ('e' or 'E')
            # If the character is a sign ('+' or '-'), transition to state 8 (to handle the sign of the exponent)
            # If the character is a digit (0-9), transition to state 9 (to start reading the exponent digits)
            {'sign': 8, 'digits_0_to_9': 9},
            
            # State 7: After encountering digits in the fractional part
            # If the character is a digit (0-9), remain in state 7 (continue reading the fractional part)
            # If the character is an exponent ('e' or 'E'), transition to state 6 (start of exponent part)
            {'digits_0_to_9': 7, 'exponent': 6},
            
            # State 8: After encountering a sign in the exponent part
            # If the character is a digit (0-9), transition to state 9 (start reading the exponent digits)
            {'digits_0_to_9': 9},
            
            # State 9: After encountering digits in the exponent part
            # If the character is a digit (0-9), remain in state 9 (continue reading the exponent digits)
            {'digits_0_to_9': 9}
        ]

        current_state = 0
        i = 0
        length = len(token_value)
        exponent = False
        fraction = False

        while i < length:
            char = token_value[i]

            # Only in the initial two states, we need to check 'zero' and 'minus' states.
            if current_state == 0 or current_state == 1:
                if char == '0':
                    group = 'zero'
                elif char in '123456789':
                    group = 'digits_1_to_9'
                elif char == '-':
                    group = 'minus'
                else:
                    raise Exception(f"Unexpected character '{char}' at index {i} for starting a number")
            else:
                if char in '0123456789':
                    group = 'digits_0_to_9'
                elif char in '+-':
                    group = 'sign'
                elif char in 'eE':
                    group = 'exponent'
                    exponent = True
                elif char == '.':
                    group = 'dot'
                    fraction = True
                else:
                    break
            
            if group not in states[current_state]:
                raise Exception(f"Unexpected character '{char}' at index {i}")

            current_state = states[current_state][group]
            int_tokens += char
            i += 1
        
        if current_state not in [3, 4, 7, 9]:
            raise Exception('Unexpected character \'{}\' at index {}'.format(token_value[i - 1], i - 1))

        if exponent or fraction:
            return float(int_tokens)
        return int(int_tokens)

    def parse_value(self):
        token = self.lexer.tokens[self.pointer]
        
        match token.type:
            case TokenType.JSON_BOOL_TRUE | TokenType.JSON_BOOL_FALSE | TokenType.JSON_NULL:
                return token.value
            case _ if token.type == TokenType.JSON_NUMBER:
                return self.parse_number()
            case _ if token.type == TokenType.JSON_QUOTE:
                return self.parse_string()
            case _ if token.type == TokenType.JSON_OPEN_BRACE:
                return self.parse_object()
            case _ if token.type == TokenType.JSON_OPEN_BRACKET:
                return self.parse_array()
            case _:
                raise Exception('Unexpected character \'{}\' at index {}'.format(token.value, self.pointer))
    
    def parse_string(self):
        states = [
            {'quote': 1},
            {'quote': 2, 'string': 3},
            {},
            {'quote': 2}
        ]
        str_value = None
        
        current_state = 0
        while self.pointer < len(self.lexer.tokens):
            token: Token = self.lexer.tokens[self.pointer]
            
            if token.type == TokenType.JSON_QUOTE:
                group = 'quote'
            elif token.type == TokenType.JSON_STRING:
                group = 'string'
                str_value = token.value
            else:
                raise Exception('Unexpected character \'{}\' at index {}'.format(self.lexer.tokens[self.pointer], self.pointer))

            if group not in states[current_state]:
                raise Exception('Unexpected character \'{}\' at index {}'.format(self.lexer.tokens[self.pointer], self.pointer))

            current_state = states[current_state][group]
            
            # If we've reached the end state (state 2), stop processing
            if current_state == 2:
                break
                
            self.pointer += 1
        
        if current_state != 2:
            raise Exception('Unexpected character \'{}\' at index {}'.format(self.lexer.tokens[self.pointer], self.pointer))

        return str_value
    
input = '{"name":[[1E+27, false]]}'
parser = Parser(input)
print(parser.json)