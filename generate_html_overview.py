#!/usr/bin/env python3

import os
import json
import html
import re

def make_prop(id, s):
    return '\n'.join('<div><a href="/se-og-stoet-forslag/?Id=FT-{}">{}</a></div>'.format(id, line) for line in s.split('\n'))

basedir = os.path.dirname(__file__)

fnames = os.listdir(os.path.join(basedir, 'text'))
proposals = [make_prop(fn.split('.')[0], html.unescape(json.load(
             open(os.path.join(basedir, 'text', fn)))['title']))
             for fn in fnames]

header = open(os.path.join(basedir, 'templates', 'header.html')).read()
footer = open(os.path.join(basedir, 'templates', 'footer.html')).read()

with open(os.path.join(basedir, 'templates', 'forside.html')) as f:
    print(f.read().format(proposals='\n'.join(proposals),
                          header=header, footer=footer).rstrip())
