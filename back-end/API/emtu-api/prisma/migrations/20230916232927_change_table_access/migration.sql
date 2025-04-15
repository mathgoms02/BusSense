/*
  Warnings:

  - You are about to drop the `acess` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropTable
DROP TABLE "acess";

-- CreateTable
CREATE TABLE "access" (
    "id" TEXT NOT NULL,
    "ip" TEXT NOT NULL,
    "data_acesso" TEXT NOT NULL,
    "password" TEXT NOT NULL,

    CONSTRAINT "access_pkey" PRIMARY KEY ("id")
);
