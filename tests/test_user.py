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

# def test_user_create_error():
#     pass
