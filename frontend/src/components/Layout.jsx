import { Link, NavLink, Outlet } from 'react-router-dom'

import { useAuth } from '../AuthContext'

const ROLE_LABELS = {
  MEMBER: 'Member',
  LIBRARIAN: 'Librarian',
  ADMIN: 'Admin',
}

const navClass = ({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')

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
                {user.role === 'MEMBER' && (
                  <NavLink to="/loans" className={navClass}>Οι δανεισμοί μου</NavLink>
                )}

                {user.role === 'MEMBER' && (
                  <NavLink to="/requests" className={navClass}>Τα αιτήματά μου</NavLink>
                )}

                {['ADMIN', 'LIBRARIAN'].includes(user.role) && (
                  <NavLink to="/staff/books" className={navClass}>Βιβλία</NavLink>
                )}

                {['ADMIN', 'LIBRARIAN'].includes(user.role) && (
                  <NavLink to="/staff/loans" className={navClass}>Δανεισμοί</NavLink>
                )}

                {['ADMIN', 'LIBRARIAN'].includes(user.role) && (
                  <NavLink to="/staff/requests" className={navClass}>Αιτήματα</NavLink>
                )}

                <div className="user-actions">
                  <span className="user">
                    <span className="avatar">{user.username.charAt(0).toUpperCase()}</span>
                    <span className="user-text">
                      <strong>{user.username}</strong>
                      <span className="user-role">{ROLE_LABELS[user.role]}</span>
                    </span>
                  </span>

                  <button className="secondary" onClick={logout}>Αποσύνδεση</button>
                </div>
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
