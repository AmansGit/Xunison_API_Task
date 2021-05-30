# Xunison_API_Task
Create Movie details with CRUD operations.

## Setup

#### First create the virtual environment using virtualenv
```
>>> virtualenv -p python3 env
```
#### Activate the environment [for Linux platform]
```
>>> source env/bin/activate
```

#### Install The requirements.txt
```
>>> pip install -r requirements.txt
```
## Server check
#### To check the server running
Go to the file where manage.py is present
```sh
 >>> python manage.py makemigrations movie_crud
 >>> python manage.py migrate
 >>> python manage.py runserver
```
## Test cases
If everything runs fine then, for running test files
```sh
>>> python manage.py test movie_crud
```

## Postman

 [getpostman.com/collections/ed76c0e2580ccd4881ad](https://www.getpostman.com/collections/ed76c0e2580ccd4881ad)


# Authors
- Aman Kumar Sharma ([github.com/AmansGit](https://github.com/AmansGit))
