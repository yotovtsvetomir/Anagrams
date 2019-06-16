# Given a words.txt file containing a newline-delimited list of dictionary
# words, please implement the Anagrams class so that the get_anagrams() method
# returns all anagrams from words.txt for a given word.
#
# Requirements:
#   - Optimise the code for fast retrieval
#   - Thread Safe implementation
#   - Write more tests

####### Implementation #######
### I have tried several different approaches and also I was curious what works best.
### Hope you like my code :)

####### Conclusion #######
### It is cool idea to create a file or separate table(database) with the actual results in such cases,
### because the actual set that has anagrams is small and will significantly reduce retrieval times.

### As in all cases in programming it depends on the problem. I would say that solving and breaking
### the problem into steps is much more important and difficult than writing the actual code.

import unittest
import itertools
import re
import time
import json

class Anagrams:
    def __init__(self):
        words = open('words.txt', 'r')
        self.dictionary = words.read().splitlines()
        words.close()

    def get_anagrams_regex(self, word):
        if type(word) == str:
            letters = list(word)
            matches = []
            regex = '^'

            for letter in letters:
                regex += '(?!.*%s.*%s)' % (letter, letter)
            regex += '[%s]{%s}$' % (word, len(word))

            pattern = re.compile(regex, re.IGNORECASE)
            matches = list(filter(pattern.search, self.dictionary))

            return matches
        else:
            raise TypeError("word must be a string")

    def get_anagrams_loop(self, word):
        if type(word) == str:
            letters = list(word)
            matches = []

            for line in self.dictionary:
                if len(line) == len(letters) and len(set(line)) == len(line) and all(elem in letters for elem in line):
                    matches.append(''.join(line))

            return matches
        else:
            raise TypeError("word must be a string")

    def get_anagrams_comprehension(self, word):
        if type(word) == str:
            letters = list(word)

            matches = [line for line in self.dictionary if len(line) == len(letters) and len(set(line)) == len(line) and all(elem in letters for elem in line)]
            return matches
        else:
            raise TypeError("word must be a string")

    def get_anagrams_filter(self, word):
        if type(word) == str:
            letters = list(word)
            matches = []

            def anagrams_filter(line):
                if len(line) == len(letters) and len(set(line)) == len(line) and all(elem in letters for elem in line):
                    return True

            matches = list(filter(anagrams_filter , self.dictionary))
            return matches
        else:
            raise TypeError("word must be a string")

class Anagrams2:
    def __init__(self):
        anagrams = open('anagrams.txt')
        self.dictionary = json.load(anagrams)
        anagrams.close()

    def get_anagrams_fromfile(self, word):
        if type(word) == str:
            try:
                return self.dictionary[word]
            except KeyError:
                return []
        else:
            raise TypeError("word must be a string")

class TestAnagrams(unittest.TestCase):
    def setUp(self):
        self._started_at = time.time()
        self.speed = {}

    def tearDown(self):
        elapsed = time.time() - self._started_at
        self.speed[self] = str(round(elapsed, 4)) + "s"
        print(self.speed)

    def test_anagrams_regex(self):
        anagrams = Anagrams()
        self.assertEqual(anagrams.get_anagrams_regex('eat'), ['ate', 'eat', 'tea'])
        self.assertEqual(anagrams.get_anagrams_regex('ababa'), [])
        self.assertEqual(anagrams.get_anagrams_regex('adfqerefq'), [])
        self.assertRaises(TypeError, anagrams.get_anagrams_regex, 777, msg='word must be a string')
        self.assertEqual(anagrams.get_anagrams_regex('plates'), ['palest', 'pastel', 'petals', 'plates', 'staple'])

    def test_anagrams_loop(self):
        anagrams = Anagrams()
        self.assertEqual(anagrams.get_anagrams_loop('eat'), ['ate', 'eat', 'tea'])
        self.assertEqual(anagrams.get_anagrams_loop('ababa'), [])
        self.assertEqual(anagrams.get_anagrams_loop('adfqerefq'), [])
        self.assertRaises(TypeError, anagrams.get_anagrams_loop, 777, msg='word must be a string')
        self.assertEqual(anagrams.get_anagrams_loop('plates'), ['palest', 'pastel', 'petals', 'plates', 'staple'])

    def test_anagrams_comprehension(self):
        anagrams = Anagrams()
        self.assertEqual(anagrams.get_anagrams_comprehension('eat'), ['ate', 'eat', 'tea'])
        self.assertEqual(anagrams.get_anagrams_comprehension('ababa'), [])
        self.assertEqual(anagrams.get_anagrams_comprehension('adfqerefq'), [])
        self.assertRaises(TypeError, anagrams.get_anagrams_comprehension, 777, msg='word must be a string')
        self.assertEqual(anagrams.get_anagrams_comprehension('plates'), ['palest', 'pastel', 'petals', 'plates', 'staple'])

    def test_anagrams_filter(self):
        anagrams = Anagrams()
        self.assertEqual(anagrams.get_anagrams_filter('eat'), ['ate', 'eat', 'tea'])
        self.assertEqual(anagrams.get_anagrams_filter('ababa'), [])
        self.assertEqual(anagrams.get_anagrams_filter('adfqerefq'), [])
        self.assertRaises(TypeError, anagrams.get_anagrams_filter, 777, msg='word must be a string')
        self.assertEqual(anagrams.get_anagrams_filter('plates'), ['palest', 'pastel', 'petals', 'plates', 'staple'])

    def test_anagrams_fromfile(self):
        anagrams = Anagrams2()
        self.assertEqual(anagrams.get_anagrams_fromfile('eat'), ['ate', 'eat', 'tea'])
        self.assertEqual(anagrams.get_anagrams_fromfile('ababa'), [])
        self.assertEqual(anagrams.get_anagrams_fromfile('adfqerefq'), [])
        self.assertRaises(TypeError, anagrams.get_anagrams_fromfile, 777, msg='word must be a string')
        self.assertEqual(anagrams.get_anagrams_fromfile('plates'), ['palest', 'pastel', 'petals', 'plates', 'staple'])

if __name__ == '__main__':
    unittest.main()
