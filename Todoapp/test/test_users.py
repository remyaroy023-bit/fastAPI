from .utils import *
from ..routers.users import get_db,get_current_user
from ..models import Todos,Users

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_user(test_user):
    print(test_user.username)

    response = client.get("/users/users")
    assert response.status_code == 200
    print(response.text)
    assert response.json()['username'] == 'remi'
    assert response.json()['email'] == 'remi.com'
    assert response.json()['firstname'] == 'remi'
    assert response.json()['lastname'] == 'ry'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '123456'

def test_change_password_success(test_user):
    response = client.put("/users/password",json={'password': 'test123','new_password':'testabc'})
    assert response.status_code == 204

def test_change_password_invalid(test_user):
    response = client.put("/users/password", json={'password': 'test--123', 'new_password': 'testabc'})
    assert response.status_code == 401
    assert response.json() == {'detail':'Incorrect Password'}

def test_change_phone_success(test_user):
    response = client.put("/users/12345678")
    assert response.status_code == 204






