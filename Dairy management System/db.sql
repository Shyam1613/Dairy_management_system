CREATE DATABASE farm;

create table admin(
  name varchar(10),
  passwd varchar(10),
  constraint pa primary key(name));

insert into admin values('root','server');

create table staff(
  staffid integer,
  name varchar(10),
  passwd varchar(10),
  salary integer,
  joindate date,
  constraint ps1 primary key(staffid));

create table seller(
  sellid integer,
  name varchar(10),
  passwd varchar(10),
  cattle varchar(10),
  address varchar(20),
  constraint ps2 primary key(sellid));  

  create table bill(
  bid integer,
  sellid integer,
  staffid integer,
  bdate date,
  amount integer,
  no_of_container integer,
  time varchar(10),
  constraint pb primary key(bid),
  constraint fb1 foreign key(sellid)references seller(sellid)on DELETE set NULL,
  constraint fb2 foreign key(staffid)references staff(staffid)on DELETE set NULL);

create table container(
  container_id integer,
  sellid integer,
  staffid integer,
  submit date,
  fat float(6),
  collected varchar(5),
  bid integer,
  constraint pc primary key(container_id),
  constraint fc1 foreign key(sellid)references seller(sellid)on DELETE set NULL,
  constraint fc2 foreign key(bid)references bill(bid)on DELETE set NULL,
  constraint fc3 foreign key(staffid)references staff(staffid)on DELETE set NULL);
 

DELIMITER $$

    CREATE TRIGGER notcollect BEFORE INSERT ON `container`
    FOR EACH ROW
     BEGIN
      IF (NEW.collected IS NULL OR NEW.collected = 'no') THEN
        SET new.staffid=Null;
      END IF;
    END$$

DELIMITER ;


DELIMITER &&

CREATE PROCEDURE get_bill (IN var1 INT)
BEGIN
  SELECT * FROM bill WHERE staffid IS NOT NULL
END &&

DELIMITER;

