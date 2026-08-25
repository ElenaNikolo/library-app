import { Navigate } from 'react-router-dom'

import { useAuth } from '../AuthContext'

export default function ProtectedRoute({ roles, children }) {
  const { user, loading } = useAuth()

  if (loading) {
    return <p className="loading">Φόρτωση...</p>
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  if (roles && !roles.includes(user.role)) {
    return <p className="error">Δεν έχετε δικαίωμα πρόσβασης σε αυτή τη σελίδα.</p>
  }

  return children
}
