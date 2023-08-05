#!/usr/bin/python

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))

from stopam.client import Service

with Service('b42aac0441104e858b996d1c7711fcaa', fallback=False, port=81) as c:
    q = c.ask()
    answer = raw_input(q.question) # How much is 3+3? (for example) 
    if c.verify(q.token, answer):
        print('Correct') # if the user entered 6
    else:
        print('Wrong') # otherwise
