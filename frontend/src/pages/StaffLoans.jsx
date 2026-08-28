import { useEffect, useState } from 'react'

import { request } from '../api'

const STATUS_LABELS = {
  ACTIVE: 'Σε δανεισμό',
  RETURNED: 'Επιστράφηκε',
}

function formatDate(value) {
  return new Date(value).toLocaleDateString('el-GR')
}

export default function StaffLoans() {
  const [loans, setLoans] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    request('/api/loans')
      .then(setLoans)
      .catch((err) => setError(err.message))
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
        <h2>Δανεισμοί</h2>
        <p className="subtitle">
          {loans.length === 1 ? '1 δανεισμός' : `${loans.length} δανεισμοί`}
        </p>
      </div>

      {loans.length === 0 ? (
        <p className="empty-state">Δεν υπάρχουν δανεισμοί.</p>
      ) : (
        <ul className="loans">
          {loans.map((loan) => (
            <li key={loan.id}>
              <span className="loan-title">{loan.book_title}</span>
              <span className="loan-code">
                {loan.member_name} · Αντίτυπο {loan.copy_code}
              </span>

              <div className="loan-meta">
                <span className={loan.status === 'ACTIVE' ? 'badge' : 'badge empty'}>
                  {STATUS_LABELS[loan.status]}
                </span>
                <span className="chip">Επιστροφή έως {formatDate(loan.due_date)}</span>

                {loan.days_overdue > 0 && (
                  <span className="badge overdue">
                    Καθυστέρηση {loan.days_overdue} ημερών
                  </span>
                )}

                {Number(loan.fine_amount) > 0 && (
                  <span className="badge overdue">Πρόστιμο {loan.fine_amount} €</span>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
