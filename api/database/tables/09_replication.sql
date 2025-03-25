-- Replication setup
ALTER SYSTEM SET wal_level = 'replica';
ALTER SYSTEM SET max_wal_senders = 5;
ALTER SYSTEM SET max_replication_slots = 5;

-- Create a replication user
CREATE USER replicator REPLICATION LOGIN ENCRYPTED PASSWORD 'replica_pass';

-- Add replication configuration to pg_hba.conf
host replication replicator 0.0.0.0/0 md5
