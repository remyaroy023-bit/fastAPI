from sqlalchemy import create_engine,text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..database import Base
from fastapi.testclient import TestClient
import pytest
from ..models import Todos,Users
from ..routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args= {"check_same_thread":False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'remi','user_id': 1,'role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_todos():
    db = TestingSessionLocal()
    db.query(Todos).delete()
    db.commit()
    todo = Todos(
    title = 'make breakfast',
    descrip = 'make dosa and vada',
    priority = '4',
    complete = True,
    owner_id = 1
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    db.close()

@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    db.query(Users).delete()
    db.commit()
    user = Users(
    email='remi.com',
    username = 'remi',
    firstname = 'remi',
    lastname = 'ry',
    hashed_password = bcrypt_context.hash('test123'),
    is_active = True,
    role = 'admin',
    phone_number = '123456'
    )

    db.add(user)
    db.commit()

    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()



