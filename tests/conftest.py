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

    # ctx = app.test_request_context()
    # ctx.push()
    with app.app_context():
        with app.test_client():
            yield client

    # ctx.pop()


@pytest.fixture
def app_with_db(client):
    # db.create_all()

    yield client

    db.session.commit()
    # db.drop_all()


@pytest.fixture
def app_with_data(app_with_db):
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
        name="ticket1",
        price=3000,
        category_id=1,
        quantity=20,
        date="2022-09-09",
        place="Lviv",
        status="available"
    )

    db.session.add(user)
    db.session.add(ticket)

    # db.session.commit()

    yield app_with_db

    db.session.execute(delete(User))
    db.session.execute(delete(Ticket))
    db.session.commit()


@pytest.fixture
def flask_login(app_with_data):
    res = app_with_data.post("/user/login", json={"email": "ros@gmail.com", "user": "mylogin"})

    # jwt = res.json["access_token"]
    token = jwt.encode({"email": "ros@gmail.com", "user": "mylogin"}, app.config['SECRET_KEY'])
    return {"Authorization": f"Bearer {token}"}

def test_get_ticket_by_id():
    app.config['TESTING'] = True

    client = app.test_client()
    with app.app_context():
        res = client.get('/tickets/3')
    a = 5
    assert res.status_code == 200

if __name__ == "__main__":
    pytest.main()
    app.run()