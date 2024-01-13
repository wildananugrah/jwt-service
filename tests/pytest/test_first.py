from jsonschema import validate
import requests

host = "http://localhost:5000"
token = None

def validate_schema(response_json, schema):
    try:
        validate(instance=response_json, schema=schema)
        return True
    except Exception as e:
        print(e)
        return False

create_token_response_schema = {
  "type": "object",
  "properties": {
    "token": {
      "type": "string"
    },
    "expired": {
      "type": "number"
    }
  },
  "required": ["token", "expired"]
}

def test_create_token():
    global token

    payload = {
        "username" : "wildananugrah",
        "age" : 32
    }

    response = requests.post(f"{host}/token", json=payload)

    assert 200 == response.status_code
    assert True == validate_schema(response_json=response.json(), schema=create_token_response_schema)
    token = response.json()["token"]

def test_validate_token():
    global token
    
    response = requests.post(f"{host}/validate", json={ "token" : token })
    response_json = response.json()
    print(response_json)
    assert 200 == response.status_code
    assert dict == type(response_json)

def test_refresh_token():
    global token
    
    response = requests.post(f"{host}/refresh", json={ "token" : token })
    
    assert 200 == response.status_code
    assert dict == type(response.json())

