import csv
import librarian as lib
import log
import sys
import intro
import account as ac
from screen import Screen
from collections import namedtuple



def exit(intro):
    print("Quitting the library\nGoodbye!")
    sys.exit()

while True:
    intro.intro()
