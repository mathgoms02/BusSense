-- public.searches definition

-- Drop table

-- DROP TABLE public.searches;

CREATE TABLE public.searches (
  id serial4 NOT NULL,
  id_cidade_origem INT NOT NULL,
  id_cidade_destino INT NOT NULL,
  id_cid INT,
  data_viagem DATE,
  hora_viagem VARCHAR(255),
  data_criacao TIMESTAMP NOT NULL,
  CONSTRAINT searches_pkey PRIMARY KEY (id),
  FOREIGN KEY (id_cidade_origem) REFERENCES city(id),
  FOREIGN KEY (id_cidade_destino) REFERENCES city(id),
  FOREIGN KEY (id_cid) REFERENCES cids(id)
);
