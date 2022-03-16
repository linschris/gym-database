
-- Employee Overall Ratings
-- Grabs the avg rating for an employee who has had classes and/or sessions
-- If in all the classes they taught, no one rated them, labeled 'N/A'
SELECT person_id AS instructor_id, IFNULL(AVG(rating), 'N/A') AS avg_rating,
COUNT(*) AS total_classes_sessions FROM (
    (SELECT class_id, person_id, rating
    FROM employee NATURAL JOIN class_instructor NATURAL JOIN class 
    NATURAL JOIN (SELECT class_id, rating FROM class_student) AS class_ratings
    UNION
    SELECT
    session_id AS class_id, trainer_id AS person_id, rating
    FROM session)
) AS ratings
GROUP BY instructor_id ORDER BY avg_rating DESC;

-- Physique Top 10 Leaderboard
-- Grabs the top 10 people, who have the strongest total
-- lift stats (bench, squat, deadlift) and ranks them!
-- uses UDF total_stats!
WITH total_stats AS (
    SELECT first_name, last_name, total_stats(person_id) AS total_lift_stats
    FROM physique NATURAL JOIN person
)
SELECT COUNT(ts.total_lift_stats) AS `rank`, 
CONCAT(ts.first_name, ' ', SUBSTRING(ts.last_name, 1, 1), '.') AS `name`, 
ts.total_lift_stats FROM total_stats ts, total_stats t
WHERE ts.total_lift_stats < t.total_lift_stats
GROUP BY ts.first_name, ts.last_name, ts.total_lift_stats
ORDER BY COUNT(ts.total_lift_stats) LIMIT 10;


-- Employee Availabilities
-- Displays employee info, their available window, and contact info.
SELECT first_name, last_name, expertise, 
email_address, phone_number, start_time, end_time
FROM employee NATURAL JOIN employee_availability NATURAL JOIN person;

-- Session/Class Available Times
-- Parameters from Query As Strings
-- For command line app, will compute both queries and combine them!
SELECT * FROM class
WHERE start_time >= 'Input Start Time Stamp' 
AND end_time <= 'Input End Time Stamp'

SELECT * FROM session
WHERE start_time >= 'Input Start Time Stamp' 
AND end_time <= 'Input End Time Stamp';

-- Example Queries
SELECT * FROM class
WHERE start_time >= '2022-03-25 12:01:36' 
AND end_time <= '2022-03-30 17:01:36';

SELECT * FROM session
WHERE start_time >= '2022-03-25 12:01:36' 
AND end_time <= '2022-03-25 17:01:36';

-- Trainer Weakest/Strongest Lift
-- Useful for determining what trainer a person may need
-- NOTE: person_id is inputed from CLI
WITH weakest_lift AS (
    SELECT person_id, time_updated, LEAST(squat, deadlift, bench_press)
    AS weakest_lift
    FROM physique
    WHERE person_id = 148
),
expertise_needed AS (
    SELECT 
    CASE
        WHEN squat = weakest_lift THEN 'Lower Body'
        WHEN deadlift = weakest_lift THEN 'Lower Body'
        ELSE 'Upper Body'
    END AS expertise
    FROM physique NATURAL JOIN weakest_lift
)
SELECT DISTINCT * FROM expertise_needed NATURAL JOIN employee;

-- Grabs all known people and their stats/physiques
SELECT DISTINCT CONCAT(first_name, ' ', last_name) AS 
full_name, squat, deadlift, bench_press FROM person 
NATURAL JOIN physique NATURAL JOIN session;
