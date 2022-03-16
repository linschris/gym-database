DROP USER 'gymadmin'@'localhost';
DROP USER 'gymmember'@'localhost';

CREATE USER 'gymadmin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'gymmember'@'localhost' IDENTIFIED BY 'memberpw';

-- As a gym admin (like an owner or employee), 
-- you have access to all information.
GRANT ALL PRIVILEGES ON gymDB.* TO 'gymadmin'@'localhost';

-- Don't want gym members updating info on other members (physiques, and their
-- personal info)!
GRANT SELECT ON gymDB.* TO 'gymmember'@'localhost';  


-- Allow members to pay for their memberships, give_ratings, enroll.
GRANT EXECUTE ON gymDB.* TO 'gymmember'@'localhost';


FLUSH PRIVILEGES;
