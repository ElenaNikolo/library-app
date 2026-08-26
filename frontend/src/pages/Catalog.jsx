import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { request } from '../api'

export default function Catalog() {
  const [books, setBooks] = useState([])
  const [categories, setCategories] = useState([])
  const [title, setTitle] = useState('')
  const [categoryId, setCategoryId] = useState('')
  const [filtered, setFiltered] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadBooks(titleValue, categoryValue) {
    const searchTitle = titleValue.trim()
    const params = new URLSearchParams()

    if (searchTitle) {
      params.set('title', searchTitle)
    }

    // Η κενή κατηγορία σημαίνει «όλες». Δεν στέλνουμε category_id χωρίς τιμή,
    // γιατί το backend το απορρίπτει με 422.
    if (categoryValue) {
      params.set('category_id', categoryValue)
    }

    // Το κρατάμε χωριστά από τα πεδία, ώστε το μήνυμα του άδειου
    // αποτελέσματος να δείχνει την αναζήτηση που έγινε και όχι ό,τι
    // πληκτρολογεί ο χρήστης μετά.
    setFiltered(Boolean(searchTitle || categoryValue))
    setLoading(true)
    setError('')

    const query = params.toString()

    try {
      setBooks(await request(query ? `/api/books?${query}` : '/api/books'))
    } catch (err) {
      setBooks([])
      setError(err.message)
    }

    setLoading(false)
  }

  useEffect(() => {
    // Αν οι κατηγορίες δεν φορτωθούν, μένει διαθέσιμη η αναζήτηση με τίτλο.
    request('/api/categories')
      .then(setCategories)
      .catch(() => setCategories([]))

    // Το πρώτο φόρτωμα δεν έχει φίλτρα, οπότε δεν χρειάζεται το loadBooks.
    request('/api/books')
      .then(setBooks)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  function handleSubmit(event) {
    event.preventDefault()
    loadBooks(title, categoryId)
  }

  function handleClear() {
    setTitle('')
    setCategoryId('')
    loadBooks('', '')
  }

  return (
    <div>
      <div className="page-head">
        <h2>Κατάλογος</h2>
        <p className="subtitle">
          {books.length === 1 ? '1 βιβλίο' : `${books.length} βιβλία`}
        </p>
      </div>

      <form className="toolbar" onSubmit={handleSubmit}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Αναζήτηση με τίτλο"
        />

        <select value={categoryId} onChange={(e) => setCategoryId(e.target.value)}>
          <option value="">Όλες οι κατηγορίες</option>

          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>

        <button type="submit" className="primary">Αναζήτηση</button>

        {(title || categoryId) && (
          <button type="button" className="secondary" onClick={handleClear}>
            Καθαρισμός
          </button>
        )}
      </form>

      {loading && <p className="loading">Φόρτωση...</p>}

      {error && !loading && <p className="error">{error}</p>}

      {!loading &&
        !error &&
        (books.length === 0 ? (
          <p className="empty-state">
            {filtered
              ? 'Δεν βρέθηκαν βιβλία με αυτά τα κριτήρια.'
              : 'Δεν υπάρχουν βιβλία.'}
          </p>
        ) : (
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
        ))}
    </div>
  )
}
