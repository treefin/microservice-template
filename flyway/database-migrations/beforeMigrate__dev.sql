-- ONLY MODIFY in dev-only dir and copy back to flyway/database-migrations

-- cstore specific
CREATE extension cstore_fdw;
CREATE server cstore_server
    FOREIGN DATA wrapper cstore_fdw;

-- not really used for development, for consistency sake
CREATE ROLE r_admin;
CREATE ROLE r_xxx_service_ro;

-- for saving
CREATE ROLE r_xxx_service WITH login password 'r_xxx_service';

-- for reading
CREATE ROLE r_user WITH login password 'r_user';