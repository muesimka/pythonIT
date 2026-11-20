CREATE DATABASE IF NOT EXISTS academy
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE academy;

CREATE TABLE IF NOT EXISTS users (
  id INT NOT NULL AUTO_INCREMENT,
  email VARCHAR(254) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email_UNIQUE (email)
);

-- Необязательная таблица классов, используемая методами Database.
CREATE TABLE IF NOT EXISTS classes (
  id INT NOT NULL AUTO_INCREMENT,
  class_name VARCHAR(255) NOT NULL,
  places INT NOT NULL,
  PRIMARY KEY (id)
);
