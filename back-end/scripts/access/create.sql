-- public.access definition

-- Drop table

-- DROP TABLE public.access;

CREATE TABLE public.access (
  id serial4 NOT NULL,
  ip VARCHAR(255) NOT NULL,
  data_acesso TIMESTAMP NOT NULL,
  CONSTRAINT access_pkey PRIMARY KEY (id)
);
