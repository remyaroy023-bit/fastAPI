from fastapi import FastAPI,Body

app = FastAPI()
BOOKS = [
    {'title': 'title1','author' : 'author1','subject':'arts'},
{'title': 'title1','author' : 'author11','subject':'arts'},
{'title': 'title15','author' : 'author14','subject':'science'},
{'title': 'title5','author' : 'author1','subject':'cs'},
{'title': 'title8','author' : 'author19','subject':'maths'},
{'title': 'title17','author' : 'author13','subject':'history'}
]
@app.get("/books/all")
async def read_all_books():
    print('hi')
    return BOOKS


@app.get("/books/title/{title}")
async def read_book(title:str):
    for book in BOOKS:
        if book['title'].casefold() == title.casefold():
            return book

@app.get("/books/subject/")
async def read_by_subject(subject:str):
    books_returned = []
    for book in BOOKS:
        if book['subject'].casefold() == subject.casefold():
            books_returned.append(book)
    return books_returned

@app.get("/books/author/")
async def read_by_subject(author:str):
    books_returned = []
    for book in BOOKS:
        if book['author'].casefold() == author.casefold():
            books_returned.append(book)
    return books_returned

@app.get("/books/author/{author}/")
async def read_by_subject(author:str, subject:str):
    books_returned = []
    for book in BOOKS:
        if book['subject'].casefold() == subject.casefold() and book['author'].casefold() == author.casefold():
            books_returned.append(book)
    return books_returned

@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def create_book(update_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book

@app.delete("/books/delete_book/{title}")
async def create_book(title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == title.casefold():
            BOOKS.pop(i)
            break

