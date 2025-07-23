-- public."group" definition

-- Drop table

-- DROP TABLE public."group";

CREATE TABLE public."group" (
	"name" varchar(50) NULL,
	description varchar(256) NULL,
	id serial4 NOT NULL,
	CONSTRAINT group_pkey PRIMARY KEY (id)
);