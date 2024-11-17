import unittest
from parser import Parser

class TestJsonParser(unittest.TestCase):

    def test_object_str_key(self):
        string = '{"name": "John"}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"name": "John"})

    def test_object_num_key(self):
        string = '{"1": "value"}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"1": "value"})

    def test_object_multiple_pairs(self):
        string = '{"name": "John", "age": 30}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"name": "John", "age": 30})

    def test_array_basic(self):
        string = '[1, 2, 3]'
        parser = Parser(string)
        self.assertListEqual(parser.json, [1, 2, 3])

    def test_array_with_mixed_types(self):
        string = '[1, "hello", true, null]'
        parser = Parser(string)
        self.assertListEqual(parser.json, [1, "hello", True, None])

    def test_nested_objects(self):
        string = '{"person": {"name": "John", "age": 30}}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"person": {"name": "John", "age": 30}})

    def test_nested_arrays(self):
        string = '[1, [2, 3], 4]'
        parser = Parser(string)
        self.assertListEqual(parser.json, [1, [2, 3], 4])

    def test_object_with_empty_string(self):
        string = '{"name": ""}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"name": ""})

    def test_empty_object(self):
        string = '{}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {})

    def test_empty_array(self):
        string = '[]'
        parser = Parser(string)
        self.assertListEqual(parser.json, [])

    def test_boolean_true(self):
        string = '{"flag": true}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"flag": True})

    def test_boolean_false(self):
        string = '{"flag": false}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"flag": False})

    def test_null_value(self):
        string = '{"key": null}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"key": None})

    def test_object_with_whitespace(self):
        string = '  {"name": "John"}  '
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"name": "John"})

    def test_array_with_whitespace(self):
        string = '  [1, 2, 3]  '
        parser = Parser(string)
        self.assertListEqual(parser.json, [1, 2, 3])

    def test_missing_closing_brace(self):
        string = '{"name": "John"'
        with self.assertRaises(Exception):
            Parser(string)

    def test_missing_closing_bracket(self):
        string = '[1, 2, 3'
        with self.assertRaises(Exception):
            Parser(string)

    def test_unexpected_character(self):
        string = '{"name": "John" & "age": 30}'
        with self.assertRaises(Exception):
            Parser(string)

    def test_extra_comma_in_object(self):
        string = '{"name": "John",}'
        with self.assertRaises(Exception):
            Parser(string)

    def test_extra_comma_in_array(self):
        string = '[1, 2, 3,]'
        with self.assertRaises(Exception):
            Parser(string)

    def test_number(self):
        string = '{"age": 30}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"age": 30})

    def test_float(self):
        string = '{"height": 5.9}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"height": 5.9})

    def test_exponential_notation(self):
        string = '{"value": 1e2}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"value": 100})

    def test_exponential_negative(self):
        string = '{"value": 1e-2}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"value": 0.01})

    def test_large_number(self):
        string = '{"large": 10000000000000000}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"large": 10000000000000000})

    def test_number_in_array(self):
        string = '[10, 20, 30]'
        parser = Parser(string)
        self.assertListEqual(parser.json, [10, 20, 30])

    def test_mixed_data_in_array(self):
        string = '[1, "hello", false, null]'
        parser = Parser(string)
        self.assertListEqual(parser.json, [1, "hello", False, None])

    def test_object_with_boolean_value(self):
        string = '{"flag": true}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"flag": True})

    def test_object_with_null_value(self):
        string = '{"flag": null}'
        parser = Parser(string)
        self.assertDictEqual(parser.json, {"flag": None})

if __name__ == '__main__':
    unittest.main()