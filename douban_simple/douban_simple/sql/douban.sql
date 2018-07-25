-- 创建数据库表 --

CREATE TABLE movie (
  subject int NOT NULL,
  name text NOT NULL,
  year text,
  director text,
  scenarist text,
  actor text,
  mtype text,
  country varchar(128),
  releaseDate varchar(256),
  language varchar(128),
  runtime varchar(64),
  rating text,
  name2 varchar(128),
  IMDb varchar(64),
  summary text,
  tags text,
  sposterUrl varchar(128),
  sposterPath varchar(128),
  PRIMARY KEY (subject)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE review (
  id int NOT NULL,
  subject text NOT NULL,
  title varchar(128),
  rating varchar(64),
  createAt varchar(64),
  content text,
  authorName varchar(128),
  authorId varchar(128),
  usefulCount varchar(256),
  uselessCount varchar(128),
  donateNum varchar(64),
  recNum varchar(64),
  commentsCount varchar(64),
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE people (
  id varchar(64) NOT NULL,
  name varchar(128) NOT NULL,
  signature varchar(512),
  address varchar(128),
  registerTime varchar(128),
  intro text,
  groups varchar(512),
  doulists varchar(512),
  friendNum varchar(32),
  revNum varchar(32),
  avatarUrl varchar(256),
  avatarPath varchar(256),
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;