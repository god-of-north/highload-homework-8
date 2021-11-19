CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    login VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,

    Name VARCHAR(255) NOT NULL,
    Surname VARCHAR(255) NOT NULL,
    Patronymic VARCHAR(255) NOT NULL,

    birth_day DATE,
    registration_date DATE,

    status TINYINT NOT NULL,
    priority TINYINT NOT NULL,
    description TEXT,

)  ENGINE=INNODB;

CREATE INDEX btree_index USING BTREE ON tasks (birth_day);
CREATE INDEX hash_index USING HASH ON tasks (registration_date);

OPTIMIZE TABLE users;
