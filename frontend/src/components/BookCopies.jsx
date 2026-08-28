import { useEffect, useState } from 'react'

import { request } from '../api'

const STATUS_LABELS = {
  AVAILABLE: 'Διαθέσιμο',
  ON_LOAN: 'Δανεισμένο',
  LOST: 'Χαμένο',
}

export default function BookCopies({ bookId }) {
  const [copies, setCopies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [acting, setActing] = useState(null)

  useEffect(() => {
    request(`/api/books/${bookId}/copies`)
      .then(setCopies)
      .catch((err) =>
        setError(
          err.status === 401 ? 'Η σύνδεσή σας έληξε. Συνδεθείτε ξανά.' : err.message,
        ),
      )
      .finally(() => setLoading(false))
  }, [bookId])

  // Το backend δέχεται μόνο AVAILABLE και LOST, ποτέ ON_LOAN.
  async function changeStatus(copy, status) {
    setActing(copy.id)
    setError('')

    try {
      const saved = await request(`/api/copies/${copy.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      })
      setCopies((current) => current.map((c) => (c.id === saved.id ? saved : c)))
    } catch (err) {
      setError(
        err.status === 401 ? 'Η σύνδεσή σας έληξε. Συνδεθείτε ξανά.' : err.message,
      )
    }

    setActing(null)
  }

  if (loading) {
    return <p className="loading">Φόρτωση...</p>
  }

  return (
    <div className="copies">
      {error && <p className="error">{error}</p>}

      {copies.length === 0 ? (
        <p className="empty-state">Δεν υπάρχουν αντίτυπα.</p>
      ) : (
        <ul>
          {copies.map((copy) => (
            <li key={copy.id}>
              <span className="loan-code">{copy.copy_code}</span>

              <span className={copy.status === 'AVAILABLE' ? 'badge' : 'badge empty'}>
                {STATUS_LABELS[copy.status]}
              </span>

              {copy.status === 'AVAILABLE' && (
                <button
                  className="secondary"
                  disabled={acting === copy.id}
                  onClick={() => changeStatus(copy, 'LOST')}
                >
                  Σήμανση ως χαμένο
                </button>
              )}

              {copy.status === 'LOST' && (
                <button
                  className="secondary"
                  disabled={acting === copy.id}
                  onClick={() => changeStatus(copy, 'AVAILABLE')}
                >
                  Επαναφορά σε διαθέσιμο
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
