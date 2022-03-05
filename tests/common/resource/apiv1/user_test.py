import pytest, json
@pytest.mark.parametrize(
    ("headers", "body", "status", "code"),
    [
        ({}, {}, 415, 101)
        ({"Content-type": "application/json"}, {"username": 1, "password": 1}, 400,104 ),
        ({"Content-type": "application/json"}, {"username": "", "password": test}, 400,105 ),
        ({"Content-type": "application/json"}, {"username": "test", "password": "1"}, 400,105 ),
        ({"Content-type": "application/json"}, {"username": "test", "password": "test"}, 201,100 ),
        ({"Content-type": "application/json"}, {"username": 1, "password": 1}, 409,106 ),
        


    ]

)
def test_create_user(client, headers, body, status, code):
    result = client.post(
        "/api/v1/users",
        data=json.dump(body),
        json=body,
        headers=headers
        )
        assert result.status_code == status
        assert result.get_json()["code"] == code
