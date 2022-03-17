DROP USER 'gymadmin'@'localhost';
DROP USER 'gymmember'@'localhost';
-- GUEST is purely for logging in purposes. Has little logging in purpose.
DROP USER 'guest'@'localhost';

CREATE USER 'gymadmin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'gymmember'@'localhost' IDENTIFIED BY 'memberpw';
CREATE USER 'guest'@'localhost' IDENTIFIED BY 'password';


GRANT ALL PRIVILEGES ON gymDB.* TO 'gymadmin'@'localhost';
GRANT ALL PRIVILEGES ON gymDB.* TO 'gymmember'@'localhost';
GRANT ALL PRIVILEGES ON gymDB.* TO 'guest'@'localhost';

-- Don't want gym members updating info on other members (physiques, and their
-- personal info)!
GRANT SELECT ON gymDB.* TO 'gymmember'@'localhost';  


-- Allow members to pay for their memberships, give_ratings, enroll.
GRANT EXECUTE ON gymDB.* TO 'gymmember'@'localhost';

-- Allow access to whether a user is an admin or not.
GRANT SELECT ON user_info.* TO 'guest'@'localhost';

-- Allow usage of authenticate()
GRANT EXECUTE ON gymDB.* TO 'guest'@'localhost';

FLUSH PRIVILEGES;
