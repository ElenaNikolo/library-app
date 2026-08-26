import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

import { useAuth } from '../AuthContext'

const DEMO_PASSWORD = 'Library2026!'

const DEMO_ACCOUNTS = [
  ['Member', 'maria'],
  ['Librarian', 'librarian'],
  ['Admin', 'admin'],
]

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')

    try {
      await login(username, password)
      navigate('/')
    } catch (err) {
      setError(err.message)
    }
  }

  function fillDemo(demoUsername) {
    setUsername(demoUsername)
    setPassword(DEMO_PASSWORD)
    setError('')
  }

  return (
    <div className="auth">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Σύνδεση</h2>
        <p className="subtitle">Εισάγετε τα στοιχεία του λογαριασμού σας</p>

        {location.state?.registered && (
          <p className="badge">Η εγγραφή ολοκληρώθηκε. Συνδεθείτε με τα στοιχεία σας.</p>
        )}

        {error && <p className="error">{error}</p>}

        <label className="field">
          Όνομα χρήστη
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="π.χ. maria"
            required
          />
        </label>

        <label className="field">
          Κωδικός
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>

        <button type="submit" className="primary">Σύνδεση</button>

        <div className="demo">
          <span className="demo-label">Demo accounts</span>

          <div className="demo-buttons">
            {DEMO_ACCOUNTS.map(([label, demoUsername]) => (
              <button key={demoUsername} type="button" onClick={() => fillDemo(demoUsername)}>
                {label}
              </button>
            ))}
          </div>
        </div>

        <p className="subtitle">
          Δεν έχετε λογαριασμό; <Link to="/register">Εγγραφή</Link>
        </p>
      </form>
    </div>
  )
}
