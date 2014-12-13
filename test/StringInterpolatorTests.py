import unittest
from lib.StringInterpolator import interpolate_string


class MoccaStringInterpolatorTests(unittest.TestCase):
    def test_interpolates_single_variable(self):
        environment = {'name': 'Bob'}
        text_to_interpolate = "Hello {{name}}"
        expected_result = "Hello Bob"

        self.assertEqual(expected_result, interpolate_string(text_to_interpolate, environment))

    def test_interpolates_multiple_occurrences_of_a_single_variable(self):
        environment = {'name': 'Bob'}
        text_to_interpolate = "Hello {{name}} {{name}}"
        expected_result = "Hello Bob Bob"

        self.assertEqual(expected_result, interpolate_string(text_to_interpolate, environment))

    def test_interpolates_single_occurrences_of_multiple_variables(self):
        environment = {'name': 'Bob', 'last_name': 'da Bobby'}
        text_to_interpolate = "Hello {{name}} {{last_name}}"
        expected_result = "Hello Bob da Bobby"

        self.assertEqual(expected_result, interpolate_string(text_to_interpolate, environment))

    def test_interpolates_multiple_occurrences_of_multiple_variables(self):
        environment = {'name': 'Bob', 'last_name': 'da Bobby'}
        text_to_interpolate = "Hello {{name}} {{last_name}} {{name}} {{last_name}}"
        expected_result = "Hello Bob da Bobby Bob da Bobby"

        self.assertEqual(expected_result, interpolate_string(text_to_interpolate, environment))
