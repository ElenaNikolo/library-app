import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { request } from '../api'

const EMPTY_FORM = {
  username: '',
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  phone: '',
  address: '',
}

export default function Register() {
  const navigate = useNavigate()

  const [form, setForm] = useState(EMPTY_FORM)
  const [error, setError] = useState('')
  const [sending, setSending] = useState(false)

  function update(field, value) {
    setForm({ ...form, [field]: value })
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSending(true)
    setError('')

    try {
      await request('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          // Τα προαιρετικά πεδία πάνε ως null, ώστε να μην αποθηκευτεί κενό κείμενο.
          phone: form.phone.trim() || null,
          address: form.address.trim() || null,
        }),
      })

      navigate('/login', { state: { registered: true } })
    } catch (err) {
      setError(
        err.status === 422 ? 'Ελέγξτε τα στοιχεία που συμπληρώσατε.' : err.message,
      )
      setSending(false)
    }
  }

  return (
    <div className="auth">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Εγγραφή μέλους</h2>
        <p className="subtitle">Συμπληρώστε τα στοιχεία σας</p>

        {error && <p className="error">{error}</p>}

        <label className="field">
          Όνομα χρήστη
          <input
            value={form.username}
            onChange={(e) => update('username', e.target.value)}
            placeholder="π.χ. maria"
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
            placeholder="Τουλάχιστον 8 χαρακτήρες"
            minLength={8}
            required
          />
        </label>

        <div className="field-row">
          <label className="field">
            Όνομα
            <input
              value={form.first_name}
              onChange={(e) => update('first_name', e.target.value)}
              maxLength={60}
              required
            />
          </label>

          <label className="field">
            Επώνυμο
            <input
              value={form.last_name}
              onChange={(e) => update('last_name', e.target.value)}
              maxLength={60}
              required
            />
          </label>
        </div>

        <label className="field">
          Τηλέφωνο (προαιρετικό)
          <input
            value={form.phone}
            onChange={(e) => update('phone', e.target.value)}
            maxLength={20}
          />
        </label>

        <label className="field">
          Διεύθυνση (προαιρετικό)
          <input
            value={form.address}
            onChange={(e) => update('address', e.target.value)}
            maxLength={200}
          />
        </label>

        <button type="submit" className="primary" disabled={sending}>
          {sending ? 'Αποστολή...' : 'Εγγραφή'}
        </button>

        <p className="auth-switch">
          Έχετε ήδη λογαριασμό; <Link to="/login">Σύνδεση</Link>
        </p>
      </form>
    </div>
  )
}
