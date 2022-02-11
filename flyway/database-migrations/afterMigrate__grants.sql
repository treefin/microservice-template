GRANT ALL PRIVILEGES ON SCHEMA xxx_service TO r_xxx_service;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA xxx_service TO r_xxx_service;

GRANT USAGE ON SCHEMA xxx_service TO r_user;
GRANT SELECT ON ALL TABLES IN SCHEMA xxx_service TO r_user;
