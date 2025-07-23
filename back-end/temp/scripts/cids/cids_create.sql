-- public.cids definition

-- Drop table

-- DROP TABLE public.cids;

CREATE TABLE public.cids (
	cod varchar(50) NULL,
	diagnostic varchar(128) NULL,
	observations varchar(256) NULL,
	companion varchar(128) NULL,
	duration int4 NULL,
	requirements varchar(128) NULL,
	"group" varchar(50) NULL,
	slugdiagnostic varchar(128) NULL,
	id serial4 NOT NULL,
	CONSTRAINT cids_pkey PRIMARY KEY (id)
);