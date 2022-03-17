'''
    Queries.py
    A file to store all the query functions we call!
    As well as, a few helper methods
'''
from termcolor import colored
from prettytable import PrettyTable
import mysql.connector
import mysql.connector.errorcode as errorcode
import sys

DEBUG = False

#----------------#
# Helper Methods #
#----------------#

def print_error(error_str):
    print(colored(error_str, 'red'))

def print_success(success_str):
    print(colored(success_str, 'green'))

def handle_error(err):
    if DEBUG:
        print(f"{colored('ERROR', 'red')}: {colored(err, 'red')}")
        sys.exit(1)
    else:
        error_string = f'An error occurred, couldn\'t do query due to the following error: \n{err}.'
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

#-----------------#
# Query Functions #
#-----------------#


def instructor_ratings(conn):
    cursor = conn.cursor()
    sql = "SELECT person_id AS instructor_id, IFNULL(AVG(rating), 'N/A') AS avg_rating, COUNT(*) AS total_classes_sessions FROM ((SELECT class_id, person_id, rating FROM employee NATURAL JOIN class_instructor NATURAL JOIN class NATURAL JOIN (SELECT class_id, rating FROM class_student) AS class_ratings UNION SELECT session_id AS class_id, trainer_id AS person_id, rating FROM session)) AS ratings GROUP BY instructor_id ORDER BY avg_rating DESC;"
    try:
        execute_and_print_sql(cursor, sql)
    except mysql.connector.ProgrammingError as err:
        handle_error(err)
        

def leaderboard_query(conn):
    cursor = conn.cursor()
    sql = "WITH total_stats AS (SELECT first_name, last_name, total_stats(person_id) AS total_lift_stats FROM physique NATURAL JOIN person) SELECT COUNT(ts.total_lift_stats) AS `rank`, CONCAT(ts.first_name, ' ', SUBSTRING(ts.last_name, 1, 1), '.') AS `name`, ts.total_lift_stats FROM total_stats ts, total_stats t WHERE ts.total_lift_stats < t.total_lift_stats GROUP BY ts.first_name, ts.last_name, ts.total_lift_stats ORDER BY COUNT(ts.total_lift_stats) LIMIT 10;"
    try:
        execute_and_print_sql(cursor, sql)
    except mysql.connector.ProgrammingError as err:
        handle_error(err)


def select_query(conn, relation_name=None, where=None):
    cursor = conn.cursor()
    if not relation_name:
        print("Invalid, nothing to select.")
    else:
        where_clause = where if where else ''
        sql = "SELECT * FROM %s %s;" % (relation_name, where_clause)
        try:
            execute_and_print_sql(cursor, sql)
        except mysql.connector.ProgrammingError as err:
            handle_error(err)


def pay_membership(conn, person_id):
    cursor = conn.cursor()
    sql = "CALL pay_membership(%d)" % (person_id)
    try:
        execute_and_print_sql(cursor, sql, False)
        print_success('Success!')
    except mysql.connector.ProgrammingError as err:
        handle_error(err)

def fire_person(conn, person_id):
    pass

def enroll_in_class(conn, person_id, class_id):
    cursor = conn.cursor()
    sql = "CALL enroll_in_class_or_session(%s, %s, 2)" % (class_id, person_id)
    try:
        execute_and_print_sql(cursor, sql, False)
        print_success('Success!')
    except mysql.connector.ProgrammingError as err:
        handle_error(err)

# cs_id = class or session id
def rate_class_or_session(conn, cs_id, person_id, rating, num_choice):
    cursor = conn.cursor()
    procedure_name = 'give_class_rating' if num_choice == 2 else 'give_session_rating'
    sql = "CALL %s(%s, %s, %s);" % (procedure_name, cs_id, person_id, rating)
    try:
        execute_and_print_sql(cursor, sql, False)
        print_success('Success!')
    except mysql.connector.ProgrammingError as err:
        handle_error(err)


def fire_employee_or_member(conn, person_id, is_employee):
    cursor = conn.cursor()
    sql = 'CALL fire_employee(%s)' % (person_id) if is_employee else 'CALL remove_member(%s)' % (person_id)
    try:
        execute_and_print_sql(cursor, sql, False)
        print_success('Success!')
    except mysql.connector.ProgrammingError as err:
        handle_error(err)