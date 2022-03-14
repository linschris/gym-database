'''
    Creates the data for my database final project.
    Not completely original, refer to 
    https://towardsdatascience.com/generating-random-data-into-a-database-using-python-fd2f7d54024e
'''

import math
import pandas as pd
from faker import Faker
from collections import defaultdict
import random as r
from constants import *
from create_col_data import create_csv

fake = Faker()
people = defaultdict(list)
members = defaultdict(list)
physiques = defaultdict(list)
membership_prices = defaultdict(list)
classes = defaultdict(list)
class_student = defaultdict(list)
class_rating = defaultdict(list)

membership_types = ['Classic', 'Premium']
membership_price = [20.35, 40.55]




'''
    Creates fake people.
'''
for num in range(1, NUM_TOTAL_PEOPLE):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email_address = f'{first_name}{last_name}@{fake.domain_name()}'

    people["person_id"].append(num)
    people["first_name"].append(first_name)
    people["last_name"].append(last_name)
    people["email_address"].append(email_address)
    people["phone_number"].append(f'{r.randint(100, 999)}-{r.randint(100, 999)}-{r.randint(100, 999)}')

'''
    Creates fake members.
'''
for num in range(1, NUM_TOTAL_PEOPLE - NUM_TOTAL_EMPLOYEES):
    members["person_id"].append(num) # TODO 
    # fake payment info
    members["credit_card_no"].append(fake.credit_card_number())
    random_month = r.randint(1, 12)
    members["exp"].append(f'{r.randint(2022, 2035)}-{fake.month()}-01')

'''
    Creates fake physqiues (body stats and PRs).
'''
for i in range(1, NUM_PHYSIQUES):
    physiques["person_id"].append(r.randint(1, NUM_TOTAL_PEOPLE-1)) # TODO: if necessary, not use just incrementing num
    physiques["time_updated"].append(fake.date_this_year())
    # fake physique info
    fake_height = r.randint(36, 100) # inches
    fake_weight = r.randint(80, 400)
    # BMI is calculated as lb / inches^2
    fake_bmi = round((fake_weight / (fake_height ** 2)) * 703, 1)

    physiques["height"].append(fake_height)
    physiques["weight"].append(fake_weight)
    # physiques["bmi"].append(fake_bmi)
    physiques["squat"].append(r.randint(45, 1000))
    physiques["bench_press"].append(r.randint(45, 1000))
    physiques["deadlift"].append(r.randint(45, 1000))

'''
    Generates membership_prices table (to get prices of memberships).
'''
for membership_type in membership_types:
    membership_prices["membership_type"].append(membership_type)
for membership_pr in membership_price:
    membership_prices["price"].append(membership_pr)

# Classes

possible_class_types = ['HIIT', 'Upper Body', 'Legs', 'Abs', 'Yoga']
for i in range(NUM_CLASSES):
    fake_start_time = fake.date_time_this_month(True, True)
    fake_end_time = fake_start_time.replace(hour = min(fake_start_time.hour + 1, 23))
    fake_class_type = possible_class_types[r.randint(0, len(possible_class_types)-1)]
    does_rate_class = True if r.randint(0, 1) == 1 else False

    classes["class_id"].append(i)
    classes["class_name"].append(f'{fake_class_type} at {fake_start_time.time()}')
    classes["class_type"].append(fake_class_type)
    classes["start_time"].append(fake_start_time)
    classes["end_time"].append(fake_end_time)

# Class Students

for i in range(NUM_ENROLLMENTS):
    random_num = r.randint(1, 2)
    random_student = r.randint(0, 134)
    random_class = r.randint(0, 20)
    class_student["student_id"].append(random_student)
    class_student["class_id"].append(random_class)
    # print(random_num)
    class_student["rating"].append(r.randint(1, 5) if random_num == 1 else 'NULL')
    # print(class_student["rating"])

create_csv(people, 'person')
create_csv(physiques, 'physique')
create_csv(members, 'member')
create_csv(membership_prices, 'membership_prices')
create_csv(classes, 'class')
create_csv(class_student, 'class_student')