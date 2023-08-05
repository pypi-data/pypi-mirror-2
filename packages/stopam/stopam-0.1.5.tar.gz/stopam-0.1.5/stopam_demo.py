#!/usr/bin/python
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))

from stopam.client import Service, InvalidApiKeyError

usage = '\n'.join(['Usage:', 
                   ' {0} key'.format(sys.argv[0]),
                   ' where key looks like "0123456789abcdefghijklmnopqrstuv"',
                   'Example:',
                   ' {0} 0123456789abcdefghijklmnopqrstuv'.format(sys.argv[0]),
                   '',
                   'Visit http://stopam.com/ to obtain your key.'])

try:
    key = sys.argv[1]

    if not key:
        print usage
        sys.exit(0)
except IndexError:
    print usage
    sys.exit(0)

print('Press Ctrl+C to stop\n')

try:
    with Service(key, fallback=False) as c:
        while True:
            q = c.ask()
            
            answer = raw_input(q.question) # How much is 3+3? (for example) 
            if c.verify(q.token, answer):
                print('Correct') # if the user entered 6
            else:
                print('Wrong') # otherwise
except KeyboardInterrupt:
    print('\n\nCheck http://stopam.com/ for more information.') 
except InvalidApiKeyError:
    print('The key provided seems to be invalid.')
    print(usage)