# Welcome!
The purpose of this project is to create a small Python server that can interact with a PostgreSQL database. This server is built in a docker container and can be ran using `docker compose up`. The following tasks explain how we expect you to do this.

## Task 1:
- Write a Dockerfile so that when the command `docker build --build-arg mode=dev . -t demo/server` is ran in the root of the directory an image that meets the following requirements is be built:
  - Has Python version 3.7
  - Sets an environment variable `MODE` to the value of the build argument `mode`
  - Has the program `psql` for version 13 of PostgreSQL installed
  - Has the Google Cloud SDK installed
  - Populate the `requirements.txt` to specify:
    - `uvicorn[standard]` at the explicit version `0.15.0`
    - `fastapi` at the major version `0` minor version `70` and the most recent patch version
    - (Eventually you will need to add more libraries to this file in order to complete the python portion of this challenge)
  - Installs the pip `requirements.txt` file
  - The container by default should run `sleep infinity` when started
- The Dockerfile contains the line `COPY . /app` you can not remove this line, but you must ensure that only relevant files get copied in the container. For example, the `.gitignore` is a file that should not be contained in the image

## Task 2:
- Write a docker compose file so that when the command `docker compose up` is ran at the root of the directory the following requirements are met:
  - The image described above is started and meets the following specifications:
    - It is built if not already present on the system
    - The build arg value for `mode` should be set to `dev`
    - Has a volume set up so that all changes made locally are instantly reflected in the container
    - This command `uvicorn main:app --reload` should be ran at startup
    - Sets environment variable `LOG_LEVEL` to `debug`
    - The command `docker exec -it server /bin/bash` will shell into this
    - Below there are details on starting up a PostgreSQL database, the `database`, `user`, and `password` will also need to be made accessible to this container
  - Starts an image that has PostgreSQL version 13 that:
    - Is accessible by the other container
    - Has a database called `demo`
    - Has a user named `demouser` whose password is `password123`

## Task 3 (Note: The following script is meant to be executed inside the server container):
- Create a bash script `create-database-and-tables.sh` that:
  - Is executable
  - Reads from environment variables to determine the database/username/password for the PostgreSQL instance
  - Uses `psql` to create a table called `store` that has an auto incremented `id` column and a text column `name`
- Execute the script on the server container to populate the database

## Task 4 (Look at the FastAPI docs for reference):
- Open the `main.py` file
- Make it so that on startup of the server if the environment variable `LOG_LEVEL` is set to `debug` you print out the contents of the environment variable `MODE`
- Create a route in the file that takes a `store_name` and adds it to the database. As long as FastAPI is the web server you can use any additional libraries you choose.
- Bonus: Write unit tests that are ran automatically during the image build. The build for the should fail if the tests fail

## Task 5:
- Provide a cURL command that when ran will post data to your Python service, resulting in a store with name `test_store` being inserted into the database.


# How will we verify this once submitted?
Once your code is submitted we will do the following to verify functionality:
- Run `docker compose up` to start the server/database containers
- In the server container we will confirm:
  - All requested packages are installed at the versions requested
  - Only relevant files were copied in
- In the logs we will verify that the content of the environment variable `MODE` is visible. We will also confirm that when we change the value of `LOG_LEVEL` to `info` it is no longer visible.
- We will verify that when `create-database-and-tables.sh` is executed inside of the server container the `store` table is created and the schema is correct
- We will execute the cURL command provided by you and verify that that it populates the database as expected
- Bonus: If you chose to do the bonus we will verify if the tests fail that the docker image build fails

# Sam Judd's Submission Notes
Here is the curl request to GET all items in `store` table:

``` curl -X GET "http://localhost:8000/stores/" ```



Here is the curl request to POST `test_store` to the `demo` db:

``` curl -X POST "http://localhost:8000/stores/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"name\": \"test_store\"}" ```


## Notes:

- `create-database-and-tables.sh` has both the functionality to create the db and the tables as requested, however, I found that the more efficient way of accomplishing this is to have the `demo` database created during `docker-compose up`. The `store` table is created when the python server is initialized in order for the server to work properly.
- `logging.conf` is a file used in order for the uvicron logs to work properly

