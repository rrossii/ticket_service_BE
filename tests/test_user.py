from conftest import client, flask_login, app_with_database, data, data_admin


def test_user_create(app_with_database):
    res = app_with_database.post("/user",
                                 json={
                                     "username": "queen",
                                     "first_name": "Freddie",
                                     "last_name": "Mercury",
                                     "email": "cool@mail.com",
                                     "password": "12345678",
                                     "phone": "0956789709",
                                     "user_status": "admin"
                                 })
    assert res.status_code == 200


def test_update_user_error(data, flask_login):
    res = data.put("/user/2",
                   json={
                       "username": "queen",
                       "first_name": "Freddie",
                       "last_name": "Mercury",
                       "email": "cool@mail.com",
                       "password": "12345678",
                       "phone": "0956789709",
                       "user_status": "admin"
                   },
                   headers=flask_login)
    assert res.status_code == 404


def test_get_user_by_id():
    pass
