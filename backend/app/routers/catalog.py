from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_staff
from app.models.book import Book
from app.schemas.catalog import (
    AuthorCreate,
    AuthorResponse,
    BookCreate,
    BookResponse,
    CategoryResponse,
)
from app.services import catalog

router = APIRouter(prefix="/api", tags=["catalog"])


def book_response(book: Book, total: int, available: int) -> BookResponse:
    return BookResponse(
        id=book.id,
        isbn=book.isbn,
        title=book.title,
        publisher=book.publisher,
        publication_year=book.publication_year,
        description=book.description,
        category=book.category,
        authors=book.authors,
        total_copies=total,
        available_copies=available,
    )


@router.get("/categories", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return catalog.list_categories(db)


@router.get("/authors", response_model=list[AuthorResponse])
def list_authors(db: Session = Depends(get_db)):
    return catalog.list_authors(db)


@router.post(
    "/authors",
    response_model=AuthorResponse,
    status_code=201,
    dependencies=[Depends(require_staff)],
)
def create_author(data: AuthorCreate, db: Session = Depends(get_db)):
    return catalog.create_author(db, data)


@router.get("/books", response_model=list[BookResponse])
def list_books(
    title: str | None = None,
    category_id: int | None = None,
    db: Session = Depends(get_db),
):
    books = []
    for book in catalog.search_books(db, title, category_id):
        total, available = catalog.count_copies(db, book.id)
        books.append(book_response(book, total, available))
    return books


@router.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = catalog.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Το βιβλίο δεν βρέθηκε")

    total, available = catalog.count_copies(db, book.id)
    return book_response(book, total, available)


@router.post(
    "/books",
    response_model=BookResponse,
    status_code=201,
    dependencies=[Depends(require_staff)],
)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    try:
        book = catalog.create_book(db, data)
    except catalog.BookAlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except catalog.InvalidBookDataError as error:
        raise HTTPException(status_code=400, detail=str(error))

    total, available = catalog.count_copies(db, book.id)
    return book_response(book, total, available)


@router.put(
    "/books/{book_id}",
    response_model=BookResponse,
    dependencies=[Depends(require_staff)],
)
def update_book(book_id: int, data: BookCreate, db: Session = Depends(get_db)):
    book = catalog.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Το βιβλίο δεν βρέθηκε")

    try:
        book = catalog.update_book(db, book, data)
    except catalog.BookAlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except catalog.InvalidBookDataError as error:
        raise HTTPException(status_code=400, detail=str(error))

    total, available = catalog.count_copies(db, book.id)
    return book_response(book, total, available)


@router.delete(
    "/books/{book_id}",
    status_code=204,
    dependencies=[Depends(require_staff)],
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = catalog.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Το βιβλίο δεν βρέθηκε")

    try:
        catalog.delete_book(db, book)
    except catalog.BookHasLoansError as error:
        raise HTTPException(status_code=409, detail=str(error))
