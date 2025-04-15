-- CreateTable
CREATE TABLE "acess" (
    "id" TEXT NOT NULL,
    "ip" TEXT NOT NULL,
    "data_acesso" TEXT NOT NULL,
    "password" TEXT NOT NULL,

    CONSTRAINT "acess_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "cids" (
    "id" TEXT NOT NULL,
    "cod" TEXT NOT NULL,
    "diagnostic" TEXT NOT NULL,
    "observations" TEXT NOT NULL,
    "companion" TEXT NOT NULL,
    "duration" INTEGER NOT NULL,
    "requirements" TEXT NOT NULL,
    "group" TEXT NOT NULL,
    "slugdiagnostic" TEXT NOT NULL,

    CONSTRAINT "cids_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "cities" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "cities_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "groups" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT NOT NULL,

    CONSTRAINT "groups_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "reports" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "id_cidade_origem" INTEGER NOT NULL,
    "id_cidade_destino" INTEGER NOT NULL,
    "id_cid" INTEGER NOT NULL,
    "data_criacao" TEXT NOT NULL,

    CONSTRAINT "reports_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "bus_routes" (
    "id" TEXT NOT NULL,
    "route_short_name" TEXT NOT NULL,
    "route_name_start" INTEGER NOT NULL,
    "route_name_end" INTEGER NOT NULL,
    "route_type" INTEGER NOT NULL,

    CONSTRAINT "bus_routes_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "searches" (
    "id" TEXT NOT NULL,
    "id_cidade_origem" INTEGER NOT NULL,
    "id_cidade_destino" INTEGER NOT NULL,
    "id_cid" INTEGER NOT NULL,
    "data_viagem" TEXT NOT NULL,
    "hora_viagem" TEXT NOT NULL,
    "data_criacao" TEXT NOT NULL,

    CONSTRAINT "searches_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "vehicles" (
    "id" TEXT NOT NULL,
    "prefix" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "group" TEXT NOT NULL,

    CONSTRAINT "vehicles_pkey" PRIMARY KEY ("id")
);
