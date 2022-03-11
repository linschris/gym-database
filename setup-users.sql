CREATE USER 'gymadmin'@'localhost' IDENTIFIED BY 'adminpw';
CREATE USER 'gymmember'@'localhost' IDENTIFIED BY 'memberpw';

GRANT ALL PRIVILEGES ON gymDB.* TO 'gymadmin'@'localhost';

FLUSH PRIVILEGES;