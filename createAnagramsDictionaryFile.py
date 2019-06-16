### Creating a file with all existing anagrams within our dictionary ###
import json

file = open('words.txt', 'r')
words = file.read().splitlines()
file.close()
dictionary = {}

def get_anagrams_comprehension(word):
    letters = list(word)
    matches = [line for line in words if len(line) == len(letters) and len(set(line)) == len(line) and all(elem in letters for elem in line)]
    return matches

for line in words:
    anags = get_anagrams_comprehension(line)
    if anags != [] and len(anags) > 1:
        dictionary[line] = anags

with open('anagrams.txt', 'w') as file:
     file.write(json.dumps(dictionary))
