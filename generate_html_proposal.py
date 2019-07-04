#!/usr/bin/env python3

import sys
import os
import json
import html
import re

def make_paragraphs(s):
    return '\n'.join('<p>{}</p>'.format(line) for line in s.split('\n'))

id = sys.argv[1]
basedir = os.path.dirname(__file__)
with open(os.path.join(basedir, 'text', id + '.json')) as f:
    data = json.load(f)

header = open(os.path.join(basedir, 'templates', 'header.html')).read()
footer = open(os.path.join(basedir, 'templates', 'footer.html')).read()

with open(os.path.join(basedir, 'templates', 'side.html')) as f:
    html = f.read().format(title=html.escape(data['title']), id=id,
                           teaser=make_paragraphs(html.escape(data['teaser'])),
                           body=make_paragraphs(html.escape(data['body'])),
                           header=header, footer=footer)
os.makedirs('html', exist_ok=True)
with open(os.path.join(basedir, 'html', id + '.html'), 'w') as f:
    f.write(html)
