import csv
import os
import datetime
import log
import exit
from datetime import timedelta
from datetime import date
from screen import Screen


def search_for_books(main_page): # Add information to the printout if the book is rented
    """Ask for the type of search and then lists books based of the criteria"""

    type_of_search = 0

    header = """
    Do you want to search for books by the first letter of the title
    or by the type?
            """
    search_choices= (
        ("To search by letter", search_by_letter),
        ("To search by type", search_by_type),
        ("To exit",exit.exit_to_main)
                    )

    book_search = Screen(header,search_choices,
                        main_page.login, main_page.password)
    book_search.activate()

def search_by_letter(book_search):
    """ Lists books that are starting with the entered letter"""
    print("What is the first letter of the searched title? Use uppercase")
    letter = input(">  ")

    # books.csv = [title,author,year,ID,book_type]
    with open('books.csv', 'r') as book_base:
        book_list = csv.reader(book_base)
        next(book_list)
        pointer = 0

        for book_data in book_list:
            if book_data[0].startswith(letter):
                print(book_data)
                ID = book_data[-2]
                if_rented(ID)
                pointer = 1

        if pointer == 0:
            print("Sorry, there is no book starting with this letter\n")
    return


def book_printer(book_type):
    """Prints books of the type"""

    # books.csv = [title,author,year,ID,book_type]
    with open('books.csv', 'r') as book_base:
        book_list = csv.reader(book_base)
        next(book_list)

        for book_data in book_list:
            if book_data[-1] == book_type:
                print(book_data)
                ID = book_data[-2]
                if_rented(ID)
        print('\n')
        return


def search_by_type(book_search):
    """Lists all books from the set type"""

    book_type_translator = {
        '1':'fiction',
        '2':'crime',
        '3':'adventure'
        }

    print("What type of book are you looking for? Enter a number")
    print(
    "\n".join(f"{num}.{genre}" for num, genre in book_type_translator.items()))

    book_type_number = 0

    while True:
        book_type_number = input('>  ')

        if book_type_number in book_type_translator:
            book_type = book_type_translator[book_type_number]
            book_printer(book_type)
        elif book_type_number == 'X':
            return
        else:
            print("Book type invalid, try again or [X] to exit")


def if_rented(ID):
    """Checks if book is rented or not, prints the information"""

    # rented.csv = [ID,rental_date,return_date,RETURNED,login]
    with open('rented.csv','r') as rented_base:
        rented_reader = csv.DictReader(rented_base)
        for rented_data in rented_reader:
            if rented_data['ID'] == ID:
                if rented_data['RETURNED'] == 'TRUE':
                    print("Book is available!")
                else:
                    print("\tBook is rented and should be back on",
                        rented_data['return_date'],"\n"
                        )


def check_my_books(main_page):
    """checks the books rented by the person in rented.csv base"""

    login = main_page.login

    # rented.csv = [ID, rental_date, return_date, login]
    with open('rented.csv', 'r') as rented_base:
        rented_reader = csv.reader(rented_base)
        next(rented_reader)

        books_table = []

        for line in rented_reader:
            if line[-1] == login:
                books_table.append([line[0],line[1],line[2]])

        print("Your rented books are:")

        books_table_reader(books_table)


def books_table_reader(books_table):
    """Reads user books from books_table"""

    # books.csv = [title, author, year, ID, book_type]
    with open('books.csv', 'r') as book_base:
        book_reader = csv.reader(book_base)
        next(book_reader)
        for line in book_reader:
            for box in books_table:
                if line[3] == box[0]:
                    print(line)
                    print("\tRented on",box[1],"\nTo be returned on",box[2])


def rent_book(main_page):
    """changes books data to 'rented' in rented.csv"""

    print("Which book do you wish to rent? Enter its code")
    book_code = input('>  ')

    check_code_and_rent(main_page, book_code)

    os.remove('rented.csv')
    os.rename('rented_temp.csv','rented.csv')


def check_code_and_rent(main_page, book_code):
    """ Check if book code exists in base and  rents it"""

    with open('rented.csv', 'r') as rented_base:
        rented_reader = csv.reader(rented_base)
        next(rented_reader)

        rented_book_data = []
        check_if_available(main_page, rented_reader, book_code,
                            rented_book_data)

        if rented_book_data == []:
            print("There is no book with this code")
            return 1


def check_if_available(main_page,rented_reader, book_code,
                        rented_book_data):
    """Checks if book is available and if yes, rents it """

    for line in rented_reader:
        if line[0] == book_code:
            if line[-2] == 'FALSE':
                print('Books is unavailable')
                return
            else:
                rented_book_data = line
                change_books_status(main_page,book_code,
                                    rented_book_data)
                print("Congratulations, you've rented a book!")
                return


def date_setter():
    """ Sets rental and return data for a book"""
    rental_date = datetime.date.today()
    return_date = rental_date + timedelta(days= 40)

    rental_dates = []
    rental_dates.append(date.strftime(rental_date,'%d.%m.%Y'))
    return_dates.append(date.strftime(return_date,'%d.%m.%Y'))

    return rental_dates


def rented_book_new_data(main_page, book_code):
    """Sets a table of rented book data"""

    login = main_page.login

    # modifying book_data:
    rental_date, return_date = date_setter()

    new_rented_data = [book_code,
                    rental_date,
                    return_date,
                    'FALSE',
                    login
                    ]

    return new_rented_data


def change_books_status(main_page, book_code, rented_book_data):
    """Creates rented_temp.csv file with changed book status"""

    new_rented_data = rented_book_new_data(main_page, book_code)

    with open('rented.csv', 'r') as rented_base_r:
        rented_reader = csv.reader(rented_base_r)

        with open('rented_temp.csv','w', newline = '') as rented_base_w:
            rented_writer = csv.writer(rented_base_w)

            for line in rented_reader:
                if line[0] == book_code:
                    rented_writer.writerow(new_rented_data)
                else:
                    rented_writer.writerow(line)


def change_name(change_account):
    """ Delegates change_name() to change_data() with 'name' """
    change_data(change_account, changed_data='name')


def change_surname(change_account):
    """ Delegates change_name() to change_data() with 'surname' """
    change_data(change_account, changed_data='surname')


def change_password(change_account):
    """ Delegates change_name() to change_data() with 'password' """
    change_data(change_account, changed_data='password')


def change_account_details(main_page):
    """ Depending on the imput changes account details in 'data.csv'"""

    header = "What do you want to change?"
    change_choices =(
            ('Name',change_name),
            ('Surname',change_surname),
            ('Password',change_password),
            ('To exit',log.exit)
            )

    change_account = Screen( header, change_choices, main_page.login,
                            main_page.password)

    change_account.activate()


def change_data(change_account, changed_data):

    login = change_account.login
    password = change_account.password

    print("What is your new",changed_data,"?")
    new_data = input('>  ')
    print("Enter your current password to accept the change")
    user_password = input('>  ')

    if user_password == password:
        change_data_writer(login, changed_data, new_data,)
    else:
        print("Wrong password")
        return


def data_line_code_generator(changed_data):

    changed_value = {
                    'name':0,
                    'surname':1,
                    'password':3
                    }

    data_line_code = changed_value[changed_data]
    return data_line_code


def change_new_data_writer_from_file(login):
    """Returns users data table from data.csv"""

    with open('data.csv', 'r') as data_base_r:
        data_reader = csv.reader(data_base_r)
        # searching for a line with inputed login
        data_line = []

        with open("data.csv", 'r') as login_search:
            login_reader = csv.reader(login_search)
            next(login_reader)

            for lines in login_reader:
                if lines[2] == login:
                    data_line = lines
                    return data_line


def change_data_writer(login, changed_data, new_data):

    data_line_code = data_line_code_generator(changed_data)

    data_line = change_new_data_writer_from_file(login)

    # change the data
    data_line[data_line_code] = new_data

    change_new_data_writer_to_file(login, data_line)

    os.remove('data.csv')
    os.rename('data_temp.csv','data.csv')


def change_data_writer_to_file(login, data_line):
    """ Creates data_temp.csv copy of data.csv with changed data"""

    with open("data_temp.csv", 'w', newline='') as data_base_w:
        data_writer = csv.writer(data_base_w)

        for line in data_reader:
            if line[2] == login:
                data_writer.writerow(data_line)
            else:
                data_writer.writerow(line)
