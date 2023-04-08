CREATE DATABASE nckh;
USE nckh;

CREATE table web (
		id INT NOT NULL PRIMARY KEY auto_increment,
		title VARCHAR(255),
		link VARCHAR(255),
		published VARCHAR(255)
);

SET SQL_SAFE_UPDATES = 0;

CREATE TABLE setting(
	name VARCHAR(255),
	time INT);

INSERT into setting (name, time) VALUES ('admin', 120);

select * from web;
