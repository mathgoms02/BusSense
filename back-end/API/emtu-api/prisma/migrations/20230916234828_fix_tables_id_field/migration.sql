/*
  Warnings:

  - The primary key for the `access` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The `id` column on the `access` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - The primary key for the `bus_routes` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The `id` column on the `bus_routes` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - The primary key for the `cids` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The `id` column on the `cids` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - The primary key for the `city` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The `id` column on the `city` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - The primary key for the `reports` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The `id` column on the `reports` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - The primary key for the `searches` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The `id` column on the `searches` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - The primary key for the `users` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The `id` column on the `users` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - The primary key for the `vehicles` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The `id` column on the `vehicles` table would be dropped and recreated. This will lead to data loss if there is data in the column.

*/
-- AlterTable
ALTER TABLE "access" DROP CONSTRAINT "access_pkey",
DROP COLUMN "id",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "access_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "bus_routes" DROP CONSTRAINT "bus_routes_pkey",
DROP COLUMN "id",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "bus_routes_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "cids" DROP CONSTRAINT "cids_pkey",
DROP COLUMN "id",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "cids_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "city" DROP CONSTRAINT "city_pkey",
DROP COLUMN "id",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "city_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "reports" DROP CONSTRAINT "reports_pkey",
DROP COLUMN "id",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "reports_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "searches" DROP CONSTRAINT "searches_pkey",
DROP COLUMN "id",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "searches_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "users" DROP CONSTRAINT "users_pkey",
DROP COLUMN "id",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");

-- AlterTable
ALTER TABLE "vehicles" DROP CONSTRAINT "vehicles_pkey",
DROP COLUMN "id",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "vehicles_pkey" PRIMARY KEY ("id");
