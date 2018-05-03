import sys
import log


def exit_to_intro(self):
    import Library
    """ Returns to the intro screen """
    # intro.activate()

    Library.main()


def exit_to_main(self):
    """ Returns to main page along with login and password data"""
    login = self.login
    password = self.password
    log.main_page(login, password)


def exit(self):
    """ Exits the system"""
    print("Goodbye")
    sys.exit()
