CREATE TABLE IF NOT EXISTS user_details (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255),
    email VARCHAR(255),
    user_password VARCHAR(255),
    secret_key VARCHAR(255)
) AUTO_INCREMENT = 1000;

CREATE TABLE IF NOT EXISTS reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    File_name VARCHAR(255),
    note VARCHAR(255),
    file_data LONGBLOB,
    FOREIGN KEY (user_id) REFERENCES user_details(user_id)
);