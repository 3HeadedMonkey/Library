import csv
import os
import datetime
import log
from datetime import timedelta
from datetime import date
from screen import Screen


def search_for_books(main_page): # Add information to the printout if the book is rented
    """Ask for the type of search and then lists the books based of the criteria"""

    type_of_search = 0

    header = """
    Do you want to search for books by the first letter of the title [A]
    or by the type [T]?
    To exit enter 'X'
            """
    search_choices= (
        ("To search by letter", search_by_letter),
        ("To search by type", search_by_type),
        ("To exit",log.exit)
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

    while book_type_number != 'X':
        book_type_number = input('>  ')
        if book_type_number in book_type_translator:
            book_type = book_type_translator[book_type_number]
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

        elif book_type_number is 'X':
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

    login = main_page.login # how to do it?


    # rented.csv = [ID, rental_date, return_date, login]
    with open('rented.csv', 'r') as rented_base:
        rented_reader = csv.reader(rented_base)
        next(rented_reader)

        books_table = []

        for line in rented_reader:
            if line[-1] == login:
                books_table.append([line[0],line[1],line[2]])

        print("Your rented books are:")

        # books.csv = [title, author, year, ID, book_type]
        with open('books.csv', 'r') as book_base:
            book_reader = csv.reader(book_base)
            next(book_reader)
            for line in book_reader:
                for box in books_table:
                    if line[3] == box[0]:
                        print(line)
                        print("\tRented on",box[1],"\nTo be returned on",box[2])


    input('> ')


def rent_book(main_page):
    """changes books data to 'rented' its 'return date' and by whom"""

    print("Which book do you wish to rent? Enter its code")
    book_code = input('>  ')

    with open('rented.csv', 'r') as rented_base:
        rented_reader = csv.reader(rented_base)
        next(rented_reader)

        pointer = 0
        # Verify if the book is available
        for line in rented_reader:
            if line[0] == book_code:
                pointer = 1
                if line[-2] == 'FALSE':
                    print('Books is unavailable')
                else:
                    rented_book_data = line
                    change_books_status(main_page,cbook_code, rented_book_data)
                    print("Congratulations, you've rented a book!")
                    break

        if pointer == 0:
            print("There is no book with this code")
            return 0

    os.remove('rented.csv')
    os.rename('rented_temp.csv','rented.csv')


def change_books_status(main_page, book_code, rented_book_data):
    """ creates rented_temp.csv file with changed book status"""

    login = main_page.login

    # modifying book_data:
    rental_date = datetime.date.today()
    return_date = rental_date + timedelta(days= 40)

    rental_date = date.strftime(rental_date,'%d.%m.%Y')
    return_date = date.strftime(return_date,'%d.%m.%Y')

    new_rented_data = [book_code,
                    rental_date,
                    return_date,
                    'FALSE',
                    login
                    ]

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

    changed_value = {
                'name':0,
                'surname':1,
                'password':3
                    }

    print("What is your new",changed_data,"?")
    new_data = input('>  ')
    print("Enter your OLD password to accept the change")
    user_password = input('>  ')

    #Out data base will be outdayed after the change

    if user_password == password:
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
                        break

            # change the data
            data_line[changed_value[changed_data]] = new_data

            with open("data_temp.csv", 'w', newline='') as data_base_w:
                data_writer = csv.writer(data_base_w)

                for line in data_reader:
                    if line[2] == login:
                        data_writer.writerow(data_line)
                    else:
                        data_writer.writerow(line)

        os.remove('data.csv')
        os.rename('data_temp.csv','data.csv')

    else:
        print("Wrong password")
