-- Functions
DROP FUNCTION IF EXISTS weight_status;
DROP FUNCTION IF EXISTS total_stats;

-- Procedures
DROP PROCEDURE IF EXISTS enroll_in_class_or_session;
DROP PROCEDURE IF EXISTS give_class_rating;
DROP PROCEDURE IF EXISTS give_session_rating;
DROP PROCEDURE IF EXISTS pay_membership;
DROP PROCEDURE IF EXISTS remove_member;

-- Triggers
DROP TRIGGER IF EXISTS unpaid_members;


/* UDFs */

DELIMITER !
-- BMI user defined function. Based on a user's height in inches 
-- and weight in pounds, it will return a string of a user's weight_status
CREATE FUNCTION weight_status (height INT, weight INT) 
RETURNS VARCHAR(11) DETERMINISTIC
BEGIN
    DECLARE BMI DECIMAL(4, 1); -- body mass index
    DECLARE weight_stat VARCHAR(11) DEFAULT NULL;

    -- Body mass index = [weight in pounds / (height in inches)^2] * 703
    -- Rounded to one decimal as further precision is not necessary (nor used).
    SET BMI = ROUND((weight / (height * height)) * 703, 1);

    IF BMI > 30 THEN SET weight_stat = 'Obese';
    ELSEIF BMI > 25 THEN SET weight_stat = 'Overweight';
    ELSEIF BMI > 18.5 THEN SET weight_stat = 'Healthy';
    ELSE SET weight_stat = 'Underweight';
    END IF;

    RETURN weight_stat;
END !
DELIMITER ;

DELIMITER !
-- Often to compare total strength between different body builders or 
-- power lifters, they compare by looking at the total 
-- weight of their three lifts.
CREATE FUNCTION total_stats (person_id INT) 
RETURNS INT DETERMINISTIC
BEGIN
    DECLARE person_stats INT;
    SELECT squat + deadlift + bench_press INTO person_stats
        FROM physique p WHERE person_id = p.person_id;
    RETURN person_stats;
END !
DELIMITER ;


/* Procedures */

DELIMITER !
-- enrolls a student into a class or session (based on parameter)
-- 1 = session, 2 = class
CREATE PROCEDURE enroll_in_class_or_session (
    class_or_session_id INT,
    person_id INT,
    enrollment_choice TINYINT
)
BEGIN
    DECLARE already_in_class TINYINT;
    DECLARE already_in_session TINYINT;

    -- values to check
    SET already_in_class = EXISTS(SELECT * FROM class_student cs 
    WHERE class_id = class_or_session_id AND person_id = cs.person_id);
    SET already_in_session = EXISTS(SELECT * FROM session_trainee st 
    WHERE session_id = class_or_session_id AND person_id = st.person_id);

    IF enrollment_choice = 1 AND already_in_session = 0 THEN
        INSERT INTO session_trainee VALUES
        (class_or_session_id, person_id, NULL);
    ELSEIF enrollment_choice = 2 AND already_in_class = 0 THEN
        INSERT INTO class_student VALUES
        (class_or_session_id, person_id, NULL);
    ELSE
        SELECT 'Student is already in class or session 
        OR invalid class/session.';
    END IF;
END!
DELIMITER ;


DELIMITER !
-- For a class, when a person enrolls, the rating will be NULL.
-- To give a rating (or update it), run this procedure
CREATE PROCEDURE give_class_rating (
    old_class_id INT,
    old_person_id INT,
    new_rating TINYINT
)
BEGIN
    UPDATE class_student
    SET rating = new_rating
    WHERE class_id = old_class_id AND old_person_id = person_id;
END!
DELIMITER ;

DELIMITER !
-- For a sesson, when a person enrolls, the rating will be NULL.
-- To give a rating (or update it), run this procedure.
CREATE PROCEDURE give_session_rating (
    old_session_id INT,
    old_person_id INT,
    new_rating TINYINT
)
BEGIN
    UPDATE session_trainee
    SET rating = new_rating
    WHERE session_id = old_session_id AND old_person_id = person_id;
END!
DELIMITER ;

DELIMITER !
-- Removes members given a member_id
-- Removes all sessions, classes, and info associated with them.
CREATE PROCEDURE remove_member (
    member_id INT
)
BEGIN 
    DELETE FROM session WHERE trainee_id = member_id;
    DELETE FROM class_student WHERE person_id = member_id;
    DELETE FROM member WHERE
    person_id = member_id; 
    DELETE FROM person WHERE
    person_id = member_id; 
END !
DELIMITER ;

-- Allows users to "pay" for their membership.
-- Updates last_payment to now()
DELIMITER !
CREATE PROCEDURE pay_membership (
    member_id INT
)
BEGIN 
    UPDATE membership
    SET last_payment = DATE(NOW())
    WHERE person_id = member_id;
END!
DELIMITER ;

DELIMITER !
-- When someone pays for their membership, check and see
-- if any other members have not paid for their membership by their own due
-- date!
-- If so, delete them (remove them as members).
CREATE TRIGGER unpaid_members AFTER UPDATE ON membership
FOR EACH ROW
BEGIN 
    DECLARE not_paid TINYINT DEFAULT 0;
    SET not_paid = DATE_ADD(OLD.last_payment, INTERVAL 1 MONTH) <= DATE(NOW());
    IF not_paid = 1 THEN
        CALL remove_member(OLD.person_id);
    END IF;
END !
DELIMITER ;



