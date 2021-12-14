# Sam Judd's Submission Notes
Here is the curl request to GET all items in `store` table:

``` curl -X GET "http://localhost:8000/stores/" ```



Here is the curl request to POST `test_store` to the `demo` db:

``` curl -X POST "http://localhost:8000/stores/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\": \"test_store\"}" ```


## Notes:

- `create-database-and-tables.sh` has both the functionality to create the db and the tables as requested, however, I found that the more efficient way of accomplishing this is to have the `demo` database created during `docker-compose up`. The `store` table is created when the python server is initialized in order for the server to work properly.
- `logging.conf` is a file used in order for the uvicron logs to work properly



