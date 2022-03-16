CREATE USER 'gymadmin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'gymmember'@'localhost' IDENTIFIED BY 'memberpw';

-- As a gym admin (like an owner or employee), 
-- you have access to all information.
GRANT ALL PRIVILEGES ON gymDB.* TO 'gymadmin'@'localhost';

-- Don't want gym members seeing info on other members (physiques, and their
-- personal info) or sessions (as they are meant to be private)
GRANT SELECT ON gymDB.employee,
gymDB.employee_availability, gymDB.class,
gymDB.membership_price, gymDB.sessions
TO 'gymmember'@'localhost';

-- Allow members to pay for their memberships.
GRANT EXECUTE ON gymDB.pay_membership TO 'gymmember'@'localhost';

-- Allow members to give ratings to their classes.
GRANT EXECUTE ON gymDB.give_class_rating TO 'gymmember'@'localhost';
GRANT EXECUTE ON gymDB.give_session_rating TO 'gymmember'@'localhost';

-- Allow members to enroll in a class or session.
GRANT EXECUTE ON gymDB.enroll_in_class_or_session TO 'gymmember'@'localhost';




FLUSH PRIVILEGES;