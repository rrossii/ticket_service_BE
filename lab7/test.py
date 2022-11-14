import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "test/2", json={"likes": 500, "name": "Joe", "views": 60000})
print(response.json())
