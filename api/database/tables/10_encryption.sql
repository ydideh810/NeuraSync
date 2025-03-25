-- Enable pgcrypto for encryption
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Encrypt columns
ALTER TABLE devices ADD COLUMN secret_key BYTEA;
ALTER TABLE devices ADD COLUMN encrypted_info BYTEA;

-- Insert encrypted data
INSERT INTO devices (device_name, device_type, secret_key, encrypted_info)
VALUES (
    'Device_1',
    'GPU',
    pgp_sym_encrypt('my_secret_key', 'encryption_passphrase'), 
    pgp_sym_encrypt('Confidential Data', 'encryption_passphrase')
);
