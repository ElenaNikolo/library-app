import { useEffect, useState } from 'react'

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

export default function StaffRequests() {
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [acting, setActing] = useState(null)
  const [actionError, setActionError] = useState('')

  useEffect(() => {
    request('/api/requests')
      .then(setRequests)
      .catch((err) =>
        setError(
          err.status === 401 ? 'Η σύνδεσή σας έληξε. Συνδεθείτε ξανά.' : err.message,
        ),
      )
      .finally(() => setLoading(false))
  }, [])

  async function act(id, action) {
    setActing(id)
    setActionError('')

    let done = false
    let shouldRefresh = false

    try {
      await request(`/api/requests/${id}/${action}`, { method: 'POST' })
      done = true
    } catch (err) {
      setActionError(
        err.status === 401 ? 'Η σύνδεσή σας έληξε. Συνδεθείτε ξανά.' : err.message,
      )
      shouldRefresh = err.status === 409
    }

    if (done || shouldRefresh) {
      try {
        setRequests(await request('/api/requests'))
      } catch {
        if (done) {
          setActionError(
            'Η ενέργεια ολοκληρώθηκε, αλλά η λίστα δεν ανανεώθηκε. Ανανέωσε τη σελίδα.',
          )
        }
        // Αλλιώς κρατάμε το μήνυμα του σφάλματος, που είναι πιο χρήσιμο.
      }
    }

    setActing(null)
  }

  if (loading) {
    return <p className="loading">Φόρτωση...</p>
  }

  if (error) {
    return <p className="error">{error}</p>
  }

  return (
    <div>
      <div className="page-head">
        <h2>Αιτήματα</h2>
        <p className="subtitle">
          {requests.length === 1 ? '1 αίτημα' : `${requests.length} αιτήματα`}
        </p>
      </div>

      {actionError && <p className="error">{actionError}</p>}

      {requests.length === 0 ? (
        <p className="empty-state">Δεν υπάρχουν αιτήματα.</p>
      ) : (
        <ul className="loans">
          {requests.map((item) => (
            <li key={item.id}>
              <span className="loan-title">{item.book_title}</span>
              <span className="loan-code">{item.member_name}</span>

              <div className="loan-meta">
                <span className={STATUS_CLASSES[item.status]}>
                  {STATUS_LABELS[item.status]}
                </span>
                <span className="chip">Αίτημα {formatDate(item.request_date)}</span>

                {item.decided_date && (
                  <span className="chip">Απόφαση {formatDate(item.decided_date)}</span>
                )}
              </div>

              {item.status === 'PENDING' && (
                <div className="loan-actions">
                  <button
                    className="secondary"
                    onClick={() => act(item.id, 'approve')}
                    disabled={acting === item.id}
                  >
                    Έγκριση
                  </button>
                  <button
                    className="secondary"
                    onClick={() => act(item.id, 'reject')}
                    disabled={acting === item.id}
                  >
                    Απόρριψη
                  </button>
                </div>
              )}

              {item.status === 'APPROVED' && (
                <div className="loan-actions">
                  <button
                    className="secondary"
                    onClick={() => act(item.id, 'fulfill')}
                    disabled={acting === item.id}
                  >
                    Παραλαβή
                  </button>
                  <button
                    className="secondary"
                    onClick={() => act(item.id, 'cancel')}
                    disabled={acting === item.id}
                  >
                    Ακύρωση
                  </button>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
