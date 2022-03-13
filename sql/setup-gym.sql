-- DROP TABLE statements


DROP TABLE IF EXISTS class_ratings;
DROP TABLE IF EXISTS class_instructors;
DROP TABLE IF EXISTS class_students;
DROP TABLE IF EXISTS class;
DROP TABLE IF EXISTS session;
DROP TABLE IF EXISTS membership_prices;
DROP TABLE IF EXISTS memberships;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS employee_availabilities;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS physique;
DROP TABLE IF EXISTS person;



-- Representation of a person in our gym database.
-- A person is more of a general categorization between
-- members and employees (where we use specialization).

CREATE TABLE person (
    person_id INT PRIMARY KEY,
    first_name VARCHAR(15) NOT NULL,
    last_name VARCHAR(15) NOT NULL,
    -- youremail@example.com
    email_address VARCHAR(30),
    -- XXX-XXX-XXX format
    phone_number CHAR(9)
);

-- A table of the statistics of a given person, member or employee.
-- Carries body statistics (size, weight) and person records of a client.
CREATE TABLE physique (
    person_id INT, 
    time_updated TIMESTAMP,
    height TINYINT NOT NULL, -- ft
    -- all weights and PRs should be in pounds
    weight INT NOT NULL, 
    BMI DECIMAL(3, 1) NOT NULL, -- Body Mass Index
    -- personal record section
    -- can be NULL as possible someone has not done one of the lifts
    squat INT,
    deadlift INT,
    bench_press INT,

    PRIMARY KEY(person_id, time_updated),
    FOREIGN KEY physique(person_id) REFERENCES person(person_id)
    ON DELETE CASCADE
);


-- A person who works, teaches, or trains others at the gym.
-- Mainly an instructor or trainer, but specified by a job title.
-- Employees are not broken down into instructors and trainers, 
-- as they are very similar to each other and often overlap.

CREATE TABLE employee (
    person_id INT PRIMARY KEY,
    job_title VARCHAR(20) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    -- What they know how to train best: upper body, cardio, etc.
    expertise VARCHAR(20), 

    FOREIGN KEY employee(person_id) REFERENCES person(person_id)
);

-- Availabilities for employees. Shows the schedule and what times
-- an instructor/trainer is available for sessions or classes.
CREATE TABLE employee_availabilities (
    employee_id INT PRIMARY KEY,
    from_time TIMESTAMP NOT NULL,
    to_time TIMESTAMP NOT NULL,

    FOREIGN KEY employee_availabilities(employee_id) REFERENCES 
        employee(person_id) ON DELETE CASCADE
);

-- A person who attends the gym, classes, and does workout sessions with trainers.
-- A member MUST have a membership unlike employees.
CREATE TABLE member (
    person_id INT PRIMARY KEY,
    credit_card_no CHAR(16), 
    exp_date DATE, 

    FOREIGN KEY member(person_id) REFERENCES person(person_id)
);


-- Memberships for the gym currently own by a member.
-- Memberships are monthly only.
-- Price is dependent on the type of membership, refer to membership_prices.
CREATE TABLE memberships (
    member_id INT,
    membership_type VARCHAR(10), -- Either classic or premium

    -- most recent payment from member for month of membership
    -- update upon subsequent payments from members.
    last_payment TIMESTAMP,

    -- a member can only have one type of membership
    PRIMARY KEY (member_id, membership_type), 
    FOREIGN KEY membership(member_id) REFERENCES member(person_id)
    ON DELETE CASCADE
);

-- Displays prices for memberships.
-- Avoid redundancy of prices (in a column) in memberships.
CREATE TABLE membership_prices (
    membership_type VARCHAR(10),
    price DECIMAL(5, 2), 

    PRIMARY KEY (membership_type, price) 
);

-- A representation of an instructor class.
-- Instructor teaches, members enroll in a class of a given type.
-- Unlike sessions, you can have 1+ instructor and 0+ students
CREATE TABLE class (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(30),
    class_type VARCHAR(30), -- could be yoga, HIIT, upperbody, etc.
    start_time TIMESTAMP,
    end_time TIMESTAMP
);

-- Shows what classes are taught by what instructors.
CREATE TABLE class_instructors (
    instructor_id INT, 
    class_id BIGINT UNSIGNED,

    PRIMARY KEY (instructor_id, class_id),
    FOREIGN KEY class_instructors(instructor_id) REFERENCES employee(person_id),
    FOREIGN KEY class_instructors(class_id) REFERENCES class(class_id)
);

-- Shows what classes are enrolled by what gymgoers (or gym "students").
CREATE TABLE class_students (
    student_id INT, 
    class_id BIGINT UNSIGNED,

    PRIMARY KEY (student_id, class_id),
    FOREIGN KEY class_instructors(student_id) REFERENCES member(person_id),
    FOREIGN KEY class_instructors(class_id) REFERENCES class(class_id)
);

-- Ratings for the individual class sessions by members only.
CREATE TABLE class_ratings (
    class_id BIGINT UNSIGNED,
    rating TINYINT, -- 1-5, comes from member

    PRIMARY KEY (class_id), 
    FOREIGN KEY class_ratings(class_id) REFERENCES class(class_id),
    CHECK(rating BETWEEN 1 AND 5)
);

-- A representation of a 1-on-1 trainer session.
-- Sessions must be between only one member and one trainer (employee).
CREATE TABLE session (
    session_id SERIAL PRIMARY KEY, 
    trainer_id INT NOT NULL,
    trainee_id INT NOT NULL, 
    session_type VARCHAR(30) NOT NULL, -- could be yoga, HIIT, upperbody, etc.
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    rating TINYINT, -- must be 1-5, and comes from member
    
    -- a trainer nor trainee can have 2 1-1 sessions at the same time.
    UNIQUE (trainer_id, start_time), 
    UNIQUE (trainee_id, start_time),
    CHECK(rating BETWEEN 1 AND 5),

    FOREIGN KEY session(trainer_id) REFERENCES employee(person_id),
    FOREIGN KEY session(trainee_id) REFERENCES member(person_id),
    CHECK(rating BETWEEN 1 AND 5)
);

-- Indices: justified in part B
