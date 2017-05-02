# DjangoGuestBookAPI
Python Django Guest Book API example

## Requirements
1. Python 3.4
2. Django 1.11
3. PostgreSQL 9.6.2

## Installation
1. Install PostgreSQL
2. Apply some commands and SQL:

  ```
  sudo su - postgres  
  psql
  CREATE DATABASE djangoguestbook;
  CREATE USER djangoguestuser WITH PASSWORD 'djangoguest12qw?';
  ALTER ROLE djangoguestuser SET client_encoding TO 'utf8';
  ALTER ROLE djangoguestuser SET default_transaction_isolation TO 'read committed';
  ALTER ROLE djangoguestuser SET timezone TO 'UTC';
  GRANT ALL PRIVILEGES ON DATABASE djangoguestbook TO djangoguestuser;
  ALTER USER djangoguestuser CREATEDB;
  ```  

3. Install `venv` into project's directory and enter the `venv`
4. Install all requirements from `requirements.txt` under `venv` by using `pip`
5. Apply migrations with `./manage.py migrate`
6. Check yourself with `./manage.py check`
