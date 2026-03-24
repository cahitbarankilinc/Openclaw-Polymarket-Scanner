import unittest
from src.string_utils import analyze_text


class AnalyzeTextTests(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(analyze_text(""), {
            "word_count": 0,
            "unique_word_count": 0,
            "longest_word": "",
            "average_word_length": 0.0,
        })

    def test_basic_sentence(self):
        self.assertEqual(analyze_text("Hello world from OpenClaw"), {
            "word_count": 4,
            "unique_word_count": 4,
            "longest_word": "OpenClaw",
            "average_word_length": 6.0,
        })

    def test_case_insensitive_uniques_and_punctuation(self):
        self.assertEqual(analyze_text("Hello, hello! HELLO? world..."), {
            "word_count": 4,
            "unique_word_count": 2,
            "longest_word": "Hello",
            "average_word_length": 5.0,
        })

    def test_hyphenated_words_stay_together(self):
        self.assertEqual(analyze_text("state-of-the-art tools are useful"), {
            "word_count": 4,
            "unique_word_count": 4,
            "longest_word": "state-of-the-art",
            "average_word_length": 7.5,
        })

    def test_first_longest_word_wins_tie(self):
        self.assertEqual(analyze_text("alpha bravo charlie delta"), {
            "word_count": 4,
            "unique_word_count": 4,
            "longest_word": "charlie",
            "average_word_length": 5.5,
        })


if __name__ == "__main__":
    unittest.main()
