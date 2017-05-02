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

3. Apply migrations `./manage.py migrate`
4. Make sure all unit tests are passing `./manage.py test`
5. Create superuser with `./manage.py createsuperuser`
6. Start local server `./manage.py runserver`

## Usage 
1. Go to `localhost:8000/api/oauth/applications/`, authenticate as SU and create new application. Choose *Name: just a name of your choice*, *Client type: confidential* and *Authorization grant type: Resource owner password-based*. Save your **client_id** and **client_secret**.
2. Sign up:
```
curl -X POST \
  http://localhost:8000/api/sign-up/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d 'username=<USERNAME>&password=<PASSWORD>'
```
3. Authenticate and save your token:
```
curl -X POST \
  http://localhost:8000/api/oauth/token/ \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=<USERNAME>&password=<PASSWORD>&client_id=<CLIENT_ID>&client_secret=<CLIENT_SECRET>'
```
4. Always use your new token in headers `{"Authorization":"Bearer YOUR-AUTH-TOKEN"}`

## Functionality
1. Create new review object and save it's ID:
```
curl -X POST \
  http://localhost:8000/api/review/add/ \
  -H 'authorization: Bearer YOUR-AUTH-TOKEN' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d body=new%20body11
``` 
2. Create a few comments for a previous review by passing review's ID:
```
curl -X POST \
  http://localhost:8000/api/review/comment/add/ \
  -H 'authorization: Bearer YOUR-AUTH-TOKEN' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d 'body=new%20body22222234234234&review=1'
```
3. Check all saved data:
```
curl -X GET \
  http://localhost:8000/api/reviews/ \
  -H 'authorization: Bearer YOUR-AUTH-TOKEN' \
  -H 'cache-control: no-cache'
```
