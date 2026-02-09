

from fastapi import status
from ..routers.todos import get_db,get_current_user
from .utils import *




app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todos):
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == [{'priority': 4, 'id': 1, 'owner_id': 1,
                                'title': 'make breakfast', 'descrip': 'make dosa and vada',
                                'complete': True}]

def test_read_one_authenticated(test_todos):
    response = client.get("/todos/todo/1")
    assert response.status_code == 200
    assert response.json() == {'priority': 4, 'id': 1, 'owner_id': 1,
                                'title': 'make breakfast', 'descrip': 'make dosa and vada',
                                'complete': True}

def test_read_one_authenticated_not_found(test_todos):
    response = client.get("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail':'id does not exist'}

def test_create_todo():
    request_data = {
        'priority': 2,
        'title': 'make lunch',
        'descrip': 'make rice and curry',
        'complete': True
    }
    response = client.post("/todos/todo",json=request_data)
    assert  response.status_code==201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.descrip == request_data.get('descrip')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo(test_todos):
    request_data = {
        'priority': 2,
        'title': 'make breakfast',
        'descrip': 'make poori and jam',
        'complete': True
    }
    response = client.put("/todos/todo/1",json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.descrip == request_data.get('descrip')

def test_update_todo_not_found(test_todos):
    request_data = {
        'priority': 2,
        'title': 'make breakfast',
        'descrip': 'make poori and jam',
        'complete': True
    }
    response = client.put("/todos/todo/999",json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail':"id does not exist"}

def test_delete_todo(test_todos):
    response = client.delete("/todos/todo/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_todo_not_found(test_todos):
    response = client.delete("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': "id does not exist"}


