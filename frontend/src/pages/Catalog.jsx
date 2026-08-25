import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { request } from '../api'

export default function Catalog() {
  const [books, setBooks] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    request('/api/books')
      .then(setBooks)
      .catch((err) => setError(err.message))
  }, [])

  if (error) {
    return <p className="error">{error}</p>
  }

  return (
    <div>
      <div className="page-head">
        <h2>Κατάλογος</h2>
        <p className="subtitle">{books.length} βιβλία</p>
      </div>

      <ul className="books">
        {books.map((book) => (
          <li key={book.id}>
            <Link to={`/books/${book.id}`} className="book-link">
              <span className="book-title">{book.title}</span>
              <span className="book-authors">
                {book.authors.map((a) => `${a.first_name} ${a.last_name}`).join(', ')}
              </span>

              <div className="book-meta">
                <span className="chip">{book.category.name}</span>
                <span className={book.available_copies > 0 ? 'badge' : 'badge empty'}>
                  {book.available_copies} από {book.total_copies} διαθέσιμα
                </span>
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
