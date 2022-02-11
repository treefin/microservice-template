# Template for Micro Services
This is a template for a micro service that receives a REST request with "something" and stores all the somethings in a Postgres DB if they haven't occured in the last 7 days.

## How to run locally
1. Use the ``setup-dev-db.sh`` to build and start a docker container for the postgres and perform the migration steps necessary.
2. Start the local dev server (``run-dev-server.py``)
3. Use e.g. Postman to send a request to ``http://0.0.0.0:2329/xxx/save_somethings

### Demo Request
```
{
    "somethings": [
        {
            "something_id": "{{$guid}}",
            "something_id_datetime": "2021-11-9",
            "something": "test"
        },
        {
            "something_id": "{{$guid}}",
            "something_id_datetime": "2021-11-9",
            "something": "test"
        }
    ]
}
```
