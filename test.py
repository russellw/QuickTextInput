import re
import unittest

from QuickTextInput import correct_line, last_word


class TestLastWord(unittest.TestCase):
    def test_basic_case(self):
        self.assertEqual(
            last_word("Hello world!"),
            "world",
            "Failed on a basic case with words and punctuation.",
        )

    def test_empty_string(self):
        self.assertEqual(last_word(""), "", "Failed on an empty string.")

    def test_only_punctuation(self):
        self.assertEqual(
            last_word("!@#$%^&*()"), "", "Failed on a string with only punctuation."
        )

    def test_single_word(self):
        self.assertEqual(
            last_word("Python"), "Python", "Failed on a string with a single word."
        )

    def test_trailing_non_alphanumeric(self):
        self.assertEqual(
            last_word("End."),
            "End",
            "Failed on a string with a trailing punctuation mark.",
        )

    def test_multiple_separators(self):
        self.assertEqual(
            last_word("word1, word2.word3!"),
            "word3",
            "Failed on a string with multiple non-alphanumeric separators.",
        )

    def test_numbers(self):
        self.assertEqual(
            last_word("123 456 789"), "789", "Failed on a string with numeric words."
        )

    def test_mixed_characters(self):
        self.assertEqual(
            last_word("hello123 world!"),
            "world",
            "Failed on a string with mixed alphanumeric characters.",
        )

    def test_leading_and_trailing_whitespace(self):
        self.assertEqual(
            last_word("   this is a test   "),
            "test",
            "Failed on a string with leading and trailing whitespace.",
        )

    def test_newlines_and_tabs(self):
        self.assertEqual(
            last_word("Line1\nLine2\tLine3"),
            "Line3",
            "Failed on a string with newlines and tabs.",
        )

    def test_non_alphanumeric_boundaries(self):
        self.assertEqual(
            last_word("-start middle,end."),
            "end",
            "Failed on a string with non-alphanumeric boundaries.",
        )

    def test_unicode_characters(self):
        self.assertEqual(
            last_word("¡Hola! ¿Cómo estás?"),
            "estás",
            "Failed on a string with Unicode characters.",
        )


class TestCorrectLine(unittest.TestCase):
    def test_basic_sentence(self):
        self.assertEqual(
            correct_line("hello world!this is a test."),
            "Hello world! This is a test.",
            "Failed on a basic sentence with no spaces after punctuation.",
        )

    def test_trailing_spaces(self):
        self.assertEqual(
            correct_line("This is a test.  "),
            "This is a test.",
            "Failed to remove trailing spaces.",
        )

    def test_multiple_spaces_between_words(self):
        self.assertEqual(
            correct_line("This  is   a test."),
            "This is a test.",
            "Failed to handle multiple spaces between words.",
        )

    def test_missing_space_after_punctuation(self):
        self.assertEqual(
            correct_line("Hello,world!How are you?"),
            "Hello, world! How are you?",
            "Failed to add space after punctuation.",
        )

    def test_capitalize_sentences(self):
        self.assertEqual(
            correct_line("this is a sentence. this is another one."),
            "This is a sentence. This is another one.",
            "Failed to capitalize the first letter of each sentence.",
        )

    def test_combination_of_issues(self):
        self.assertEqual(
            correct_line("this is,a test!another issue,here."),
            "This is, a test! Another issue, here.",
            "Failed on a sentence with multiple issues.",
        )

    def test_url_unchanged(self):
        self.assertEqual(
            correct_line("Visit https://example.com for more info."),
            "Visit https://example.com for more info.",
            "Failed to leave URLs unchanged.",
        )

    def test_no_punctuation(self):
        self.assertEqual(
            correct_line("this is a test without punctuation"),
            "This is a test without punctuation",
            "Failed to capitalize the first letter of a sentence without punctuation.",
        )

    def test_leading_whitespace(self):
        self.assertEqual(
            correct_line("   this is a test."),
            "This is a test.",
            "Failed to handle leading whitespace.",
        )

    def test_empty_string(self):
        self.assertEqual(correct_line(""), "", "Failed on an empty string.")

    def test_special_characters(self):
        self.assertEqual(
            correct_line("hello-world!test-case."),
            "Hello-world! Test-case.",
            "Failed on a sentence with special characters.",
        )


if __name__ == "__main__":
    unittest.main()
