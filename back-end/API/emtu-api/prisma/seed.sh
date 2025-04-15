#!/bin/sh
# -e Exit immediately when a command returns a non-zero status.
# -x Print commands before they are executed
set -ex
# Seeding command
psql -U postgres -d emtu -f /scripts/city/cidade.sql &&
psql -U postgres -d emtu -f /scripts/cids/cids_202212242142.sql &&
psql -U postgres -d emtu -f /scripts/group/group__202212251022.sql &&
psql -U postgres -d emtu -f /scripts/routes/routes.sql &&
psql -U postgres -d emtu -f /scripts/vehicles/vehicles_insert.sql