import { useEffect, useState } from 'react'

import { request } from '../api'
import { useAuth } from '../AuthContext'

const EMPTY_FORM = { username: '', email: '', password: '', role: 'LIBRARIAN' }

const ROLE_LABELS = {
  ADMIN: 'Διαχειριστής',
  LIBRARIAN: 'Βιβλιοθηκάριος',
  MEMBER: 'Μέλος',
}

export default function AdminUsers() {
  const { user: currentUser } = useAuth()

  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(EMPTY_FORM)
  const [adding, setAdding] = useState(false)
  const [acting, setActing] = useState(null)
  const [actionError, setActionError] = useState('')

  useEffect(() => {
    request('/api/users')
      .then(setUsers)
      .catch((err) =>
        setError(
          err.status === 401 ? 'Η σύνδεσή σας έληξε. Συνδεθείτε ξανά.' : err.message,
        ),
      )
      .finally(() => setLoading(false))
  }, [])

  function update(field, value) {
    setForm({ ...form, [field]: value })
  }

  async function handleSubmit(event) {
    event.preventDefault()

    setAdding(true)
    setActionError('')

    try {
      await request('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: form.username.trim(),
          email: form.email.trim(),
          password: form.password,
          role: form.role,
        }),
      })

      // Η λίστα έρχεται ταξινομημένη κατά username, οπότε τη ζητάμε ξανά.
      setUsers(await request('/api/users'))
      setForm(EMPTY_FORM)
      setShowForm(false)
    } catch (err) {
      setActionError(
        err.status === 422 ? 'Ελέγξτε τα στοιχεία που συμπληρώσατε.' : err.message,
      )
    }

    setAdding(false)
  }

  // Το backend περιμένει και τα δύο πεδία, οπότε στέλνουμε πάντα και τα δύο.
  async function save(target, role, isActive) {
    setActing(target.id)
    setActionError('')

    try {
      const saved = await request(`/api/users/${target.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role, is_active: isActive }),
      })
      setUsers((current) => current.map((u) => (u.id === saved.id ? saved : u)))
    } catch (err) {
      setActionError(
        err.status === 401 ? 'Η σύνδεσή σας έληξε. Συνδεθείτε ξανά.' : err.message,
      )
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
        <h2>Χρήστες</h2>
        <p className="subtitle">
          {users.length === 1 ? '1 χρήστης' : `${users.length} χρήστες`}
        </p>
      </div>

      {actionError && <p className="error">{actionError}</p>}

      {showForm ? (
        <form className="book-form" onSubmit={handleSubmit}>
          <label className="field">
            Όνομα χρήστη
            <input
              value={form.username}
              onChange={(e) => update('username', e.target.value)}
              minLength={3}
              maxLength={50}
              required
            />
          </label>

          <label className="field">
            Email
            <input
              type="email"
              value={form.email}
              onChange={(e) => update('email', e.target.value)}
              maxLength={120}
              required
            />
          </label>

          <label className="field">
            Κωδικός
            <input
              type="password"
              value={form.password}
              onChange={(e) => update('password', e.target.value)}
              minLength={8}
              required
            />
          </label>

          <label className="field">
            Ρόλος
            <select value={form.role} onChange={(e) => update('role', e.target.value)}>
              <option value="LIBRARIAN">Βιβλιοθηκάριος</option>
              <option value="ADMIN">Διαχειριστής</option>
            </select>
          </label>

          <div className="loan-actions">
            <button type="submit" className="secondary" disabled={adding}>
              {adding ? 'Αποθήκευση...' : 'Αποθήκευση'}
            </button>
            <button type="button" className="secondary" onClick={() => setShowForm(false)}>
              Ακύρωση
            </button>
          </div>
        </form>
      ) : (
        <button className="primary add-book" onClick={() => setShowForm(true)}>
          Προσθήκη χρήστη
        </button>
      )}

      <ul className="loans">
        {users.map((u) => {
          // Ο ίδιος ο διαχειριστής δεν αλλάζει τον ρόλο ή την κατάστασή του.
          const isSelf = u.id === currentUser.id
          const busy = isSelf || acting === u.id

          return (
            <li key={u.id}>
              <span className="loan-title">{u.username}</span>
              <span className="loan-code">{u.email}</span>

              <div className="loan-meta">
                <span className="chip">{ROLE_LABELS[u.role]}</span>
                <span className={u.is_active ? 'badge' : 'badge empty'}>
                  {u.is_active ? 'Ενεργός' : 'Ανενεργός'}
                </span>
                {isSelf && <span className="chip">Εσείς</span>}
              </div>

              <div className="loan-actions">
                {u.role !== 'MEMBER' && (
                  <select
                    className="role-select"
                    value={u.role}
                    disabled={busy}
                    onChange={(e) => save(u, e.target.value, u.is_active)}
                  >
                    <option value="LIBRARIAN">Βιβλιοθηκάριος</option>
                    <option value="ADMIN">Διαχειριστής</option>
                  </select>
                )}

                <button
                  className="secondary"
                  disabled={busy}
                  onClick={() => save(u, u.role, !u.is_active)}
                >
                  {u.is_active ? 'Απενεργοποίηση' : 'Ενεργοποίηση'}
                </button>
              </div>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
