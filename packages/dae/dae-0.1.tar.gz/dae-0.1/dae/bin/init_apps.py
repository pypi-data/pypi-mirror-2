#! /usr/bin/env python
import os

os.makedirs('apps')
os.makedirs('sessions')
with open('apps/__init__.py', 'wt') as f:
    f.write('')
