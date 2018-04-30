import csv
import librarian as lib
import log
import account as ac
from screen import Screen
from collections import OrderedDict
from collections import namedtuple



def log_in_and_go_to_main_page():
    login, password = log.log_in()
    main_page(login, password)

def exit():
    print("Quitting the library\n Goodbye!")
    # add exit


def main_page(login, password):

    choice = '0'
    while choice != '5':
        print("""
        ACCOUNT_________________
        Welcome to your page
        What do you want to do?
        1. Search for a book
        2. Check your books
        3. Rent a book
        4. Change your account data
        5. Log out
            """
            )

        choice = input('>  ')
        if choice == '1':
            ac.search_for_books()
        elif choice == '2':
            ac.check_my_books(login)
        elif choice == '3':
            ac.rent_book(login)
        elif choice == '4':
            ac.change_account_details(login, password)
        elif choice == '5':
            print("LOGGING OUT")
            return
        else:
            print("Wrong command, try again")


def librarian(main_page):
    """Admins domain with access to admin funcitons """
    admin_header ="""
        ADMIN___________________________
        This is librairian account. What do you want to do?
            """"

    admin_choices=(
        "Return a book",
        "Add a book",lib.adding_books
        "Delete a book",lib.deleting_books
        "Check person database",lib.person_check
        "Delete users account",
        "To quit"
                )
    choice = 0
    while choice != '6':
        print("""\n
        ADMIN___________________________
        This is librairian account. What do you want to do?
        1. Return a book
        2. Add a book
        3. Delete a book
        4. Check person database
        5. Delete users account
        6. To quit
            """
            )
        choice = input('>  ')
        login = 0

        if choice is '1':
            print("Enter books code, to exit enter 'X':")
            ID = input('>  ')
            if ID == 'X':
                return
            lib.return_book(ID)
        elif choice is '2':
            lib.adding_books()
        elif choice is '3':
            lib.deleting_books()
        elif choice is '4':
            lib.person_search()
            while login != 'X':
                print("\n\nTo check users data enter his login, to exit enter 'X'\n")
                login = input('>  ')
                if login == '':
                    pass
                else:
                    lib.person_details(login) #add cheker if the login exists?
        elif choice is '5':
            while login != 'X':
                print("""
    Enter login of the user that you wish to delete,
    to exit enter 'X'
    Books borrowed by that person will be marked as returned!
                    """
                    )
                login = input('>  ')

                if login == '':
                    print("Enter an argument")
                if login == 'X':
                    return
                else:
                    books = []
                    ID_list = lib.person_rented(login)
                    if len(ID_list) == 0:
                        print("User doesnt exits!")
                    else:
                        for ID in ID_list:
                            lib.return_book(ID)
                    lib.delete_account(login)
        elif choice is '6':
            print('Goodbye!')
        else:
            print("Wrong command, try again")
######################################################################
# intro()
header = """\t\tLOGIN______________________________
        Welcome to the LIBRARY 6000 system!"""

choice =  namedtuple('Choice',['desc','func'])

choices = (
        choice('To log in', log.log_in_and_go_to_main_page),
        choice('To create a new account', log.create_account),
        choice('To admin funcions', librarian),
        choice('To exit', log.exit)
        )

intro = Screen(header, choices)

intro.activate()

#######################################################

main_header = """        ACCOUNT_________________
        Welcome to your page
        What do you want to do?
        """
main_choices = (
        ('Search for a book', ac.search_for_books),
        ('Check your books', ac.check_my_books), # LOGIN?
        ('Rent a book',ac.rent_book), # LOGIN?
        ('Change your account data',ac.change_account_details),
        ('Log out',exit)
        )

main_page = Screen(main_header, main_choices, login, password)
main_page.activate()
