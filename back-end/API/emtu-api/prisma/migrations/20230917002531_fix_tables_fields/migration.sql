/*
  Warnings:

  - You are about to drop the column `password` on the `access` table. All the data in the column will be lost.
  - The primary key for the `group` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The `id` column on the `group` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - Added the required column `id_linha` to the `searches` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "access" DROP COLUMN "password";

-- AlterTable
ALTER TABLE "bus_routes" ALTER COLUMN "route_name_start" SET DATA TYPE TEXT,
ALTER COLUMN "route_name_end" SET DATA TYPE TEXT;

-- AlterTable
ALTER TABLE "group" DROP CONSTRAINT "group_pkey",
DROP COLUMN "id",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "group_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "searches" ADD COLUMN     "id_linha" INTEGER NOT NULL;
