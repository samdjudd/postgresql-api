#!/bin/sh
DATABASE=$POSTGRES_DB
USERNAME=$POSTGRES_USER
PASSWORD=$POSTGRES_PASSWORD

# Line 9: connects to PostgreSQL database
# Line 10: creates store_name table and adds id (auto incremented) and name fields
# Line 11: returns full table to shell output
psql -h db -U $POSTGRES_USER -d $POSTGRES_DB << EOF
CREATE TABLE store (id SERIAL PRIMARY KEY, name VARCHAR (50));
SELECT * FROM store;
EOF