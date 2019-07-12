#!/usr/bin/env python3

'''
Generate text.
'''

import sys
import os.path
import re
import random
import urllib.request
import json
import collections

from pyquery import PyQuery as pq

# 0. Ubestemt ental, fælleskøn
# 1. Ubestemt ental, intetkøn
# 2. Bestemt ental
# 3. Ubestemt flertal
# 4. Bestemt flertal
replacement_nouns = [
    ('burger', None, 'burgeren', 'burgere', 'burgerne'),
    ('tomatskive', None, 'tomatskiven', 'tomatskiver', 'tomatskiverne'),
    (None, None, None, 'ristede løg', 'de ristede løg'),
    ('bøf', None, 'bøffen', 'bøffer', 'bøfferne'),
    ('bolle', None, 'bollen', 'boller', 'bollerne'),
    ('syltet agurk', None, 'den syltede agurk', 'syltede agurker', 'de syltede agurker'),
    ('osteskive', None, 'osteskiven', 'osteskiver', 'osteskiverne'),
    ('baconskive', None, 'baconskiven', 'baconskiver', 'baconskiverne'),
    ('vegetarbøf', None, 'vegetarbøffen', 'vegetarbøffer', 'vegetarbøfferne'),
    (None, None, 'mayonnaisen', None, None),
    (None, None, 'ketchuppen', None, None),
    (None, None, 'remouladen', None, None),
    ('pomfrit', None, 'pomfritten', 'pomfritter', 'pomfritterne'),
    ('løgring', None, 'løgringen', 'løgringe', 'løgringene'),
    ('salatskive', None, 'salatskiven', 'salatskiver', 'salatskiverne'),
    ('champignon', None, 'champignonen', 'champignoner', 'champignonerne'),
    (None, None, 'sennepen', None, None),
    (None, None, 'guacamolen', None, None),
    ('röstibolle', None, 'röstibollen', 'röstiboller', 'röstibollerne'),
    (None, None, None, 'syltede rødbeder', 'de syltede rødbeder'),
    (None, 'Happy Meal', None, 'Happy Meals', None),
    (None, None, None, 'nuggets', None),
    ('Whopper', None, 'Whopperen', 'Whoppers', None),
    ('pickle', None, None, 'pickles', None),
    (None, 'løg', 'løget', 'løg', 'løgene'),
    ('salat', None, 'salaten', 'salater', 'salaterne'),
    (None, 'salatblad', 'salatbladet', 'salatblade', 'salatbladene'),
    ('Big Mac', None, None, 'Big Macs', None),
    ('nummer 21', None, None, 'nummer 21', None),
    ('cheeseburger', None, 'cheeseburgeren', 'cheeseburgere', 'cheeseburgerne'),
    ('sesambolle', None, 'sesambollen', 'sesamboller', 'sesambollerne'),
    ('briochebolle', None, 'briochebollen', 'briocheboller', 'briochebollerne'),
    (None, None, 'den hemmelige dressing', None, None),
]

# 0. Ental, fælleskøn
# 1. Ental, intetkøn
# 2. Flertal/bestemthed
replacement_adjectives = [
    ('sjasket', 'sjasket', 'sjaskede'),
    ('well-done', 'well-done', 'well-done'),
    ('optøet', 'optøet', 'optøede'),
    ('friturestegt', 'friturestegt', 'friturestegte'),
    ('hjemmelavet', 'hjemmelavet', 'hjemmelavede'),
    ('gennemstegt', 'gennemstegt', 'gennemstegte'),
    ('saltet', 'saltet', 'saltede'),
]

replacement_nouns_kind = []
for i in range(5):
    ws = []
    for r in replacement_nouns:
        if r[i] is not None:
            ws.append(r[i])
    replacement_nouns_kind.append(ws)

replacement_adjectives_kind = []
for i in range(3):
    ws = []
    for r in replacement_adjectives:
        if r[i] is not None:
            ws.append(r[i])
    replacement_adjectives_kind.append(ws)

_basedir = os.path.dirname(__file__)

# Regarding the nouns and adjectives files: They contain all *unique*
# words.  For example, 'helt' is not present in any of the files,
# since it can both be a noun and an adjective.
def load_nouns():
    kinds = [
        ['navneord-ubestemt_ental-fælleskøn'],
        ['navneord-ubestemt_ental-intetkøn'],
        ['navneord-bestemt_ental-fælleskøn',
         'navneord-bestemt_ental-intetkøn'],
        ['navneord-ubestemt_flertal-fælleskøn',
         'navneord-ubestemt_flertal-intetkøn',
         'navneord_flertal-ubestemt'],
        ['navneord-bestemt_flertal-fælleskøn',
         'navneord-bestemt_flertal-intetkøn',
         'navneord_flertal-bestemt'],
    ]
    nouns = []
    for filenames in kinds:
        kind_nouns = []
        for name in filenames:
            with open(os.path.join(_basedir, 'words', 'navneord', name)) as f:
                kind_nouns.extend(f.read().strip().split('\n'))
        nouns.append(set(kind_nouns))
    return nouns

def load_adjectives():
    kinds = [
        ['tillægsord-fælleskøn'],
        ['tillægsord-intetkøn'],
        ['tillægsord-generisk'],
    ]
    adjectives = []
    for filenames in kinds:
        kind_adjectives = []
        for name in filenames:
            with open(os.path.join(_basedir, 'words', 'tillægsord', name)) as f:
                kind_adjectives.extend(f.read().strip().split('\n'))
        adjectives.append(set(kind_adjectives))
    return adjectives

nouns = load_nouns()
adjectives = load_adjectives()

def find_words(s):
    return list(collections.Counter(re.findall(r'\w+', s.lower())).items())

def fix_case(orig, new):
    if all(c.isupper() for c in orig):
        return new.upper()
    elif len(orig) >= 1 and orig[0].isupper():
        return new[:1].upper() + new[1:]
    else:
        return new

def fix_word(word):
    # Check if unique.
    found = False
    for ng in nouns:
        if word in ng:
            if found:
                return
            found = True
    for ag in adjectives:
        if word in ag:
            if found:
                return
            found = True

    # Find replacement.
    for i in range(len(nouns)):
        if word in nouns[i]:
            replacements = replacement_nouns_kind[i]
            if replacements:
                word_fixed = random.choice(replacements)
                replacements.remove(word_fixed)
                return word_fixed
    for i in range(len(adjectives)):
        if word in adjectives[i]:
            replacements = replacement_adjectives_kind[i]
            if replacements:
                word_fixed = random.choice(replacements)
                replacements.remove(word_fixed)
                return word_fixed

def fix(conv, s):
    def fix_word_conv(w):
        try:
            w_fixed = conv[w.lower()]
            return fix_case(w, w_fixed)
        except KeyError:
            return w
    return re.sub(r'\w+', lambda m: fix_word_conv(m.group(0)), s)

url = sys.argv[1]

with urllib.request.urlopen(url) as f:
    html = f.read()

d = pq(html)

script = pq(list(d('script[data-module="ProposalEditor"]'))[0]).text()
data = json.loads(script[script.find('{'):script.rfind('}')+1])
proposal = data['props']['proposalCreationViewModel']['proposal']
title = proposal['title']
teaser = proposal['proposalContent']
body = proposal['remarks']

# Prioritize replacing words that are most used.
words = find_words(title + ' ' + teaser + ' ' + body)
random.shuffle(words)
words.sort(key=lambda t: t[1], reverse=True)

conv = {}
for w, _ in words:
    fixed = fix_word(w)
    if fixed:
        conv[w] = fixed

print(json.dumps({
    'title': fix(conv, title.replace('\n', ' ')),
    'teaser': fix(conv, teaser),
    'body': fix(conv, body)
}, sort_keys=True, indent=2, ensure_ascii=False))
