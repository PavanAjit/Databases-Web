use project1;

SET FOREIGN_KEY_CHECKS = 0;
drop table if exists BUILDING;
drop table if exists MEDIA;
drop table if exists ROOM;
drop table if exists ROOMMEDIA;
SET FOREIGN_KEY_CHECKS = 1;

create table BUILDING (
  bcode varchar(6),
  bname varchar(30),
  primary key (bcode)
);

create table MEDIA (
  mcode varchar(6),
  description varchar(50),
  primary key (mcode)
);

create table ROOM (
  bcode varchar(6),
  rnumber varchar(4),
  cap int,
  layout varchar(20),
  type enum ('P','G'),
  dept varchar(4),
  primary key (bcode,rnumber),
  foreign key (bcode) references BUILDING(bcode)
);

create table ROOMMEDIA (
  bcode varchar(6),
  rnumber varchar(4),
  mcode varchar(6),
  primary key (bcode,rnumber,mcode),
  foreign key (bcode,rnumber) references ROOM(bcode,rnumber),
  foreign key (mcode) references MEDIA(mcode)
);

