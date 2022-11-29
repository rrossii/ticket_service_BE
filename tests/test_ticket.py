from tests.conftest import client, flask_login, app_with_db
from lab6.models import Ticket

#
# def test_error_create_ticket(app_with_data):
#     res = app_with_data.post("/tickets", json={
#         "name":"ticket1",
#         "price":3000,
#         "category_id":1,
#         "quantity":20,
#         "date":"2022-09-09",
#         "place":"Lviv",
#         "status":"available"
#     })
#
#     assert res.status_code == 401

def test_get_ticket_by_id(client):
    res = client.get('/tickets/3')
    a = 5
    assert res.status_code == 200


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
