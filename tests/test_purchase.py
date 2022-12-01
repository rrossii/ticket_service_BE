from conftest import client, flask_login, app_with_database, data, data_admin


def test_buy_ticket(app_with_database):
    res = app_with_database.post("/tickets/buy/1",
                                 json={
                                     "quantity": 2,
                                     "user_id": 1
                                 })
    assert res.status_code == 200


def test_buy_ticket_error_with_quantity(app_with_database):
    res = app_with_database.post("/tickets/buy/1",
                                 json={
                                     "quantity": 1000,
                                     "user_id": 1
                                 })
    assert res.status_code == 404


def test_buy_ticket_error_when_ticket_not_found(app_with_database):
    res = app_with_database.post("/tickets/buy/666",
                                 json={
                                     "quantity": 3,
                                     "user_id": 1
                                 })
    data = res.json
    assert data["message"] == "Ticket not found"


def test_buy_ticket_error_when_user_not_found(app_with_database):
    res = app_with_database.post("/tickets/buy/1",
                                 json={
                                     "quantity": 3,
                                     "user_id": 666
                                 })
    data = res.json
    assert data["message"] == "User not found"


def test_book_ticket(app_with_database):
    res = app_with_database.post("/tickets/book/1",
                                 json={
                                     "quantity": 2,
                                     "user_id": 1
                                 })
    assert res.status_code == 200


def test_book_ticket_error_with_quantity(app_with_database):
    res = app_with_database.post("/tickets/book/1",
                                 json={
                                     "quantity": 1000,
                                     "user_id": 1
                                 })
    assert res.status_code == 404


def test_book_ticket_error_when_ticket_not_found(app_with_database):
    res = app_with_database.post("/tickets/book/666",
                                 json={
                                     "quantity": 3,
                                     "user_id": 1
                                 })
    data = res.json
    assert data["message"] == "Ticket not found"


def test_book_ticket_error_when_user_not_found(app_with_database):
    res = app_with_database.post("/tickets/book/1",
                                 json={
                                     "quantity": 3,
                                     "user_id": 666
                                 })
    data = res.json
    assert data["message"] == "User not found"


def test_cancel_book_error(app_with_database):
    res = app_with_database.delete("/tickets/book/666")
    assert res.status_code == 404


def test_get_all_purchases(app_with_database):
    res = app_with_database.get("/tickets")
    assert res.status_code == 200
