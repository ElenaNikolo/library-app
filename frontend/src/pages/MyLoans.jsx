import { useEffect, useState } from 'react'

import { request } from '../api'

const STATUS_LABELS = {
  ACTIVE: 'Σε δανεισμό',
  RETURNED: 'Επιστράφηκε',
}

function formatDate(value) {
  return new Date(value).toLocaleDateString('el-GR')
}

export default function MyLoans() {
  const [loans, setLoans] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    request('/api/loans/my')
      .then(setLoans)
      .catch((err) => setError(err.message))
  }, [])

  if (error) {
    return <p className="error">{error}</p>
  }

  return (
    <div>
      <div className="page-head">
        <h2>Οι δανεισμοί μου</h2>
        <p className="subtitle">
          {loans.length === 1 ? '1 δανεισμός' : `${loans.length} δανεισμοί`}
        </p>
      </div>

      {loans.length === 0 ? (
        <p className="empty-state">Δεν έχετε δανειστεί κάποιο βιβλίο.</p>
      ) : (
        <ul className="loans">
          {loans.map((loan) => (
            <li key={loan.id}>
              <span className="loan-title">{loan.book_title}</span>
              <span className="loan-code">Αντίτυπο {loan.copy_code}</span>

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
