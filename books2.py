from typing import Optional

from fastapi import FastAPI,Path,Query,HTTPException
from pydantic import BaseModel,Field
from starlette import status

app = FastAPI()
class Book:
    id: int
    title:str
    author:str
    descript:str
    rating:int
    def __init__(self,id,title,author,descript,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.descript = descript
        self.rating = rating
        self.published_date =published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='id not needed in create',default=None)
    title: str = Field(min_length=3)
    author: str =Field(min_length=1)
    descript: str= Field(min_length=2,max_length=100)
    rating: int =Field(gt=0, lt=6)
    published_date:int = Field(gt=1999,lt=2031)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"A new book",
                "author":"remi",
                "descript":"great",
                "rating":5,
                "published_date":2012

            }
        }
    }



BOOKS = [
    Book(1,'title 1','author 1','good',5,2012),
    Book(2,'title 2','author 2','ok',3,2024),
    Book(3,'title 3','author 1','bad',1,2022),
    Book(4,'title 4','author 4','good',5,2022)
]
@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.post("/books-create",status_code=status.HTTP_201_CREATED)
async def create_books(book_req: BookRequest):
    new_book = Book(**book_req.model_dump())
    BOOKS.append(set_book_id(new_book))

def set_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.get("/books/id/{book_id}",status_code=status.HTTP_200_OK)
async def read_book_id(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404,detail='not found')

@app.get("/books/rating/",status_code=status.HTTP_200_OK)
async def read_book_rating(rating:int = Query(lt=6,gt=0)):
    book_list = []
    for book in BOOKS:
        if book.rating == rating:
            book_list.append(book)
    return book_list

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(update_book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == update_book.id:
            BOOKS[i] = update_book
            book_changed=True
    if not book_changed:
        raise HTTPException(status_code=404,detail='not found')

@app.delete("/books/delete_book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt = 0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='not found')

@app.get("/books/date/",status_code=status.HTTP_200_OK)
async def read_book_date(published_date:int = Query(gt=1999,lt=2031)):
    book_list = []
    for book in BOOKS:
        if book.published_date == published_date:
            book_list.append(book)
    return book_list