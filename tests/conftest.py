import pytest
from lab6.models import db, User, Ticket
from lab7.requests_to_server import app
from werkzeug.security import generate_password_hash
from sqlalchemy import delete
import jwt


@pytest.fixture
def client():
    app.config['DEBUG'] = True
    app.config['TESTING'] = True

    client = app.test_client()

    with app.app_context():
        with app.test_client():
            yield client


@pytest.fixture()
def app_with_database(client):
    db.create_all()

    yield client

    db.session.commit()


@pytest.fixture
def data(app_with_database):
    user = User(
        username="mylogin",
        first_name="Rosana",
        last_name="Klym",
        email="ros@gmail.com",
        password=generate_password_hash(password="12345678"),
        phone="0630723191",
        user_status="user"
    )

    ticket = Ticket(
        name="fancy_event",
        price=2000,
        category_id=1,
        quantity=500,
        date="2022-09-09",
        place="Kyiv",
        status="available"
    )

    db.session.add(user)
    db.session.add(ticket)

    with app.app_context():
        db.session.commit()

    yield app_with_database

    db.session.delete(user)
    db.session.delete(ticket)
    with app.app_context():
        db.session.commit()


@pytest.fixture
def data_admin(app_with_database):
    user = User(
        username="joe_cool",
        first_name="Joe",
        last_name="Smith",
        email="joe@gmail.com",
        password=generate_password_hash(password="helloworld"),
        phone="0630674191",
        user_status="admin"
    )

    ticket = Ticket(
        name="fancy_event",
        price=2000,
        category_id=1,
        quantity=500,
        date="2022-09-09",
        place="Kyiv",
        status="available"
    )

    db.session.add(user)
    db.session.add(ticket)

    with app.app_context():
        db.session.commit()

    yield app_with_database

    db.session.delete(user)
    db.session.delete(ticket)
    with app.app_context():
        db.session.commit()


@pytest.fixture
def flask_login(data):
    res = data.post("/user/login", json={"email": "ros@gmail.com", "password": "12345678"})

    token = jwt.encode({"email": "ros@gmail.com", "user": "mylogin"}, app.config['SECRET_KEY'])
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def flask_login_admin(data_admin):
    res = data_admin.post("/user/login", json={"email": "joe@gmail.com", "password": "helloworld"})

    token = jwt.encode({"email": "joe@gmail.com", "user": "joe_cool"}, app.config['SECRET_KEY'])
    return {"Authorization": f"Bearer {token}"}

#
# if __name__ == "__main__":
#     pytest.main()
#     app.run()
