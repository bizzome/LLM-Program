# Realizar testes para as funções do arquivo tools.py
import unittest
from chatbot.tools import wikipedia, google_search, calculate


class TestTools(unittest.TestCase):
    # teste para a função wikipedia
    def test_wikipedia(self):
        self.assertEqual(
            wikipedia("Python"),
            (
                "Python is an interpreted high-level general-purpose"
                "programming language."
            ),
        )

    # teste para a função google_search
    def test_google_search(self):
        self.assertEqual(
            google_search("Python")[0].title, "Welcome to Python.org"
        )
        self.assertEqual(
            google_search("Python")[0].description,
            "The official home of the Python Programming Language.",
        )

    # teste para a função calculate
    def test_calculate(self):
        self.assertEqual(calculate("2+2"), 4)


if __name__ == "__main__":
    unittest.main()
