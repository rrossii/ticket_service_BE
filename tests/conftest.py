import pytest
from lab6.models import User, Ticket
# from lab7.requests_to_server import app
from lab7.requests_to_server import app, db
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt


@pytest.fixture(scope="session")
def _app():
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:*sashros*@localhost:3306/test_ticket_shop"

    yield app


@pytest.fixture(scope="session")
def fake_db(_app):
    fake = SQLAlchemy(_app)

    yield fake


@pytest.fixture(scope='session')
def client(_app):
    client = _app.test_client()

    ctx = _app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture
def app_with_database(client, fake_db):
    # insert tables to db

    with app.app_context():
        # with client:
        fake_db.create_all()

    yield client
    fake_db.drop_all()
    fake_db.session.commit()


@pytest.fixture
def data(app_with_database, fake_db):
    with app.app_context():
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

        fake_db.session.add(user)
        fake_db.session.add(ticket)

        fake_db.session.commit()

    yield app_with_database

    fake_db.session.delete(user)
    fake_db.session.delete(ticket)
    fake_db.session.commit()


@pytest.fixture
def data_admin(app_with_database, fake_db):
    with app.app_context():
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
        fake_db.session.add(user)
        fake_db.session.add(ticket)

        fake_db.session.commit()

    yield app_with_database

    fake_db.session.delete(user)
    fake_db.session.delete(ticket)
    fake_db.session.commit()


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
