SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(500) NOT NULL,
  role varchar(10) not null
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `club` (
  `cid` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  president varchar(20) not null,
  number_of_members int(3),
  description varchar(100) not null,
  vision text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table event(
  eid int auto_increment primary key,
  EventName varchar(20) not null,
  date_of_conduct date not null,
  eventc varchar(20),
  image blob,
  hedline text
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `student` (
  `id` int(11) NOT NULL,
  `rollno` varchar(20) NOT NULL,
  `sname` varchar(50) NOT NULL,
  `sem` int(20) NOT NULL,
  `gender` varchar(50) NOT NULL,
  `branch` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `number` varchar(12) NOT NULL,
  `address` text NOT NULL,
  cid int foreign key references club
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

create table event_participation(cid int,rollno varchar(20),name varchar(30),constraint pk primary key(cid,rollno), constraint fk foreign key(cid) references club(cid),constraint fks foreign key (rollno) references student(rollno),constraint fka foreign key(name) references alumni(name));

 create table alumni(name varchar(30),email varchar(30),designation varchar(100),linkdin varchar(50),photo blob,
 company varchar(100),about varchar(100), constraint pka primary key(name,email));

create table club_participation(cid int,rollno varchar(20),constraint pk primary key(cid,rollno), constraint fkce foreign key(cid) references club(cid),constraint fkc foreign key (rollno) references student(rollno));

  