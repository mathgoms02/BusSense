-- public.reports definition

-- Drop table

-- DROP TABLE public.reports;

CREATE TABLE public.reports (
  id serial4 NOT NULL,
  email VARCHAR(255) NOT NULL,
  id_cidade_origem INT NOT NULL,
  id_cidade_destino INT NOT NULL,
  id_cid INT NOT NULL,
  data_criacao TIMESTAMP NOT NULL,
  CONSTRAINT reports_pkey PRIMARY KEY (id),
  FOREIGN KEY (id_cidade_origem) REFERENCES city(id),
  FOREIGN KEY (id_cidade_destino) REFERENCES city(id),
  FOREIGN KEY (id_cid) REFERENCES cids(id)
);
