-- DROP TABLE statements

DROP TABLE member IF EXISTS member;
DROP TABLE memberships IF EXISTS memberships;
DROP TABLE person IF EXISTS person;
DROP TABLE physique IF EXISTS physique;
DROP TABLE session IF EXISTS session;
DROP TABLE class IF EXISTS class;

-- Representation of a person in our gym database.
-- 
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

);

-- A person who goes to the gym.
CREATE TABLE member (
    person_id INT PRIMARY KEY,
    credit_card_no CHAR(16),
    exp_date DATE, 

    FOREIGN KEY purchaser(person_id) REFERENCES person(person_id),
);

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

CREATE TABLE [session] (
    session_id SERIAL PRIMARY KEY,
    muscle_group VARCHAR(30),
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

CREATE TABLE physique (
    height TINYINT, -- ft
    -- all weights and PRs should be in pounds
    weight INT, -- lbs
    -- personal record section
    squat INT,
    deadlift INT,
    bench_press INT
);
