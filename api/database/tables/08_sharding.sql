-- Sharding setup
CREATE EXTENSION IF NOT EXISTS postgres_fdw;
CREATE SERVER shard1 FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'shard1_host', dbname 'neura_sync', port '5432');

CREATE SERVER shard2 FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host 'shard2_host', dbname 'neura_sync', port '5432');
