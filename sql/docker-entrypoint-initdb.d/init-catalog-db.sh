#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE USER app;
  GRANT CONNECT ON DATABASE catalog TO app;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname catalog <<-EOSQL
        CREATE EXTENSION pg_sphere;
EOSQL

python3 /fill_tables.py
psql -v ON_ERROR_STOP=1 --username catalog --dbname catalog <<-EOSQL
  ALTER TABLE table2 ADD PRIMARY KEY ("SourceID");
  CREATE UNIQUE INDEX table2_sourceid_index ON table2 ("ID");
  ALTER TABLE table2 ADD COLUMN coord spoint;
  UPDATE table2 SET coord = spoint("RAdeg" * pi() / 180.0, "DEdeg" * pi() / 180.0);
  ALTER TABLE table2 ALTER COLUMN coord SET NOT NULL;
  CREATE INDEX table2_coord_idx ON table2 USING GIST (coord);

  CREATE UNIQUE INDEX table6_sourceid_index ON table6 ("ID");
  ALTER TABLE table6 ADD COLUMN coord spoint;
  UPDATE table6 SET coord = spoint("RAdeg" * pi() / 180.0, "DEdeg" * pi() / 180.0);
  ALTER TABLE table6 ALTER COLUMN coord SET NOT NULL;
  CREATE INDEX table6_coord_idx ON table6 USING GIST (coord);
EOSQL

psql -v ON_ERROR_STOP=1 --username catalog --dbname catalog <<-EOSQL
   VACUUM FULL ANALYZE;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname catalog <<-EOSQL
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO app;
    REVOKE CREATE ON SCHEMA public FROM public;
EOSQL
