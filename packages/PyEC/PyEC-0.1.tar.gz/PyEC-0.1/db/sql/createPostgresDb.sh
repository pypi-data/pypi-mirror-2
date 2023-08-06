#! /bin/bash
echo "CREATE DATABASE $1" | psql -U postgres
