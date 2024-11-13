from collections import deque

class Token:
    def __init__(self):
        self.tokens = []
    
    def lex(self, input):
        i = 0
        length = len(input)

        while i < length:
            char = input[i]

            if char in '{}[]:,':
                self.tokens.append(char)
            elif char == '"':
                str_token, index = self.get_string(input, i)
                self.tokens.append(str_token)
                i = index
                continue
            elif char in '-0123456789':
                num_token, index = self.get_number(input, i)
                self.tokens.append(num_token)
                i = index
                continue
            elif char == 'n' and i + 4 < length and input[i: i + 4] == 'null':
                self.tokens.append(None)
                i += 4
                continue
            elif char == 't' and i + 4 < length and input[i: i + 4] == 'true':
                self.tokens.append(True)
                i += 4
                continue
            elif char == 'f' and i + 5 < length and input[i: i + 5] == 'false':
                self.tokens.append(False)
                i += 5
                continue
            elif char == ' ':
                pass
            else:
                print(self.tokens)
                raise Exception('Unexpected character \'{}\' at index {}'.format(char, i))

            i += 1

    def get_string(self, str, i):
        length = len(str)
        str_tokens = deque()

        # Starting character is opening quote. Move forward.
        i += 1

        while i < length and str[i] != '"':
            str_tokens.append(str[i])
            i += 1

        if i == length or str[i] != '"':
            raise Exception('Missing end quote.')
        
        # End character is closing quote. Move forward.
        i += 1

        return ''.join(str_tokens), i

    def get_number(self, str, i):
        length = len(str)
        int_tokens = deque()
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

        while i < length:
            char = str[i]

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
                elif char == '.':
                    group = 'dot'
                else:
                    break
            
            if group not in states[current_state]:
                raise Exception(f"Unexpected character '{char}' at index {i}")

            current_state = states[current_state][group]
            int_tokens.append(char)
            i += 1
        
        if current_state not in [4, 7, 9]:
            raise Exception('Unexpected character \'{}\' at index {}'.format(str[i], i))

        return ''.join(int_tokens), i

token = Token()
input = '{"name": "nimesh", "age": 123, "high": tru }'
token.lex(input)
print(token.tokens)