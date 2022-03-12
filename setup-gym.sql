-- DROP TABLE statements

DROP TABLE member IF EXISTS member;
DROP TABLE memberships IF EXISTS memberships;
DROP TABLE person IF EXISTS person;
DROP TABLE physique IF EXISTS physique;
DROP TABLE session IF EXISTS session;
DROP TABLE class IF EXISTS class;

-- Representation of a person in our gym database.
-- A person is not special, but more of a general categorization between
-- members and employees (where we use specialization).

CREATE TABLE person (
    person_id CHAR(16) PRIMARY KEY,
    first_name VARCHAR(15),
    last_name VARCHAR(15),
    email_address VARCHAR(30),
    -- phone_num doesn't have to be strictly U.S.
    -- XXX-XXX-XXX format mainly
    phone_number VARCHAR(12)
);

-- A person who works at the gym.
-- Mainly an instructor or trainer.
CREATE TABLE employee (
    person_id CHAR(16),
    expertise VARCHAR(20),
    availablity VARCHAR(20), -- TODO: need to fix here
    job_title VARCHAR(20),

    FOREIGN KEY employee(person_id) REFERENCES person(person_id),
);

-- A person who attends the gym, classes, and does workout sessions with trainers.
-- A member MUST have a membership unlike employees.
CREATE TABLE member (
    person_id INT PRIMARY KEY,
    credit_card_no CHAR(16),
    exp_date DATE, 

    FOREIGN KEY member(person_id) REFERENCES person(person_id),
);


-- Memberships for the gym. Required to be owned by a member.
-- Price is dependent on the type and length of membership.
CREATE TABLE memberships (
    member_id INT,
    membership_type VARCHAR(10),
    price DECIMAL(6, 2), -- price <= 1000
    membership_length INT -- num of months, 1+
);


-- A representation of an instructor class.
-- Instructor teaches, members enroll in a class of a given type.
CREATE TABLE class (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(30),
    class_type VARCHAR(30),
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

-- A representation of a 1-on-1 trainer session.
-- Sessions must be between one member and one trainer (employee).
CREATE TABLE [session] (
    session_id SERIAL PRIMARY KEY,
    muscle_group VARCHAR(30),
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

-- A table of the statistics of a given person, member or employee.
-- Carries body statistics (size, weight) and person records of a client.
CREATE TABLE physique (
    height TINYINT, -- ft

    -- all weights and PRs should be in pounds
    weight INT, 
    -- personal record section
    BMI DECIMAL(3, 1), 
    squat INT,
    deadlift INT,
    bench_press INT
);

-- Employee ratings
-- 1-5 scale, works for any employee!
-- Useful information for determining most popular or least popular 
-- employees at the gym.
CREATE TABLE ratings (
    employee_id CHAR(16),
    -- rating is 1-5
    rating TINYINT

    CHECK(rating BETWEEN 1 AND 5);
    FOREIGN KEY ratings(employee_id) REFERENCES employee_id(person_id), 
);  