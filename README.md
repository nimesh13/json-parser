# json-parser

A simple application that mimics a json parser. It inputs a stringify-ed json and returns a json object or array OR throw out an error highlighting what's wrong.

I wrote it to understand how lexers and parsers work.

This implements a lot of [DFAs](https://en.wikipedia.org/wiki/Deterministic_finite_automaton). Felt pretty nice trying to draw all possible states and transitions.

Currently this only has a Python support. I want to try this out in other languages as well like Golang, JavaScript, etc.

### Usage

```python
input_string = '{"name": "John Doe"}'
parser = Parser(input_string)
print(parser.json)

# Output:
# {'name': 'John Doe'}
```

### Testing

Wrote a wide range of tests to test success and error scenarios. Run them by:

```bash
python3 -m unittest unittests.py
```

### TODO:

1. Parse special characters in string.
2. `json-parse` in more languages.
3. Will also upload the DFA drawings from my notebook.

### References

Of course this was not possible without resources online. Had a bunch of help:

1. A guy's blog [post](https://notes.eatonphil.com/writing-a-simple-json-parser.html)
2. json.org documentation. Tbh [this](https://www.json.org/json-en.html) site has all the diagrams that highlights the DFAs for all tokens. Converting it to python was the challenge.
3. Following up from the previous point, [Valid Number](https://leetcode.com/problems/valid-number/) on [leetcode](https://leetcode.com/) is how I learned to implement DFAs LOL. God bless the editorial author(s)!
4. Can you do anything without chatgpt now?
