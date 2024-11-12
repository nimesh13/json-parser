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
            {'minus': 1, 'zero': 2, 'digits_1_to_9': 3},
            {'zero': 2, 'digits_1_to_9': 3},
            {'dot': 5},
            {'digits_0_to_9': 4, 'dot': 5},
            {'digits_0_to_9': 4, 'dot': 5},
            {'digits_0_to_9': 6},
            {'digits_0_to_9': 6, 'exponent': 7},
            {'sign': 8, 'digits_0_to_9': 9},
            {'digits_0_to_9': 9},
            {'digits_0_to_9': 9}
        ]

        current_state = 0

        while i < length:
            char = str[i]

            if current_state == 0:
                if char == '0':
                    group = 'zero'
                elif char in '123456789':
                    group = 'digits_1_to_9'
                else:
                    raise Exception(f"Unexpected character '{char}' at index {i} for starting a number")
            else:
                if char in '0123456789':
                    group = 'digits_0_to_9'
                elif char == '-':
                    group = 'minus'
                elif char in '+-':
                    group = 'sign'
                elif char in 'eE':
                    group = 'exponent'
                elif char == '.':
                    group = 'dot'
                else:
                    break
            
            if group not in states[current_state]:
                raise Exception('Unexpected character \'{}\' at index {}'.format(str[i], i))

            current_state = states[current_state][group]
            int_tokens.append(char)
            i += 1
        
        if current_state not in [4, 6, 9]:
            raise Exception('Unexpected character \'{}\' at index {}'.format(str[i], i))

        return ''.join(int_tokens), i



token = Token()
input = '{"name": "nimesh", "age": 123}'
token.lex(input)
print(token.tokens)