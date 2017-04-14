# GymnasistsAssistant2
v2.0 of Gymnasist's Assistant Telegram Chat-Bot  
MySQL Settings:  
```
CREATE USER 'bot'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE main;
USE main;
CREATE TABLE main(chatid INT unsigned NOT NULL, status TINYINT unsigned NULL, class varchar (255) DEFAULT 0)ENGINE=InnoDB;
CREATE TABLE lost(item varchar(255) NOT NULL)ENGINE=InnoDB;
CREATE TABLE events(name varchar(255) NOT NULL, date DATE NOT NULL, desc varchar(255) NOT NULL)ENGINE=InnoDB;
```
