#!/usr/bin/env python3

"""
Converts chaos.html into JSON. A sample of the input:

<xxx1><p>Dearest <i>creature</i> in <i>creation</i><br>
<xxx2>Studying English <i>pronunciation</i>,<br>
<xxx3><tt>&nbsp;&nbsp;&nbsp;</tt>I will teach you in my <i>verse</i><br>
<xxx4><tt>&nbsp;&nbsp;&nbsp;</tt>Sounds like <i>corpse</i>, <i>corps</i>, <i>horse</i> and <i>worse</i>.</p>

A hand-formatted portion of the output (note that indentation, line breaks,
order of dict entries, etc. don't matter as long as the data matches):

[
    ...
    {"stanza": 3,
     "lines": [
          {"lineId": "3-1", "lineNum": 1, "text": "Pray, console your loving poet,",
           "tokens": ["Pray", ",", "console", "your", "loving", "poet"],
           "rhymeWords": ["poet"]},
          {"lineId": "3-2", "lineNum": 2, "text": "Make my coat look new, dear, sew it!",
           "tokens": ["Make", "my", "coat", "look", "new", ",", "dear", ",", "sew", "it", "!"],
           "rhymeWords": ["sew", "it"]},
          ...
     ]},
    ...
    {"stanza": 9,
     "lines": [
          {"lineId": "9-1", "lineNum": 1, "text": "From \"desire\": desirable - admirable from \"admire\",",
           "tokens": ["From", "``", "desire", "''", ":", "desirable", "-", "admirable", "from", "``", "admire", "''", ","],
           "rhymeWords": ["admire"]},
          ...
     ]},
     ...
]
"""

import json, re
from nltk import word_tokenize

def isword(token):
    for ch in token:
        if (not ch.isalpha()):
            return (False)
    return (True)# TODO: whether any character in the token is a letter

# regex that breaks an HTML line into parts: line number within the stanza, main portion, spacing
NUM_TAG_RE = re.compile(r'^<xxx\d+>')# TODO:
MAIN_RE = re.compile(r'</?\w+>')
ITALIC_RE = re.compile(r'<i>[\s\w]+</i>')

# TODO: read from chaos.html, construct data structure, write to chaos.json
if __name__ == "__main__":
    file_html = open('chaos.html','r')

    # omit first 17 lines
    for i in range(17):
        file_html.readline()

    # initialize data
    data = []
    data_stanza = {}

    # read first line
    line = file_html.readline()
    num = NUM_TAG_RE.search(line)
    stanza = 0
    
    # check if the line is valid
    while (line != "" and num != None):
        # line number
        num = int(re.search('\d', num.group(0)).group(0))
        
        # create stanza dict
        if (num == 1):
            stanza += 1
            # append created data_stanza
            if (data_stanza):
                data.append(data_stanza)
            data_stanza = {}
            data_stanza["stanza"] = stanza
            data_stanza["lines"] = []
        
        # main texts
        main = MAIN_RE.split(line)
        if ('&nbsp;&nbsp;&nbsp;' in main):
            main.remove('&nbsp;&nbsp;&nbsp;')
        main = ''.join(main)
        
        # tokens
        tokens = main.replace('-', ' - ')
        tokens = word_tokenize(tokens)
        
        # italics (used for finding rhymes)
        italics = ITALIC_RE.findall(line)
        
        # cut out <i> and </i>
        for i in range(len(italics)):
            italics[i] = italics[i][3:-4]
        italics = ' '.join(italics)
        italics = italics.split()
        print (italics)
        print (tokens)
        
        # rhymes (comparing reversed token with rhymes)
        rhymes = []
        flag = True
        for i in reversed(range(len(tokens))):
            if (isword(tokens[i])):
                if (tokens[i] in italics and tokens[i - 1] in italics
                    and isword(tokens[i - 1])):
                    rhymes.append(tokens[i - 1])
                if (isword(tokens[i])):
                    rhymes.append(tokens[i])
                break
        
        # create line_dict
        data_line = {}
        data_line["lineId"] = (str(stanza) + '-' + str(num))
        data_line["lineNum"] = num
        data_line["text"] = main
        data_line["tokens"] = tokens
        data_line["rhymeWords"] = rhymes
        data_stanza["lines"].append(data_line)
        
        # read next line
        line = file_html.readline()
        num = NUM_TAG_RE.search(line)
    else:
        # append the last one
        if (data_stanza):
            data.append(data_stanza)
    # dump into chaos.json
    with open('chaos.json', 'w') as outfile:  
        json.dump(data, outfile, indent = 4)
    file_html.close()