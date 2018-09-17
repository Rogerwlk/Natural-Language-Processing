#!/usr/bin/env python3

import json, re
from collections import defaultdict
from nltk.corpus import cmudict # need to have downloaded the data through NLTK

def isExactRhyme(p1, p2):
    """
    TODO: Explain your heuristic here.
    Split the pronunciations into 1-2 letter parts.
    If any parts match, these two words rhyme.
    """
    way1 = re.findall(r'[A-Z]{1,2}', p1)
    way2 = re.findall(r'[A-Z]{1,2}', p2)
    print (way1) # comment this line for question 2
    print (way2) # comment this line for question 2
    for w1 in way1:
        for w2 in way2:
            if (w1 == w2):
                return True
    return False # TODO: whether pronunciations p1 and p2 rhyme

# Load chaos.pron.json
with open('chaos.pron.json') as json_data:
    data = json.load(json_data)

# For each pair of lines that are supposed to rhyme,
# check whether there are any pronunciations of the words that
# make them rhyme according to cmudict and your heuristic.
# Print the rhyme words with their pronunciations and whether
# they are deemed to rhyme or not
# so you can examine the effects of your rhyme detector.
# Count how many pairs are deemed to rhyme vs. not.
for stanza in data:
    for i, line in enumerate(stanza['lines']):
        if (i % 2 == 0):
            print ('-' * 5,
                   'line pair separator',
                   '-' * 5)
            prev_line = line
            continue
        line_match = True
        for x, prev_rhy in enumerate(prev_line['rhymeProns']):
            for y, rhy in enumerate(line['rhymeProns']):
                print (prev_line['rhymeWords'][x] + ':', prev_rhy)
                print (line['rhymeWords'][y] + ':', rhy)
                word_match = False
                if (prev_rhy != None and rhy != None):
                    for prev_pron in prev_rhy.split():
                        for pron in rhy.split():
                            if (isExactRhyme(prev_pron, pron)):
                                word_match = True
                                break # comment this line for question 2
                            
#                                 print ("Good Rhyme!!!", end="") # uncomment this line for question 2
#                             else: # uncomment this line for question 2
#                                 print ("Bad Rhyme!!!", end="") # uncomment this line for question 2
#                 print() # uncomment this line for question 2

                        if (word_match): # comment this line for question 2
                            break # comment this line for question 2
                if (word_match): # comment this line for question 2
                    print ("Good Rhyme!!!\n") # comment this line for question 2
                else: # comment this line for question 2
                    line_match = False # comment this line for question 2
                    print ("Bad Rhyme!!!\n") # comment this line for question 2
        if (line_match):
            print ("Line Pair Match!")
        else:
            print ("Line Pair Mismatch!")

"""
TODO: Answer the questions briefly:

- How many pairs of lines that are supposed to rhyme actually have rhyming pronunciations
according to your heuristic and cmudict?

Change output format into one line and run command below:
python exact_rhymes.py | grep "None" | wc -l
29

- For how many lines does having the rhyming line help you disambiguate
between multiple possible pronunciations?

Change the logic of the code. Judge every possible pair of pronunciation
and print "Good" "Bad" for each rhyme check. Print them in one line.
Run command below:
python exact_rhymes.py | grep "Good" | grep "Bad" | wc -l
There must be at least one "Good" and one "Bad" for each pair of words.
13

- What are some reasons that lines supposed to rhyme do not,
according to your rhyme detector? Give examples.

The most bad rhymes are caused by missing data.
Ex:
    vapour: None
    newspaper: NUW1ZPEY2PER0
    
The rest bad rhymes are mainly bad partition of pronunciations.
Ex:
    jerk: JHER1K
    cork: KAO1RK
    ['JH', 'ER', 'K']
    ['KA', 'O', 'RK']
    Bad Rhyme!!!
--------------------------------
    ever: EH1VER0
    Neither: NIY1DHER0 NAY1DHER0
    ['EH', 'VE', 'R']
    ['NI', 'Y', 'DH', 'ER']
    ['EH', 'VE', 'R']
    ['NA', 'Y', 'DH', 'ER']
    Bad Rhyme!!!
--------------------------------
    ally: AE1LAY0 AH0LAY1
    aye: AY1
    ['AE', 'LA', 'Y']
    ['AY']
    ['AH', 'LA', 'Y']
    ['AY']
    Bad Rhyme!!!
    
"""
