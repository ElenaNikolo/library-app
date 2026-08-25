import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { request } from '../api'

const STATUS_LABELS = {
  PENDING: 'Σε αναμονή',
  APPROVED: 'Εγκρίθηκε',
  REJECTED: 'Απορρίφθηκε',
  FULFILLED: 'Παραλήφθηκε',
  CANCELLED: 'Ακυρώθηκε',
}

const STATUS_CLASSES = {
  PENDING: 'badge empty',
  APPROVED: 'badge',
  REJECTED: 'badge overdue',
  FULFILLED: 'badge',
  CANCELLED: 'badge empty',
}

function formatDate(value) {
  return new Date(value).toLocaleDateString('el-GR')
}

export default function MyRequests() {
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    request('/api/requests/my')
      .then(setRequests)
      .catch((err) =>
        setError(
          err.status === 401 ? 'Η σύνδεσή σας έληξε. Συνδεθείτε ξανά.' : err.message,
        ),
      )
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return <p className="loading">Φόρτωση...</p>
  }

  if (error) {
    return <p className="error">{error}</p>
  }

  return (
    <div>
      <div className="page-head">
        <h2>Τα αιτήματά μου</h2>
        <p className="subtitle">
          {requests.length === 1 ? '1 αίτημα' : `${requests.length} αιτήματα`}
        </p>
      </div>

      {requests.length === 0 ? (
        <p className="empty-state">Δεν έχετε κάνει κάποιο αίτημα.</p>
      ) : (
        <ul className="loans">
          {requests.map((item) => (
            <li key={item.id}>
              <Link to={`/books/${item.book_id}`} className="loan-title">
                {item.book_title}
              </Link>

              <div className="loan-meta">
                <span className={STATUS_CLASSES[item.status]}>
                  {STATUS_LABELS[item.status]}
                </span>
                <span className="chip">Αίτημα {formatDate(item.request_date)}</span>

                {item.decided_date && (
                  <span className="chip">Απόφαση {formatDate(item.decided_date)}</span>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
