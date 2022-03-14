import pandas as pd
from faker import Faker
from collections import defaultdict
import random as r
import os
from constants import NUM_SESSIONS, NUM_TOTAL_PEOPLE, NUM_TOTAL_EMPLOYEES, NUM_CLASSES

fake = Faker()

'''
    Point of this file is to generate the data which can be generated
    column for column rather than row by row.
'''

def create_default_dict(data, start=1, end=20):
    '''
        Generates fake data based on a given range of possiblities
        for each attribute.

        Not used for all data as some attributes cannot be generated
        by column (e.g. BMI needs height and weight).

        Data: dict
        Start: start number of row (e.g. person_id = 1)
        End: end number of row (e.g. person_id = 20)
    '''
    new_dict = defaultdict(list)
    for column in data.keys():
        possible_data = data[column]
        for i in range(start, end+1):
            if possible_data == 'id': # integer delimeter (like id)
                new_dict[column].append(i)
            elif isinstance(possible_data, tuple): # random int between (including endpoints) (a, b)
                new_dict[column].append(r.randint(possible_data[0], possible_data[1]))
            elif isinstance(possible_data, dict): # times
                start_time = fake.date_time_this_month(possible_data['start_time'][1], possible_data['start_time'][2])
                end_time = start_time.replace(hour = min(start_time.hour + r.randint(possible_data['window'][0], possible_data['window'][1]), 23))
                new_dict["start_time"].append(start_time)
                new_dict["end_time"].append(end_time)
            elif not isinstance(possible_data, list): # not a list, just add the value
                new_dict[column].append(possible_data)
            else:
                print(type(possible_data))
                if possible_data[0] == 'month':
                    new_dict[column].append(fake.date_time_this_month(possible_data[1], possible_data[2]))
                else:
                    new_dict[column].append(possible_data[r.randint(0, len(possible_data) - 1)])
    return new_dict

def create_csv(dict, dict_name, index=False):
    '''
        Creates a CSV from a default dictionary.
        Index specifies whether we want a number delimeter (or tuples to be specified by a number).
    '''
    dataframe = pd.DataFrame(dict)
    create_csv_directory()
    file_path = os.path.join('csv', f'{dict_name}.csv')
    dataframe.to_csv(file_path, index=index)

def create_csv_directory():
    try:
        os.mkdir('csv')
    except OSError:
        print("CSV Directory Creation Failure. Usually, means csv sub directory was already made.") 
    else:
        print("Created csv sub-dir.")



session_data = {
    'session_id': 'id',
    'session_type': ['Upper Body', 'Chest', 'Back', 'Legs', 'Lower Body', 'Cardio'],
    'time': {
        'start_time': ['month', True, True], # before and after now()
        'window': (1, 3)
    }
}

session_trainers = {
    'session_id': 'id',
    'person_id': (NUM_TOTAL_PEOPLE - NUM_TOTAL_EMPLOYEES, NUM_TOTAL_PEOPLE)
}

session_trainees = {
    'session_id': 'id',
    'person_id': (1, NUM_TOTAL_PEOPLE - NUM_TOTAL_EMPLOYEES),
    'rating': (1,5)
}

fake_employee_data = {
    'person_id': 'id',
    'job_title': ['Instructor', 'Trainer', 'Receptionist', 'Scheduler'],
    'salary': (1000, 100000),
    'expertise': ['Chest', 'Back', 'Legs', 'Upper Body', 'Lower Body', 'Calisthenics', 'Cardio'],   
}

fake_employee_ava = {
    'person_id': 'id',
    'time': {
        'start_time': ['month', False, True],
        'window': (1, 4)
    }
}

fake_class_instructors = {
    'class_id': 'id',
    'person_id': (NUM_TOTAL_PEOPLE - NUM_TOTAL_EMPLOYEES, NUM_TOTAL_PEOPLE)
}

fake_membership_data = {
    "person_id": 'id',
    "membership_type": ['Classic', 'Premium'],
    "last_payment": ['month', True, True] # times before now()
}

create_csv(create_default_dict(session_data, end=NUM_SESSIONS), 'sessions')
create_csv(create_default_dict(session_trainees, end=NUM_SESSIONS), 'session_trainees')
create_csv(create_default_dict(session_trainers, end=NUM_SESSIONS), 'session_trainers')
create_csv(create_default_dict(fake_employee_data, NUM_TOTAL_PEOPLE - NUM_TOTAL_EMPLOYEES, NUM_TOTAL_PEOPLE), 'employee')
create_csv(create_default_dict(fake_employee_ava, NUM_TOTAL_PEOPLE - NUM_TOTAL_EMPLOYEES, NUM_TOTAL_PEOPLE), 'employee_availability')
create_csv(create_default_dict(fake_membership_data, end=NUM_TOTAL_PEOPLE - NUM_TOTAL_EMPLOYEES), 'memberships')
create_csv(create_default_dict(fake_class_instructors, end=NUM_CLASSES), 'class_instructor')



