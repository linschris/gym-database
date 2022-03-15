'''

Constants.py

These contain the constants used to generate the data for the gym database.
A quick note is that while these are constants, because the data is generated
randomly, that not all records (e.g. enrollments) may not make it when loading
into SQL because the random data may end up breaking a primary key, foriegn
key, or check constraint.

'''
NUM_TOTAL_PEOPLE = 150 # num of records in person relation
NUM_PHYSIQUES = 100 # num of physiques
NUM_TOTAL_EMPLOYEES = 15 
NUM_CLASSES = 30 # in this month after now()
NUM_ENROLLMENTS = 500 # total enrollments, across all classes
NUM_SESSIONS = 15 # in this month after now()



