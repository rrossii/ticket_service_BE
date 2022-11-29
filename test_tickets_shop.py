# import json
# from flask import Flask
# import pytest
# import jwt
# from lab7.requests_to_server import *
# from lab6.models import app
# from base64 import b64decode
#
#
# # initial config
# @pytest.fixture()
# def client():
#     app.config["TESTING"] = True
#     # app.config["DEBUG"] = True
#
#     client = app.test_client()
#     ctx = app.app_context()
#     ctx.push()
#
#     yield client
#
#     ctx.pop()
#
# # ticket tests
# def test_add_ticket_success(client):
#     with client:
#         url = "/tickets"
#         # access_token = create_access_token("user") # ????
#         access_token = jwt.encode({"email": "belle@mail.com", "user": "admin_supeyr"}, app.config['SECRET_KEY'])
#         # access_token = access_token.replace("Bearer ", '')
#         mock_headers = {
#             "Authorization": format(access_token)
#         }
#
#         mock_requires_data = {
#             "category_id": 4,
#             "date": "2023-11-30 18:00:00",
#             "name": "Harry Potter",
#             "place": "Lviv",
#             "price": 295,
#             "quantity": 500,
#             "status": "available"
#         }
#
#         response = client.post(url, data=mock_requires_data, headers=mock_headers)
#         assert response.status_code == 200
