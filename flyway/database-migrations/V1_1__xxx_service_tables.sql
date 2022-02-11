CREATE FOREIGN TABLE xxx_service.something(

    something_id uuid,
    something_id_datetime timestamp with time zone,
    something text
    )
    SERVER cstore_server
    OPTIONS (compression 'pglz', stripe_row_count '100000');
