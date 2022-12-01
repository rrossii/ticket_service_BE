## Buying and Booking Tickets

### Run Program

* install dependencies
```
    pip3 install pipenv
    pipenv install
```

* activate virtual environment
```
    pipenv shell
```
* run through gunicorn
```
    gunicorn --bind 127.0.0.1:5000 wsgi:app
```
* enter 
```
    curl -v http://127.0.0.1:5000 
```

### Work with database
* install Flask-SQLAlchemy
```
    pipenv install Flask-SQLAlchemy
```
* write URI: for mysql:
```
  app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://username:password@host:port/database_name" 
```
* write URI: for test database:
```
  app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://username:password@host:port/test_database_name" 
```
* for creating migrations you need Alembic module
```
    pipenv install alembic
```
* initialize Alembic
```
    alembic init alembic
```
* change alembic.ini file
```
    sqlalchemy.url = mysql://root:password@localhost:3306/database_name
```
* to create migration use
```
    alembic upgrade head
```

### Unit Tests
* install pytest module
```
    pipenv install pytest
```
* install coverage module
```
    pipenv install coverage
```
* create conftest.py 
* create your tests in another files
* while testing use test_ticket_shop; while running queries use ticket_shop
* to run tests:
```
    coverage run -m pytest
```
* to show percent of coverage
```
    coverage report -m
```
### ER-diagram
![ticket_shop](images/ticket_shop.png)