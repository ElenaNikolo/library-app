from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.catalog import AuthorResponse, BookResponse, CategoryResponse
from app.services import catalog

router = APIRouter(prefix="/api", tags=["catalog"])


@router.get("/categories", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return catalog.list_categories(db)


@router.get("/authors", response_model=list[AuthorResponse])
def list_authors(db: Session = Depends(get_db)):
    return catalog.list_authors(db)


@router.get("/books", response_model=list[BookResponse])
def list_books(
    title: str | None = None,
    category_id: int | None = None,
    db: Session = Depends(get_db),
):
    books = []
    for book in catalog.search_books(db, title, category_id):
        total, available = catalog.count_copies(db, book.id)
        books.append(
            BookResponse(
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
        )
    return books


@router.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = catalog.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Το βιβλίο δεν βρέθηκε")

    total, available = catalog.count_copies(db, book.id)
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
