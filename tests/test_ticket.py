from tests.conftest import client, flask_login, app_with_database, data, data_admin
from lab6.models import Ticket


def test_create_ticket(data_admin, flask_login_admin):
    res = data_admin.post("/tickets",
                          json={
                              "name": "fancy_event",
                              "price": 2000,
                              "category_id": 1,
                              "quantity": 500,
                              "date": "2022-09-09",
                              "place": "Kyiv",
                              "status": "available"
                          },
                          headers=flask_login_admin)

    assert res.status_code == 200


def test_create_ticket_error(data, flask_login):
    res = data.post("/tickets",
                    json={
                        "name": "fancy_event",
                        "price": 2000,
                        "category_id": 1,
                        "quantity": 500,
                        "date": "2022-09-09",
                        "place": "Kyiv",
                        "status": "available"
                    },
                    headers=flask_login)

    assert res.status_code == 404

# def test_get_ticket_by_id(client):
#     res = client.get('/tickets/22')
#     assert res.status_code == 200

# def test_error_create_ticket(app_with_data_admin):
#     res = app_with_data_admin.post("/ticket", json={
#         "seat_number": 1,
#         "price": 3000.99,
#         "is_bought": 1,
#         "is_booked": 1
#     })
#
#     assert res.status_code == 401
#
#
# def test_delete_ticket_by_id(app_with_db, flask_login):
#     res = app_with_db.get('/ticket/8', headers=flask_login)
#     assert res.status_code == 200
#
#
# def test_error_update_ticket(app_with_data_admin, flask_login_admin):
#     res = app_with_data_admin.put("/ticket", json={
#         "idticket": 5,
#         "seat_number": 1,
#         "price": 3000.99,
#         "is_bought": 0,
#         "is_booked": 1
#     }, headers=flask_login_admin)
#     assert res.status_code == 404


# def test_get_all_tickets(client):
#     res = client.get()
#     url = "/tickets"
#
#     access_token = create_access_token("user")  # ????
#     access_token = jwt.encode({"email": "belle@mail.com", "user": "admin_supeyr"}, app.config['SECRET_KEY'])
#     # access_token = access_token.replace("Bearer ", '')
#     mock_headers = {
#         "Authorization": format(access_token)
#     }
#
#     mock_requires_data = {
#         "category_id": 4,
#         "date": "2023-11-30 18:00:00",
#         "name": "Harry Potter",
#         "place": "Lviv",
#         "price": 295,
#         "quantity": 500,
#         "status": "available"
#     }
#
#     response = client.post(url, data=mock_requires_data, headers=mock_headers)
#     assert response.status_code == 200
