
-- Create a database and then create these tables into that database.

-- raxoweb.ContactUs definition

CREATE TABLE `ContactUs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(80) DEFAULT NULL,
  `lastname` varchar(80) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile_no` bigint DEFAULT NULL,
  `message` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
)


-- raxoweb.ResetHash definition

CREATE TABLE `ResetHash` (
  `hash_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `hash` varchar(200) NOT NULL,
  PRIMARY KEY (`hash_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `hash` (`hash`)
)


-- raxoweb.users definition

CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `public_id` varchar(100) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `admin` tinyint(1) DEFAULT '0',
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `public_id` (`public_id`),
  UNIQUE KEY `email` (`email`)
)

-- raxoweb.validate_code definition

CREATE TABLE `validate_code` (
  `code_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `code` int DEFAULT NULL,
  `expiretime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`code_id`),
  UNIQUE KEY `email` (`email`)
)

