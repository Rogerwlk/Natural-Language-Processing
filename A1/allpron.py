#!/usr/bin/env python3

import json, re
from collections import defaultdict
from nltk import word_tokenize
from nltk.corpus import cmudict # need to have downloaded the data through NLTK

""" Sample part of the output (hand-formatted):

{"lineId": "3-2", "lineNum": 2,
 "text": "Make my coat look new, dear, sew it!",
 "tokens": ["Make", "my", "coat", "look", "new", ",", "dear", ",", "sew", "it", "!"],
 "rhymeWords": ["sew", "it"],
 "rhymeProns": [["S OW1"], ["IH1 T", "IH0 T"]]
},
"""

# Load the cmudict entries into a data structure.
# Store each pronunciation as a STRING of phonemes (separated by spaces).
dict_data = cmudict.dict()
pron = {}
for w in dict_data:
    temp = []
    for way in range(len(dict_data[w])):
        temp.append(''.join(dict_data[w][way]))
    pron[w] = ' '.join(temp)

# Load chaos.json
with open('chaos.json') as json_data:
    data = json.load(json_data)

# For each line of the poem, add a "rhymeProns" entry
# which is a list parallel with "rhymeWords".
# For each word, it contains a list of possible pronunciations.
for stanza in data:
    for line in stanza['lines']:
        rhymeProns = []
        for rhyme in line['rhymeWords']:
            if (rhyme.lower() in pron):
                rhymeProns.append(pron[rhyme.lower()])
            else:
                rhymeProns.append(None)
        line['rhymeProns'] = rhymeProns

# Write the enhanced data to chaos.pron.json
with open('chaos.pron.json', 'w') as outfile:  
        json.dump(data, outfile, indent = 4)

"""
TODO: Answer the question:

- How many rhyme words are NOT found in cmudict (they are "out-of-vocabulary", or "OOV")?
Give some examples.
cat chaos.pron.json | grep null | wc -l
34 words not found in cmudict.
Example: ague, Terpsichore, topsails, reviles, similes, endeavoured, tortious, davit, breeches, gaol 
...
"""
