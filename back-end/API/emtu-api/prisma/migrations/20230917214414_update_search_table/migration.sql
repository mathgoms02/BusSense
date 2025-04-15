/*
  Warnings:

  - Added the required column `sucedida` to the `searches` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "searches" ADD COLUMN     "sucedida" BOOLEAN NOT NULL,
ALTER COLUMN "id_linha" SET DATA TYPE TEXT;
