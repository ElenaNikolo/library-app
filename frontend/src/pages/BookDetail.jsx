import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { useAuth } from '../AuthContext'
import { request } from '../api'

export default function BookDetail() {
  const { id } = useParams()
  const { user } = useAuth()
  const [book, setBook] = useState(null)
  const [error, setError] = useState('')
  const [sending, setSending] = useState(false)
  const [requested, setRequested] = useState(false)
  const [requestError, setRequestError] = useState('')

  // Το id έρχεται από το URL, οπότε μπορεί να μην είναι καν αριθμός.
  const validId = /^\d+$/.test(id)

  useEffect(() => {
    if (!validId) {
      return
    }

    request(`/api/books/${id}`)
      .then(setBook)
      .catch((err) => setError(err.message))
  }, [id, validId])

  async function handleRequest() {
    setSending(true)
    setRequestError('')

    try {
      await request('/api/requests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ book_id: book.id }),
      })
      setRequested(true)
    } catch (err) {
      setRequestError(
        err.status === 401 ? 'Η σύνδεσή σας έληξε. Συνδεθείτε ξανά.' : err.message,
      )
    } finally {
      setSending(false)
    }
  }

  if (!validId) {
    return <p className="error">Το βιβλίο δεν βρέθηκε</p>
  }

  if (error) {
    return <p className="error">{error}</p>
  }

  if (!book) {
    return <p className="loading">Φόρτωση...</p>
  }

  return (
    <div>
      <Link to="/" className="back-link">← Πίσω στον κατάλογο</Link>

      <div className="page-head">
        <h2>{book.title}</h2>
        <p className="subtitle">
          {book.authors.map((a) => `${a.first_name} ${a.last_name}`).join(', ')}
        </p>
      </div>

      <div className="detail-meta">
        <span className="chip">{book.category.name}</span>
        <span className={book.available_copies > 0 ? 'badge' : 'badge empty'}>
          {book.available_copies} από {book.total_copies} διαθέσιμα
        </span>
      </div>

      <p className="book-description">{book.description}</p>

      <ul className="book-info">
        <li><strong>ISBN</strong> {book.isbn}</li>
        <li><strong>Εκδότης</strong> {book.publisher}</li>
        <li><strong>Έτος έκδοσης</strong> {book.publication_year}</li>
      </ul>

      <div className="book-actions">
        {!user && (
          <Link to="/login">Συνδεθείτε για να ζητήσετε το βιβλίο</Link>
        )}

        {user?.role === 'MEMBER' && !requested && (
          <button className="primary" onClick={handleRequest} disabled={sending}>
            {sending ? 'Αποστολή...' : 'Αίτημα δανεισμού'}
          </button>
        )}

        {requested && <span className="badge">Το αίτημα καταχωρήθηκε.</span>}

        {requestError && <p className="error">{requestError}</p>}
      </div>
    </div>
  )
}
