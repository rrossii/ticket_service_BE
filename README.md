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