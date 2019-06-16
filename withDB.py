from pymongo import MongoClient
import json
import unittest
import time

### Populate database from file ###

#file_content = []

#with open("words.txt", 'r') as f:
#    for line in f:
#        word = line.strip()
#        file_content.append({'word': word})
#
#db.anagrams.insert_many(file_content)

class Anagrams:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.words_database

    def get_anagrams_db(self, word):
        if type(word) == str:
            letters = list(word)
            matches = []

            regex = '^'

            for letter in letters:
                regex += '(?!.*%s.*%s)' % (letter, letter)
            regex += '[%s]{%s}$' % (word, len(word))

            result = self.db.anagrams.find({'word': { '$regex': regex }})
            for res in result:
                matches.append(res['word'])

            return matches
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

    def test_anagrams_db(self):
        anagrams = Anagrams()
        self.assertEqual(anagrams.get_anagrams_db('eat'), ['ate', 'eat', 'tea'])
        self.assertEqual(anagrams.get_anagrams_db('ababa'), [])
        self.assertEqual(anagrams.get_anagrams_db('adfqerefq'), [])
        self.assertRaises(TypeError, anagrams.get_anagrams_db, 777, msg='word must be a string')
        self.assertEqual(anagrams.get_anagrams_db('plates'), ['palest', 'pastel', 'petals', 'plates', 'staple'])

if __name__ == '__main__':
    unittest.main()
