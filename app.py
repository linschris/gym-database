"""
Gym Management Application (.py)
By Christopher Linscott

A simple gym management application which acts as an abstraction
to the gym database and allows one to get information from the database
given some input variables!

Run this file and see the possibilities!
"""
from ast import Pass
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode
from termcolor import colored
from prettytable import PrettyTable

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. Set to False when done testing.
DEBUG = True
IS_ADMIN = False
DONE = False

'''
    TODOs:
    - DEBUG --> FALSE
    - setup for admin, instructor, member
'''




# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='gymadmin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',
          password='adminpw',
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
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def example_query():
    param1 = ''
    cursor = conn.cursor()
    # Remember to pass arguments as a tuple like so to prevent SQL
    # injection.
    sql = 'SELECT col1 FROM table WHERE col2 = \'%s\';' % (param1, )
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        for row in rows:
            (col1val) = (row) # tuple unpacking!
            # do stuff with row data
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, please retry calling the function.')



# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
def login_user(user, password):

    pass



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
        print('  (m) - Pay for your membership!')
        print('  (q) - quit')
        print()
        ans = input('Enter an option: ').lower()
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
        print('  (f) - Fire employees/members')
        print('  (i) - Instructor Ratings')
        print('  (q) - quit')
        print()
        ans = input('Enter an option: ').lower()
        if ans == 'q':
            quit_ui()
        else:
            print(ans)
            take_in_input(ans)


def take_in_input(user_input):
    letter = user_input[0]
    if letter == 'i':
        instructor_ratings()
    elif not IS_ADMIN:
        if letter == 'c':
            # Grab classes
            select_query('class')
        elif letter == 't':
            # Leaderboard query
            leaderboard_query()
        elif letter == 'm':
            # Pay for membership
            person_id = int(input('What is your person ID number?\n'))
            pay_membership(person_id)
    else:
        if letter == 'g':
            # Ask for input
            # SELECT query with input
            relation_name = input("What relation would you like to access?\n")
            select_query(relation_name)


def select_query(relation_name=None, where=None):
    cursor = conn.cursor()
    if not relation_name:
        print("Invalid, nothing to select.")
    else:
        where_clause = where if where else ''
        sql = "SELECT * FROM %s %s;" % (relation_name, where_clause)
        try:
            execute_and_print_sql(cursor, sql)
        except mysql.connector.ProgrammingError as err:
            if not DEBUG:
                print(f"{colored('ERROR', 'red')}: {colored(err, 'red')}")
            # sys.exit(1)
            else:
                error_string = f'An error occurred, couldn\'t select from relation {relation_name} {where_clause}'
                print_error(error_string)
            
        
def instructor_ratings():
    cursor = conn.cursor()
    sql = "SELECT person_id AS instructor_id, IFNULL(AVG(rating), 'N/A') AS avg_rating, COUNT(*) AS total_classes_sessions FROM ((SELECT class_id, person_id, rating FROM employee NATURAL JOIN class_instructor NATURAL JOIN class NATURAL JOIN (SELECT class_id, rating FROM class_student) AS class_ratings UNION SELECT session_id AS class_id, trainer_id AS person_id, rating FROM session)) AS ratings GROUP BY instructor_id ORDER BY avg_rating DESC;"
    try:
        execute_and_print_sql(cursor, sql)
    except mysql.connector.ProgrammingError as err:
        if not DEBUG:
            print(f"{colored('ERROR', 'red')}: {colored(err, 'red')}")
        # sys.exit(1)
        else:
            error_string = f'An error occurred, couldn\'t do query.'
            print_error(error_string)

def leaderboard_query():
    cursor = conn.cursor()
    sql = "WITH total_stats AS (SELECT first_name, last_name, total_stats(person_id) AS total_lift_stats FROM physique NATURAL JOIN person) SELECT COUNT(ts.total_lift_stats) AS `rank`, CONCAT(ts.first_name, ' ', SUBSTRING(ts.last_name, 1, 1), '.') AS `name`, ts.total_lift_stats FROM total_stats ts, total_stats t WHERE ts.total_lift_stats < t.total_lift_stats GROUP BY ts.first_name, ts.last_name, ts.total_lift_stats ORDER BY COUNT(ts.total_lift_stats) LIMIT 10;"
    try:
        execute_and_print_sql(cursor, sql)
    except mysql.connector.ProgrammingError as err:
        if not DEBUG:
            print(f"{colored('ERROR', 'red')}: {colored(err, 'red')}")
        # sys.exit(1)
        else:
            error_string = f'An error occurred, couldn\'t do query.'
            print_error(error_string)
def pay_membership(person_id):
    cursor = conn.cursor()
    sql = "CALL pay_membership(%d)" % (person_id)
    try:
        execute_and_print_sql(cursor, sql, False)
        print_success('Success!')
    except mysql.connector.ProgrammingError as err:
        if not DEBUG:
            print(f"{colored('ERROR', 'red')}: {colored(err, 'red')}")
        # sys.exit(1)
        else:
            error_string = f'An error occurred, couldn\'t do query.'
            print_error(error_string)


def execute_and_print_sql(cursor, sql, print_table=True):
    cursor.execute(sql)
    if print_table:
        rows = cursor.fetchall()
        field_names = [i[0] for i in cursor.description]
        t = PrettyTable(field_names)
        for row in rows:
            t.add_row(list(row))
        print_success('Success!')
        print(t)
    


def print_error(error_str):
    print(colored(error_str, 'red'))

def print_success(success_str):
    print(colored(success_str, 'green'))


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
    show_options()
    # show_admin_options()


if __name__ == '__main__':
    # This conn is a global object that other functinos can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    
    main()
