import csv
import os
import operator
import datetime

import log
import exit as ex

from datetime import date
from collections import namedtuple
from screen import Screen





def librarian(main_page):
    """Admins domain with access to admin funcitons """

    admin_header = """
            ADMIN___________________________
            This is librairian account. What do you want to do?
                """
    choice =  namedtuple('Choice',['desc','func'])

    admin_choices=(
            choice("Return a book", return_single_book),
            choice("Add a book",adding_books),
            choice("Delete a book",deleting_books),
            choice("Check person database",person_search),
            choice("Delete users account",if_to_delete_user),
            choice("To quit", exit.exit_to_intro)
            )

    admin_page = Screen(admin_header,admin_choices, main_page)
    while True:
        admin_page.activate()


def adding_books(admin_page):
    """ Adds books to database and then sorts the bookbase by code"""

    book_type_translator = {
                            '1':'fiction',
                            '2':'crime',
                            '3':'adventure'
                            }

    print("\nWhat type of a book do you wish to add? To exit type 'X'")
    print("\n".join(f"{num}.{genre}" for num,
     genre in book_type_translator.items()))

    book_type_letter = input_checker(book_type_translator)
    highest_previous_code = code_letter_generator(book_type_letter)
    new_code = code_generator(highest_previous_code)

    new_book_data(new_code, book_type_letter)


def input_checker(book_type_translator):
    """ Takes input and checks if its in the dict, or exits the loop"""

    book_type_translator_letter = {
                            '1':'F',
                            '2':'C',
                            '3':'A'
                            }

    while True:
        type = input('>  ')
        if type in book_type_translator:
            book_type_letter = book_type_translator_letter[type]
            return book_type_letter
        elif type == 'X':
            log.exit() # do something about this exit funcion finally
        else:
            print("Invalid number, try again")


def code_letter_generator(book_type_letter):
    """ Checks for the existing highest book code of the type"""

    with open('rented.csv','r') as book_base:
        book_rented = csv.reader(book_base)

        for line in book_rented:
            if line[0].startswith(book_type_letter):
                highest_previous_code = line[0]

    return highest_previous_code


def code_generator(highest_previous_code):
    """Returns a new code from the of the highest previous code """

    code_number = int(highest_previous_code[1:])
    code_number +=1
    code_number = str(code_number)
    new_code = ''.join([highest_previous_code[0],code_number])

    return new_code


def new_book_data(new_code, book_type_letter):
    """ Gathers book data form keyboard and adds the book to the base"""

    print("What is the books title?")
    title = input('>  ')

    print("Who is the author?")
    author = input('>  ')

    print('What is the year the books has been published?')
    year = int(input('>  '))

    new_book = [title, author, year, new_code, book_type]
    book_adder(new_book)

    print('\nBook has been added to the base\n')


def book_adder(new_book):
    """modifier of booth books.csv and rented.csv files"""

    # rented_table = [ID,rental_date,return_date,RETURNED,login]
    new_rented = [new_code,0,0,'TRUE',0]

    with open('books.csv', 'a') as book_base:
        book_appender = csv.writer(book_base)
        book_appender.writerow(new_book)

    with open('rented.csv', 'a') as rented_base:
        rented_appender = csv.writer(rented_base)
        rented_appender.writerow(new_rented)


def deleting_books():
    """ Deletes certain book from librairies, intakes books code"""

    print("Enter books code:")
    book_code = input('>  ')

    rented_base_deleter(book_code)
    books_base_deleter(book_code)

    temp_files_renamer()


def rented_base_deleter(book_code):
    """Creates temp file of rented.csv without given book"""

    with open('rented.csv', 'r', newline='') as rented_base_r:
        rented_reader = csv.reader(rented_base_r)

        with open('rented_temp.csv','w',newline='') as rented_base_w:
            rented_writer = csv.writer(rented_base_w)

            # rented.csv = [book_code,rental_date,return_date,RETURNED,login ]
            for line in rented_reader:
                if line[0] != book_code:
                    rented_writer.writerow(line)


def books_base_deleter(book_code):
    """Creates temp file of books.csv without given book"""

    with open('books.csv', 'r', newline='') as book_base_r:
        book_reader = csv.reader(book_base_r)

        with open('books_temp.csv', 'w', newline='') as book_base_w:
            book_writer = csv.writer(book_base_w)

            for row in book_reader:
                if row[3] != book_code:
                    book_writer.writerow(row)


def temp_files_renamer():
    """Exchanges temp versions of 'rented.csv' 'books.csv' with current"""

    os.remove('rented.csv')
    os.rename('rented_temp.csv','rented.csv')

    os.remove('books.csv')
    os.rename('books_temp.csv','books.csv')


def person_search(admin_page):
    """Lists all users alphabetically by name then surname """

    print("Listing all the users!\n__________________________________")

    with open('data.csv','r') as data_base_r:
        data_reader = csv.reader(data_base_r)

        next(data_reader)
        data_sorted = sorted(data_reader, key=operator.itemgetter(0, 1))
        data_sorted = enumerate(data_sorted, 1)

        for lines in data_sorted:
            print('\n',lines[0], end = '  ')
            for row in lines[1]:
                print(row, end = ' ')

    if_to_detailed_search(admin_page)


def if_to_detailed_search(admin_page):
    """ Takes login from keyboard and looks for its data in database"""

    while True:
        print("\n\nTo check users data enter his login, to exit enter 'X'\n")
        searched_login = input('>  ')
        if searched_login == '':
            pass
        if searched_login == 'X':
            return
        else:
            person_details(searched_login) #add cheker if the login exists?


def person_details(searched_login):
    """Lists details of a person (DictReader), his rented books etc"""

    person_details_data_printer(searched_login)
    print("\nAccounts books:\n")
    account_books_printer(searched_login)


def person_details_data_printer(searched_login):
    """Prints login details"""

    with open('data.csv','r') as data_base_r:
        data_reader = csv.DictReader(data_base_r)
        next(data_reader)

        print("Account data:\n")

        for line in data_reader:
            if line['login'] == searched_login:
                print(
                '\n'.join(f"\t{data}: {person}"
                for data, person in line.items()))
                return
        print("There is no login of the kind in the base")


def account_books_printer(searched_login):
    """Prints accounts rented books"""

    with open('rented.csv', 'r') as rented_base_r:
        rented_reader = csv.DictReader(rented_base_r)

        with open('books.csv', 'r') as books_base_r:
            books_reader = csv.DictReader(books_base_r)

            counter = 0
            for line in rented_reader:
                if line['login'] == searched_login:
                    counter += 1
                    for row in books_reader:
                        if line['ID'] == row['ID']:
                            book_data_printer(line, row, counter)
                            break


def book_data_printer(line, row, counter):
    """Prints outs users rented books"""

    print('  ',counter,"__")
    print(
        "\n".join(f"\t{data}: {person}"
        for data, person in row.items())
        )
    print(
        "\n\tRented on:", line['rental_date'],
        "\n\tTo be returned on:",line["return_date"],"\n\n")


def if_to_delete_user(admin_page):
    """ Takes user login, deletes it and returns its books"""

    while True:
        print("""
        Enter login of the user that you wish to delete,
        to exit enter 'X'
        Books borrowed by that person will be marked as returned!
            """
            )

        login_to_delete = input('>  ')

        if login_to_delete == '':
            print("Enter an argument")
        if login_to_delete == 'X':
            return
        else:
            books = []
            ID_list = person_rented(login_to_delete)
            for ID in ID_list:
                return_book(ID)
                delete_account(login_to_delete)


def delete_account(login_to_delete):
    """ Delets users account from data.csv"""


    with open('data.csv', 'r', newline='') as data_base_r:
        data_reader = csv.reader(data_base_r)

        with open('data_temp.csv','w', newline='') as data_base_w:
            data_writer = csv.writer(data_base_w)

            for line in data_reader:
                if line[2] != login_to_delete:
                    data_writer.writerow(line)

    os.remove('data.csv')
    os.rename('data_temp.csv','data.csv')


def return_single_book(admin_page):
    """Asks for a book code to return and executes return_book(ID)"""

    print("Enter books code, to exit enter 'X':")
    ID = input('>  ')
    if ID == 'X':
        return # EXIT FUNCION
    return_book(ID)


def return_book(ID):
    """ In rented.csv sets books RETURNED status to TRUE """

    returned_date = datetime.date.today()
    returned_date = date.strftime(returned_date,'%d.%m.%Y')

    book_status = return_book_status(ID, returned_date)

    return_book_status_writer(ID, book_status)

    os.remove('rented.csv')
    os.rename('rented_temp.csv','rented.csv')


def return_book_status(ID, returned_date):
    """Creates table with return book status data"""

    # rented = [ID,rental_date,return_date,RETURNED,login]
    with open('rented.csv','r') as rented_base_r:
        rented_reader = csv.reader(rented_base_r)
        next(rented_reader)
        book_status = []

        for line in rented_reader:
            if line[0] == ID:
                book_status = [line[0], line[1],
                            returned_date, "TRUE",
                            ""] # empty place after the login
                return book_status

        print('There is no book of this code in the database')
        return 1

    return book_status


def return_book_status_writer(ID, book_status):
    """Creates rented_temp.csv file with new book status"""

    with open('rented.csv','r') as rented_base_r:
        rented_reader = csv.reader(rented_base_r)
        with open('rented_temp.csv','w', newline = '') as rented_base_w:
            rented_writer = csv.writer(rented_base_w)

            for row in rented_reader:
                if row[0] == ID:
                    rented_writer.writerow(book_status)
                else:
                    rented_writer.writerow(row)


def person_rented(login):
    """Returns a list of IDs of books borrowed by the user"""

    # rented.csv = [ID,rental_date,return_date,RETURNED,login]
    with open('rented.csv','r') as rented_base_r:
        rented_reader = csv.DictReader(rented_base_r)
        ID_list = []
        for line in rented_reader:
            if line['login'] == login:
                ID_list.append(line['ID'])

        return ID_list
