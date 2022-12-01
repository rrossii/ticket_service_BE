from conftest import client, flask_login, app_with_database, data, data_admin


def test_get_ticket_by_id(app_with_database):
    # тут також змінити айді
    res = app_with_database.get('/tickets/1')
    assert res.status_code == 200


def test_get_ticket_by_id_error(app_with_database):
    res = app_with_database.get('/tickets/67')
    assert res.status_code == 404


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

    assert res.status_code in [401, 404]


def test_get_all_tickets(app_with_database):
    res = app_with_database.get('/tickets')
    assert res.status_code == 200


# update error when not admin updates
# maybe do another test for checking if ticket not exists then error
def test_update_ticket_info_error(data, flask_login):
    res = data.put("/tickets/1",
                   json={
                       "name": "fancy_event_updated",
                       "price": 1500,
                       "category_id": 1,
                       "quantity": 156,
                       "date": "2022-09-09",
                       "place": "Kyiv",
                       "status": "available"
                   },
                   headers=flask_login)

    assert res.status_code in [404, 401]


# def test_delete_ticket(app_with_database, flask_login_admin):
#     # не забути змінити айді квитка який буде видалятись!!!!!!
#     res = app_with_database.delete('/tickets/1', headers=flask_login_admin)
#     assert res.status_code == 204


def test_delete_ticket_error(app_with_database, flask_login):
    res = app_with_database.delete('/tickets/67', headers=flask_login)
    assert res.status_code == 404
