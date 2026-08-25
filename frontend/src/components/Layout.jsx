import { Link, Outlet } from 'react-router-dom'

import { useAuth } from '../AuthContext'

const ROLE_LABELS = {
  MEMBER: 'Member',
  LIBRARIAN: 'Librarian',
  ADMIN: 'Admin',
}

export default function Layout() {
  const { user, loading, logout } = useAuth()

  if (loading) {
    return <p className="loading">Φόρτωση...</p>
  }

  return (
    <>
      <header className="header">
        <div className="header-inner">
          <Link to="/" className="brand">
            <svg
              className="logo"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M12 8C10.4 6 7.6 5 4 5v12c3.6 0 6.4 1 8 3z" />
              <path d="M12 8c1.6-2 4.4-3 8-3v12c-3.6 0-6.4 1-8 3z" />
            </svg>
            Βιβλιοθήκη
          </Link>

          <nav>
            {user ? (
              <>
                <Link to="/loans" className="nav-link">Οι δανεισμοί μου</Link>

                {user.role === 'MEMBER' && (
                  <Link to="/requests" className="nav-link">Τα αιτήματά μου</Link>
                )}

                {['ADMIN', 'LIBRARIAN'].includes(user.role) && (
                  <Link to="/staff/loans" className="nav-link">Δανεισμοί</Link>
                )}

                <span className="user">
                  <span className="avatar">{user.username.charAt(0).toUpperCase()}</span>
                  <span className="user-text">
                    <strong>{user.username}</strong>
                    <span className="user-role">{ROLE_LABELS[user.role]}</span>
                  </span>
                </span>

                <button className="secondary" onClick={logout}>Αποσύνδεση</button>
              </>
            ) : (
              <Link to="/login" className="secondary">Σύνδεση</Link>
            )}
          </nav>
        </div>
      </header>

      <main className="page">
        <Outlet />
      </main>
    </>
  )
}
