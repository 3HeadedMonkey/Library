import csv
import exit
from datetime import datetime
from collections import namedtuple

import account as ac
from screen import Screen

def log_in_and_go_to_main_page(intro):
    """Logs in the user and activates his main page"""

    login, password = log_in(intro)
    main_page(login, password)


def main_page(login, password):
    """Loads main page of the user"""

    main_header = """
            ACCOUNT_________________
            Welcome to your page
            What do you want to do?
            """

    choice =  namedtuple('Choice',['desc','func'])

    main_choices = (
            choice('Search for a book', ac.search_for_books),
            choice('Check your books', ac.check_my_books), # LOGIN?
            choice('Rent a book',ac.rent_book), # LOGIN?
            choice('Change your account data',ac.change_account_details),
            choice('Log out',exit.exit_to_intro)
            )

    main_page = Screen(main_header, main_choices, login, password)
    while True:
        main_page.activate()


def create_account(intro):
    """Adds person data into 'base.csv' """

    with open('data.csv', 'a', newline='') as data:
        data_writer = csv.writer(data)

        print("""
        Welcome to the account creator!
        To exit at any time type 'X'"
        "What is your new login?
        """
        )
        login = input('>  ')
        if login == 'X':
            return

        login_test = login_taken(login)
        data = data_collector(login)
        data_writer.writerow(data)


def data_collector(login):
    """ Returns a table of new user data from the keyboard"""

    collecting_data = ['name', 'surname', 'email', 'password']
    temp_data = []

    for info in data:
        print('What is your ', info,'?')
        collected_data = input('>  ')
        if collected_data == 'X':
            return
        temp_data.append(collected_data)

    name, surname, email, paassword = temp_data
    data = [name, surname, login, password, email]

    return data


def login_taken(main_page):
    """ Checks if the login in the base is already taken"""

    login = main_page.login

    taken = 1
    while taken != 0:
        with open('data.csv', 'r') as data_file:
            data_list = csv.reader(data_file)
            next(data_list)

            for person_data in data_list:
                if person_data[2] is login:
                    print("ERROR\nLOGIN TAKEN")
                    if taken == 'X':
                        return 1
                else:
                    taken = 0
    return 0


def log_in(intro):
    """ After verification with 'data.csv' base returns users login"""

    print("Hello User! Enter your login OR enter '1' to create account")
    check = 2

    while check != 0:
        login = input('>  ')

        if login == '1':
            create_account(intro)
            print("Enter your login again")
            login = input('>  ')

        print("Enter your password")
        password = str(input('>  '))
        check = check_password(login,password)

    return login, password


def check_password(login,password):
    """Checks if the password and login are binded together"""


    with open('data.csv', 'r') as data_file:
        data_list = csv.reader(data_file)
        next(data_list)

        for person_data in data_list:
            if person_data[2] == login\
            and person_data[3] == password:
                print("WORKS FINE")
                return 0
    print(
    """Either password or Login is not good. Enter your login again.
    To create a new account enter '1'
    """
    )
    return 2
