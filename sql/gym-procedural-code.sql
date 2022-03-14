
DROP FUNCTION IF EXISTS weight_status;
DELIMITER !
-- BMI user defined function. Based on a user's height in inches 
-- and weight in pounds, it will return a string of a user's weight_status
CREATE FUNCTION weight_status (height INT, weight INT) 
RETURNS VARCHAR(11) DETERMINISTIC
BEGIN
    DECLARE BMI DECIMAL(4, 1); -- body mass index
    DECLARE weight_stat VARCHAR(11) DEFAULT NULL;

    -- Body mass index = [weight in pounds / (height in inches)^2] * 703
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
-- Based on a given due_date, we can calculate the due date for the payment
-- of the next month of membership.
CREATE FUNCTION next_payment_due_date (due_date TIMESTAMP) 
RETURNS VARCHAR(11) DETERMINISTIC
BEGIN
    DECLARE next_due_date TIMESTAMP; -- body mass index
    -- Body mass index = [weight in pounds / (height in inches)^2] * 703
    SET next_due_date = ROUND((weight / (height * height)) * 703, 1);

    IF BMI > 30 THEN SET weight_stat = 'Obese';
    ELSEIF BMI > 25 THEN SET weight_stat = 'Overweight';
    ELSEIF BMI > 18.5 THEN SET weight_stat = 'Healthy';
    ELSE SET weight_stat = 'Underweight';
    END IF;

    RETURN weight_stat;
END !
DELIMITER ;


SELECT person_id AS instructor_id, AVG(rating) AS avg_rating, COUNT(class_id) AS num_class_taught 
FROM employee NATURAL JOIN class_instructor NATURAL JOIN class NATURAL JOIN (SELECT class_id, rating FROM class_student) AS classes GROUP BY person_id;