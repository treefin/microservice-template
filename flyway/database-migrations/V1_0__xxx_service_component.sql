-- xxx_service
CREATE SCHEMA IF NOT EXISTS xxx_service;
GRANT USAGE ON SCHEMA xxx_service TO r_xxx_service;
GRANT USAGE ON SCHEMA xxx_service TO r_xxx_service_ro;

GRANT r_yyy_xxx_service TO r_admin;
GRANT r_yyy_xxx_service_ro TO r_user;
