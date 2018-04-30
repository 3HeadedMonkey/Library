import collections
# from collections import OrderedDict
import os
from collections import OrderedDict
from collections import namedtuple
from screen import Screen

# Choice = namedtuple('name','desc')
# p = Choice('Dark', 'A very dark place')

choice =  namedtuple('choice',['desc','func'])


header = """\t\tLOGIN______________________________
        Welcome to the LIBRARY 6000 system!"""

def first():
    print("Works")

def create_account():
    print("works2")

def librarian():
    print('works 3')

def exit():
    print('works 4')

choices = (
        choice('To log in', first),
        choice('To create a new account', create_account),
        choice('To admin funcions', librarian),
        choice('To exit', exit)
        )

print(choices)
print('_____________________')
for i, row in enumerate(choices, 1):
    print(i, row[0], row[1])

intro = Screen(header, choices)
intro.activate()

# first()
# pu = choice ('forst', first())
# pu[1]()
