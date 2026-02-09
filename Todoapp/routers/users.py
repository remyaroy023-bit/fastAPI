from fastapi import APIRouter,Depends,HTTPException,Path
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from ..models import Todos, Users
from ..database import Sessionlocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/users',
    tags=['users']
)
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

class UpdateNumber(BaseModel):
    phone_number: str
    new_number: str = Field(min_length=7)


@router.get("/users",status_code=status.HTTP_200_OK)
async def read_user(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail='User not Found')

    return db.query(Users).filter(Users.id == user.get('user_id')).first()




@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password( user: user_dependency, db: db_dependency,user_verification: UserVerification):
    if not user:
        raise HTTPException(status_code=401, detail='User not Found')
    user_model = db.query(Users).filter(Users.id == user.get('user_id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Incorrect Password')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put("/{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number( user: user_dependency, db: db_dependency,phone_number:str):
    if not user:
        raise HTTPException(status_code=401, detail='User not Found')
    user_model = db.query(Users).filter(Users.id == user.get('user_id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
