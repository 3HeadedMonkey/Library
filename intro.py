import sys
import log
import exit
import librarian as lib
from screen import Screen
from collections import namedtuple

def intro():
    """Loads intro screen"""

    header = """\t\tLOGIN______________________________
            Welcome to the LIBRARY 6000 system!"""

    choice =  namedtuple('Choice',['desc','func'])

    choices = (
            choice('To log in',log.log_in_and_go_to_main_page),
            choice('To create a new account', log.create_account),
            choice('To admin funcions', lib.librarian),
            choice('To exit', exit.exit)
            )

    intro = Screen(header, choices)

    intro.activate()
