CREATE TABLE vehicles(
  id serial not null,
  prefix varchar(50) not null,
  name varchar(200),
  "group" varchar(50) null,
  CONSTRAINT vids_pkey PRIMARY KEY (id)
)




