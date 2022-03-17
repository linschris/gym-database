"""
Gym Management Application (.py)
By Christopher Linscott

A simple gym management application which acts as an abstraction
to the gym database and allows one to get information from the database
given some input variables!

Run this file and see the possibilities!
If you don't want to make a new user, use 
'gymmember' for user and 'gains' for pass to try out non-admin mode!

Or refer to setup-passwords to see already created users.
"""

import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode
from queries import *

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. Set to False when done testing.
DEBUG = False
DONE = False
# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn(user, password):
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user=user,
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',
          password=password,
          database='gymDB'
        )
        if DEBUG:
            print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            print_error('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            print_error('Database does not exist.')
        elif DEBUG:
            print_error(err)
        else:
            print_error('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
def login_user(conn):
    print("Please type in your corresponding credentials to access the DB.")
    user = input("Username:\n")
    password = input("Password:\n")
    return authenticate(conn, user, password)

def authenticate(conn, user, password):
    authenticate_procedure = "SELECT authenticate(\'%s\', \'%s\') AS logged_in;" % (user, password)
    cursor = conn.cursor()
    cursor.execute(authenticate_procedure)
    rows = cursor.fetchall()
    for row in rows:
        if row[0]:
            print_success('Authenticated!')
            return is_admin(cursor, user)
        else:
            print_error('Could not authenticate. Please try again.')
            exit()

def is_admin(cursor, user):
    query = "SELECT is_admin FROM user_info WHERE username = \'%s\';" % (user)
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            if row[0]:
                print_success('Signed in as an admin!')
                conn = get_conn('gymadmin', 'adminpw')
                return conn, True
            else:
                print_success('Signed in as a member!')
                conn = get_conn('gymmember', 'memberpw')
                return conn, False
    except mysql.connector.ProgrammingError as err:
        handle_error(err)



# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    while not DONE:
        print('What would you like to do? ')
        print('  (c) - What classes are currently being offered?')
        print('  (t) - Top 10 Lift Stats')
        print('  (i) - Instructor Ratings')
        print('  (p) - Enroll in class')
        print('  (r) - Give class rating')
        print('  (m) - Pay for your membership!')
        print('  (q) - quit')
        print()
        ans = input('Enter an option: \n').lower()
        if ans == 'q':
            quit_ui()
        else:
            take_in_input(ans)



# You may choose to support admin vs. client features in the same program, or
# separate the two as different client and admin Python programs using the same
# database.
def show_admin_options():
    """
    Displays options specific for admins, such as adding new data <x>,
    modifying <x> based on a given id, removing <x>, etc.
    """
    while not DONE:
        print('What would you like to do? ')
        print('  (g) - Grab information about any relation! (give input relation)')
        print('  (f) - Fire employees or remove members')
        print('  (i) - Instructor Ratings')
        print('  (q) - quit')
        print()
        ans = input('Enter an option: \n').lower()
        if ans == 'q':
            quit_ui()
        else:
            take_in_input(ans)


def take_in_input(user_input):
    if len(user_input) != 1:
        print_error("Only 1-letter input are accepted, please try again.")
        return
    letter = user_input[0]
    if letter == 'i':
        instructor_ratings(conn)
    elif not IS_ADMIN:
        if letter == 'c':
            # Grab classes
            select_query(conn, 'class')
        elif letter == 't':
            # Leaderboard query
            leaderboard_query(conn)
        elif letter == 'm':
            # Pay for membership
            person_id = int(input('What is your person ID number?\n'))
            pay_membership(conn, person_id)
        elif letter == 'p':
            # Enroll in class
            person_id = int(input("What is your person ID?\n"))
            class_id = int(input("What is the class ID of the class you want to enroll?\n"))
            enroll_in_class(conn, person_id, class_id)
        elif letter == 'r':
            # Give rating
            num_choice = int(input("Type 1 if you're voting for a session, and 2 for a class.\n"))
            cs_id = int(input("What is the class or session ID?\n"))
            rating = int(input("Give a rating from 1-5 (any other values will not work).\n"))
            person_id = int(input("What is your person ID?\n"))
            enroll_in_class(conn, cs_id, person_id, rating, num_choice)
        else:
            print_error("Not an available option, please try again.")
    else:
        if letter == 'g':
            # Ask for input
            # SELECT query with input
            relation_name = input("What relation would you like to access?\n")
            select_query(conn, relation_name)
        elif letter == 'f':
            # Fire employees/members
            is_member_or_employee = (int(input("Type 0 for member and Type 1 for employee.\n")))
            person_id = int(input("What is the member or employee ID?\n"))
            fire_employee_or_member(conn, person_id, is_member_or_employee)
            
        else:
            print_error("Not an available option, please try again.")


def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    if IS_ADMIN:
        show_admin_options()
    else:
        show_options()


if __name__ == '__main__':
    # This conn is a global object that other functinos can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    guest_conn = get_conn('guest', 'password')
    (conn, IS_ADMIN) = login_user(guest_conn)


    #  = login_user()
    main()
