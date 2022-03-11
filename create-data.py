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

fake = Faker()

people = defaultdict(list)
members = defaultdict(list)
employees = defaultdict(list)
physiques = defaultdict(list)

# create fake people
for num in range(1, 150):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email_address = f'{first_name}{last_name}@{fake.domain_name()}'

    people["person_id"].append(num) # TODO: if necessary, not use just incrementing num
    people["first_name"].append(first_name)
    people["last_name"].append(last_name)
    people["email_address"].append(email_address)
    people["phone_number"].append(fake.phone_number())

# create fake members
for num in range(135):
    members["person_id"].append(num) # TODO: if necessary, not use just incrementing num
    # fake payment info
    members["credit_card_no"].append(fake.credit_card_number())
    members["exp"].append(fake.credit_card_expire())

fake_expertises = ['Chest', 'Back', 'Legs', 'Upper Body', 'Lower Body', 'Calisthenics', 'Cardio']
fake_job_titles = ['Instructor', 'Trainer', 'Receptionist', 'Manager']

# create fake employees
for num in range(135, 151):
    employees["person_id"].append(num) # TODO: if necessary, not use just incrementing num
    employees["job_title"].append(fake_job_titles[r.randint(0, len(fake_job_titles) - 1)])
    employees["expertise"].append(fake_expertises[r.randint(0, len(fake_expertises) - 1)])

# create fake physiques
for i in range(1, 100):
    physiques["person_id"].append(r.randint(0, 150)) # TODO: if necessary, not use just incrementing num
    # fake physique info
    fake_height = r.randint(36, 100) # inches
    fake_weight = r.randint(80, 400)
    # BMI is calculated as lb / inches^2
    fake_bmi = round((fake_weight / (fake_height ** 2)) * 703, 1)

    physiques["height"].append(fake_height)
    physiques["weight"].append(fake_weight)
    physiques["bmi"].append(fake_bmi)
    physiques["squat"].append(r.randint(45, 1000))
    physiques["bench_press"].append(r.randint(45, 1000))
    physiques["deadlift"].append(r.randint(45, 1000))

# create fake 



# creates all the dataframes and csvs for this fake data to use in mySQL!
def create_csv(dict, dict_name):
    dataframe = pd.DataFrame(dict)
    dataframe.to_csv(f'{dict_name}.csv', index=False)

create_csv(people, 'person')
create_csv(physiques, 'physique')
create_csv(employees, 'employee')
