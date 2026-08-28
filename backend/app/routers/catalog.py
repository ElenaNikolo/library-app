from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_staff
from app.models.book import Book
from app.schemas.catalog import (
    AuthorCreate,
    AuthorResponse,
    BookCopyCreate,
    BookCopyResponse,
    BookCopyUpdate,
    BookCreate,
    BookResponse,
    CategoryCreate,
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


@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=201,
    dependencies=[Depends(require_staff)],
)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return catalog.create_category(db, data)
    except catalog.CategoryAlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=str(error))


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
    except catalog.BookHasRequestsError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.get(
    "/books/{book_id}/copies",
    response_model=list[BookCopyResponse],
    dependencies=[Depends(require_staff)],
)
def list_copies(book_id: int, db: Session = Depends(get_db)):
    book = catalog.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Το βιβλίο δεν βρέθηκε")

    return catalog.list_copies(db, book.id)


@router.post(
    "/books/{book_id}/copies",
    response_model=BookCopyResponse,
    status_code=201,
    dependencies=[Depends(require_staff)],
)
def create_copy(book_id: int, data: BookCopyCreate, db: Session = Depends(get_db)):
    book = catalog.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Το βιβλίο δεν βρέθηκε")

    try:
        return catalog.create_copy(db, book, data)
    except catalog.CopyCodeExistsError as error:
        raise HTTPException(status_code=409, detail=str(error))


@router.put(
    "/copies/{copy_id}",
    response_model=BookCopyResponse,
    dependencies=[Depends(require_staff)],
)
def update_copy(copy_id: int, data: BookCopyUpdate, db: Session = Depends(get_db)):
    copy = catalog.get_copy(db, copy_id)
    if copy is None:
        raise HTTPException(status_code=404, detail="Το αντίτυπο δεν βρέθηκε")

    try:
        return catalog.update_copy_status(db, copy, data)
    except catalog.CopyOnLoanError as error:
        raise HTTPException(status_code=409, detail=str(error))
