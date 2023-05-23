create database qustomate;

use qustomate;

CREATE TABLE user (
    id_user INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    email VARCHAR(25) UNIQUE NOT NULL,
    password VARCHAR(20) NOT NULL,
    role VARCHAR(6) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    isActive BOOLEAN NOT NULL
);

INSERT INTO user (id_user, email, password, role,phone, isActive) VALUES (1,'test@gmail.com','001','admin','081220952593',true);