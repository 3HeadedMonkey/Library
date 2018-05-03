from collections import namedtuple
import exit


class Screen():
    """ Controls the printout"""
    
    def __init__(self, header, choices, login = 'none', password = 'none'):
        self.header = header
        self.screen_text = self.header + '\n'
        self.choices = choices
        self.dict = {}

        self.login = login
        self.password = password

        for i, row in enumerate(self.choices, 1):
            self.screen_text += '{} {}\n'.format(i, row[0])
            self.dict[str(i)] = row[1]


    def activate(self):
        """ Prints out the text and follows the choise"""

        while True:
            print(self.screen_text)
            self.task = input('>  ')
            if self.task in self.dict:
                self.dict[self.task](self)
                # (self.login, self.password)
            else:
                print('Wrong command')
