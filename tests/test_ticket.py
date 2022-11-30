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


# def test_create_ticket_error(data, flask_login):
#     res = data.post("/tickets",
#                     json={
#                         "name": "fancy_event",
#                         "price": 2000,
#                         "category_id": 1,
#                         "quantity": 500,
#                         "date": "2022-09-09",
#                         "place": "Kyiv",
#                         "status": "available"
#                     },
#                     headers=flask_login)
#
#     assert res.status_code == 404


# def test_get_ticket_by_id(app_with_database):
#     res = app_with_database.get('/tickets/25')
#     assert res.status_code == 200

# def test_get_ticket_by_id_error(app_with_database):
#     res = app_with_database.get('/tickets/1')
#     assert res.status_code == 404
#
#
# def test_delete_ticket(app_with_database, flask_login_admin):
#     res = app_with_database.get('/tickets/3', headers=flask_login_admin)
#     assert res.status_code == 200
#
#
# def test_delete_ticket_error(app_with_database, flask_login):
#     res = app_with_database.get('/tickets/1', headers=flask_login)
#     assert res.status_code == 404
#
#
# def test_get_all_tickets(app_with_database):
#     res = app_with_database.get('/tickets')
#     assert res.status_code == 200
#
#
# def test_update_ticket_info(data_admin, flask_login_admin):
#     res = data_admin.put("/tickets/3",
#                          json={
#                              "name": "fancy_event",
#                              "price": 2000,
#                              "category_id": 1,
#                              "quantity": 500,
#                              "date": "2022-09-09",
#                              "place": "Kyiv",
#                              "status": "available"
#                          },
#                          headers=flask_login_admin)
#
#     assert res.status_code == 200
#
#
# def test_update_ticket_info_error(data_admin, flask_login_admin):
#     res = data_admin.put("/tickets/1",
#                          json={
#                              "name": "fancy_event",
#                              "price": 2000,
#                              "category_id": 1,
#                              "quantity": 500,
#                              "date": "2022-09-09",
#                              "place": "Kyiv",
#                              "status": "available"
#                          },
#                          headers=flask_login_admin)
#
#     assert res.status_code == 404
