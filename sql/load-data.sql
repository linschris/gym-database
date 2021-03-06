-- Load instructions for getting CSV files into your database.
LOAD DATA LOCAL INFILE 'csv/person.csv' INTO TABLE person
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'csv/member.csv' INTO TABLE member
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'csv/membership_prices.csv' INTO TABLE membership_price
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'csv/memberships.csv' INTO TABLE membership
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'csv/employee.csv' INTO TABLE employee
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'csv/employee_availability.csv' INTO TABLE employee_availability
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'csv/physique.csv' INTO TABLE physique
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'csv/sessions.csv' INTO TABLE session
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'csv/session_trainees.csv' INTO TABLE session_trainee
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'csv/session_trainers.csv' INTO TABLE session_trainer
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'csv/class.csv' INTO TABLE class
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'csv/class_instructor.csv' INTO TABLE class_instructor
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names

LOAD DATA LOCAL INFILE 'csv/class_student.csv' INTO TABLE class_student
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
IGNORE 1 ROWS; -- If your CSV file has a row with column names