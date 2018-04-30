import csv
import os
import operator
import datetime
from datetime import date


def adding_books():
    """ Adds books to database and then sorts the bookbase by code"""

    book_type_translator = {
                            '1':'fiction',
                            '2':'crime',
                            '3':'adventure'
                            }
    book_type_translator_letter = {
                                '1':'F',
                                '2':'C',
                                '3':'A'
                                }

    print("\nWhat type of a book do you wish to add? To exit type 'X'")
    print("\n".join(f"{num}.{genre}" for num,
     genre in book_type_translator.items()))

    type = 0
    stoper = 0
    # This is plain stupid, redo, just check ofr key() or whatever

    # Creating new books ID (its type as the last one in the base)
    while stoper == 0:
        type = input('>  ')
        if type == '1' or type == '2' or type == '3':
            stoper = 1
        elif type == 'X':
            return
        else:
            print("Invalid number, try again")

    book_type = book_type_translator[type]

    code_letter = code_letter_generator(book_type)

    new_code = code_generator(code_letter)


def code_letter_generator(book_type):

    with open('rented.csv','r') as book_base:
        book_rented = csv.reader(book_base)

        for line in book_rented:
            if line[0].startswith(book_type):
                code_letter = line[0]

    return code_letter
    # Add iterating from the back instead of rerwriting code_letter all over again


def new_book_data(new_code, book_type):
    """ Gathers book data form keyboard and adds the book to the base"""

    print("What is the books title?")
    title = input('>  ')

    print("Who is the author?")
    author = input('>  ')

    print('What is the year the books has been published?')
    year = int(input('>  '))

    new_book = [title, author, year, new_code, book_type]
    book_adder(new_book)


def code_generator(code_letter):
    """Returns a new code from the letter of the last book of the type"""

    code_number = int(code_letter[1:])
    code_number +=1
    code_number = str(code_number)
    new_code = ''.join([code_letter[0],code_number])
    return new_code


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

    with open('rented.csv', 'r', newline='') as rented_base_r:
        rented_reader = csv.reader(rented_base_r)

        with open('rented_temp.csv','w',newline='') as rented_base_w:
            rented_writer = csv.writer(rented_base_w)

            # rented.csv = [book_code,rental_date,return_date,RETURNED,login ]
            for line in rented_reader:
                if line[0] != book_code:
                    rented_writer.writerow(line)

    with open('books.csv', 'r', newline='') as book_base_r:
        book_reader = csv.reader(book_base_r)

        with open('books_temp.csv', 'w', newline='') as book_base_w:
            book_writer = csv.writer(book_base_w)

            for row in book_reader:
                if row[3] != book_code:
                    book_writer.writerow(row)



    os.remove('rented.csv')
    os.rename('rented_temp.csv','rented.csv')

    os.remove('books.csv')
    os.rename('books_temp.csv','books.csv')


def person_search():
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


def person_details(login):
    """Lists details of a person (DictReader), his rented books etc"""

    with open('data.csv','r') as data_base_r:
        data_reader = csv.DictReader(data_base_r)
        next(data_reader)

        print("Account data:\n")

        for line in data_reader:
            if line['login'] == login:
                print(
                    '\n'.join(f"\t{data}: {person}"
                    for data, person in line.items())
                    )

    print("\nAccounts books:\n")

    with open('rented.csv', 'r') as rented_base_r:
        rented_reader = csv.DictReader(rented_base_r)

        with open('books.csv', 'r') as books_base_r:
            books_reader = csv.DictReader(books_base_r)

            licznik = 0
            exist = 0

            for line in rented_reader:
                if line['login'] == login:
                    licznik += 1
                    exist = 1
                    for row in books_reader:
                        if line['ID'] == row['ID']:
                            print('  ',licznik,"__")
                            print(
                                "\n".join(f"\t{data}: {person}"
                                for data, person in row.items())
                                )
                            print(
                                "\n\tRented on:", line['rental_date'],
                                "\n\tTo be returned on:",line["return_date"],"\n\n"
                                )
                            break
            if exist ==0:
                print("There is no login of the kind in the database")


def delete_account(login):
    """ Delets users account from data.csv"""

    print("Which account should be deleted? Enter its login:")
    login = input('>  ')

    with open('data.csv', 'r', newline='') as data_base_r:
        data_reader = csv.reader(data_base_r)

        with open('data_temp.csv','w', newline='') as data_base_w:
            data_writer = csv.writer(data_base_w)

            for line in data_reader:
                if line[2] != login:
                    data_writer.writerow(line)

    os.remove('data.csv')
    os.rename('data_temp.csv','data.csv')


def return_book(ID):
    """ In rented.csv sets books RETURNED status to TRUE """

    returned_date = datetime.date.today()
    returned_date = date.strftime(returned_date,'%d.%m.%Y')

    # rented = [ID,rental_date,return_date,RETURNED,login]
    with open('rented.csv','r') as rented_base_r:
        rented_reader = csv.reader(rented_base_r)
        next(rented_reader)
        book_status = []

        pointer = 0
        for line in rented_reader:
            if line[0] == ID:
                pointer = 1
                book_status.append(line[0])
                book_status.append(line[1])
                book_status.append(returned_date)
                book_status.append("TRUE")
                book_status.append("") # empty place after the login

        if pointer == 0:
            print('There is no book of this code in the database')
            return 1

    with open('rented.csv','r') as rented_base_r:
        rented_reader = csv.reader(rented_base_r)
        with open('rented_temp.csv','w', newline = '') as rented_base_w:
            rented_writer = csv.writer(rented_base_w)

            for row in rented_reader:
                if row[0] == ID:
                    rented_writer.writerow(book_status)
                else:
                    rented_writer.writerow(row)



    os.remove('rented.csv')
    os.rename('rented_temp.csv','rented.csv')


def person_rented(login):

    """ returns a list of IDs of books borrowed by the user"""

    # rented.csv = [ID,rental_date,return_date,RETURNED,login]
    with open('rented.csv','r') as rented_base_r:
        rented_reader = csv.DictReader(rented_base_r)
        ID_list = []
        for line in rented_reader:
            if line['login'] == login:
                ID_list.append(line['ID'])



        return ID_list


def person_check(admin_choices):
    person_search()
    detailed_check()


def detailed_check():
    users_login = 'none'
    while users_login != 'X':
        print("\n\nTo check users data enter his login, to exit enter 'X'\n")
        users_login = input('>  ')
        if users_login == '':
            pass
        else:
            person_details(login) #add cheker if the login exists?
