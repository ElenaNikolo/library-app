import { useEffect, useState } from 'react'

import { request } from '../api'

const EMPTY_FORM = {
  isbn: '',
  title: '',
  publisher: '',
  publication_year: '',
  description: '',
  category_id: '',
  author_ids: [],
  copies: '1',
}

export default function StaffBooks() {
  const [books, setBooks] = useState([])
  const [categories, setCategories] = useState([])
  const [authors, setAuthors] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // null = κλειστή φόρμα, 0 = νέο βιβλίο, θετικό = επεξεργασία εκείνου του βιβλίου.
  const [editingId, setEditingId] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [saving, setSaving] = useState(false)
  const [acting, setActing] = useState(null)
  const [actionError, setActionError] = useState('')

  // null = κλειστό, αλλιώς τα πεδία της μικρής φόρμας που φαίνεται μέσα στη φόρμα βιβλίου.
  const [newAuthor, setNewAuthor] = useState(null)
  const [newCategory, setNewCategory] = useState(null)
  const [adding, setAdding] = useState(false)

  useEffect(() => {
    request('/api/books')
      .then(setBooks)
      .catch((err) =>
        setError(
          err.status === 401 ? 'Η σύνδεσή σας έληξε. Συνδεθείτε ξανά.' : err.message,
        ),
      )
      .finally(() => setLoading(false))

    // Αν αποτύχουν, η φόρμα δεν μπορεί να συμπληρωθεί σωστά και το backend θα
    // απορρίψει την αποθήκευση με 400.
    request('/api/categories').then(setCategories).catch(() => setCategories([]))
    request('/api/authors').then(setAuthors).catch(() => setAuthors([]))
  }, [])

  function update(field, value) {
    setForm({ ...form, [field]: value })
  }

  function toggleAuthor(id, checked) {
    update(
      'author_ids',
      checked ? [...form.author_ids, id] : form.author_ids.filter((x) => x !== id),
    )
  }

  function openNew() {
    setForm(EMPTY_FORM)
    setEditingId(0)
    setActionError('')
  }

  function openEdit(book) {
    setForm({
      isbn: book.isbn,
      title: book.title,
      publisher: book.publisher || '',
      publication_year: book.publication_year ? String(book.publication_year) : '',
      description: book.description || '',
      category_id: String(book.category.id),
      author_ids: book.authors.map((a) => a.id),
      copies: '0',
    })
    setEditingId(book.id)
    setActionError('')
  }

  // Ο νέος συγγραφέας μπαίνει στο τέλος της λίστας, εκτός αλφαβητικής σειράς, μέχρι
  // την επόμενη φόρτωση της σελίδας.
  async function saveAuthor() {
    setAdding(true)
    setActionError('')

    try {
      const created = await request('/api/authors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          first_name: newAuthor.first_name.trim(),
          last_name: newAuthor.last_name.trim(),
        }),
      })

      setAuthors((current) => [...current, created])
      setForm((current) => ({
        ...current,
        author_ids: [...current.author_ids, created.id],
      }))
      setNewAuthor(null)
    } catch (err) {
      setActionError(
        err.status === 422 ? 'Συμπληρώστε όνομα και επώνυμο.' : err.message,
      )
    }

    setAdding(false)
  }

  async function saveCategory() {
    setAdding(true)
    setActionError('')

    try {
      const created = await request('/api/categories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newCategory.trim() }),
      })

      setCategories((current) => [...current, created])
      setForm((current) => ({ ...current, category_id: String(created.id) }))
      setNewCategory(null)
    } catch (err) {
      setActionError(
        err.status === 422 ? 'Συμπληρώστε όνομα κατηγορίας.' : err.message,
      )
    }

    setAdding(false)
  }

  // Τα αντίτυπα ονομάζονται {isbn}-{αριθμός} και δεν διαγράφονται ποτέ, οπότε η
  // αρίθμηση συνεχίζει από όσα υπάρχουν ήδη.
  async function addCopies(bookId, isbn, from, howMany) {
    let added = 0

    for (let number = from; number < from + howMany; number++) {
      try {
        await request(`/api/books/${bookId}/copies`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ copy_code: `${isbn}-${number}` }),
        })
        added += 1
      } catch {
        break
      }
    }

    return added
  }

  async function handleSubmit(event) {
    event.preventDefault()

    if (form.author_ids.length === 0) {
      setActionError('Επιλέξτε τουλάχιστον έναν συγγραφέα.')
      return
    }

    setSaving(true)
    setActionError('')

    // Τα πεδία της φόρμας είναι κείμενο, ενώ το backend περιμένει αριθμούς και
    // null στα κενά προαιρετικά.
    const payload = {
      isbn: form.isbn.trim(),
      title: form.title.trim(),
      publisher: form.publisher.trim() || null,
      publication_year: form.publication_year ? Number(form.publication_year) : null,
      description: form.description.trim() || null,
      category_id: Number(form.category_id),
      author_ids: form.author_ids,
    }

    const howMany = Number(form.copies)
    let message = ''

    try {
      if (editingId === 0) {
        const created = await request('/api/books', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })

        const added = await addCopies(created.id, payload.isbn, 1, howMany)
        if (added < howMany) {
          message = `Το βιβλίο δημιουργήθηκε με ${added} από ${howMany} αντίτυπα.`
        }
      } else {
        const saved = await request(`/api/books/${editingId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })

        if (howMany > 0) {
          const added = await addCopies(
            saved.id,
            payload.isbn,
            saved.total_copies + 1,
            howMany,
          )
          if (added < howMany) {
            message = `Οι αλλαγές αποθηκεύτηκαν. Προστέθηκαν ${added} από ${howMany} αντίτυπα.`
          }
        }
      }
    } catch (err) {
      setActionError(
        err.status === 401
          ? 'Η σύνδεσή σας έληξε. Συνδεθείτε ξανά.'
          : err.status === 422
            ? 'Ελέγξτε τα στοιχεία που συμπληρώσατε.'
            : err.message,
      )
      setSaving(false)
      return
    }

    try {
      setBooks(await request('/api/books'))
    } catch {
      message = 'Η ενέργεια ολοκληρώθηκε, αλλά η λίστα δεν ανανεώθηκε. Ανανέωσε τη σελίδα.'
    }

    setActionError(message)
    setEditingId(null)
    setSaving(false)
  }

  async function remove(book) {
    // Η διαγραφή είναι μη αναστρέψιμη, οπότε ζητάμε επιβεβαίωση.
    if (!window.confirm(`Να διαγραφεί το βιβλίο «${book.title}»;`)) {
      return
    }

    const id = book.id
    setActing(id)
    setActionError('')

    let done = false
    let shouldRefresh = false

    try {
      await request(`/api/books/${id}`, { method: 'DELETE' })
      done = true
    } catch (err) {
      setActionError(
        err.status === 401 ? 'Η σύνδεσή σας έληξε. Συνδεθείτε ξανά.' : err.message,
      )
      shouldRefresh = err.status === 409 || err.status === 404
    }

    if (done || shouldRefresh) {
      try {
        setBooks(await request('/api/books'))
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
        <h2>Βιβλία</h2>
        <p className="subtitle">
          {books.length === 1 ? '1 βιβλίο' : `${books.length} βιβλία`}
        </p>
      </div>

      {actionError && <p className="error">{actionError}</p>}

      {editingId === null ? (
        <button className="primary add-book" onClick={openNew}>Προσθήκη βιβλίου</button>
      ) : (
        <form className="book-form" onSubmit={handleSubmit}>
          <label className="field">
            ISBN
            <input
              value={form.isbn}
              onChange={(e) => update('isbn', e.target.value)}
              minLength={10}
              maxLength={20}
              required
              disabled={editingId > 0}
            />
          </label>

          <label className="field">
            Τίτλος
            <input
              value={form.title}
              onChange={(e) => update('title', e.target.value)}
              maxLength={200}
              required
            />
          </label>

          <div className="field-row">
            <label className="field">
              Εκδότης (προαιρετικό)
              <input
                value={form.publisher}
                onChange={(e) => update('publisher', e.target.value)}
                maxLength={120}
              />
            </label>

            <label className="field">
              Έτος έκδοσης (προαιρετικό)
              <input
                type="number"
                value={form.publication_year}
                onChange={(e) => update('publication_year', e.target.value)}
              />
            </label>
          </div>

          <label className="field">
            Περιγραφή (προαιρετικό)
            <textarea
              rows={3}
              value={form.description}
              onChange={(e) => update('description', e.target.value)}
            />
          </label>

          <label className="field">
            Κατηγορία
            <select
              value={form.category_id}
              onChange={(e) => update('category_id', e.target.value)}
              required
            >
              <option value="">Επιλέξτε κατηγορία</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>{category.name}</option>
              ))}
            </select>
          </label>

          {newCategory === null ? (
            <button
              type="button"
              className="secondary add-trigger"
              onClick={() => setNewCategory('')}
            >
              + Νέα κατηγορία
            </button>
          ) : (
            <div className="inline-add">
              {/* Το Enter εδώ θα υπέβαλλε τη φόρμα του βιβλίου. */}
              <input
                placeholder="Όνομα κατηγορίας"
                value={newCategory}
                onChange={(e) => setNewCategory(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && e.preventDefault()}
                maxLength={80}
              />
              <button type="button" className="secondary" onClick={saveCategory} disabled={adding}>
                Προσθήκη
              </button>
              <button type="button" className="secondary" onClick={() => setNewCategory(null)}>
                Ακύρωση
              </button>
            </div>
          )}

          <span className="field">
            Συγγραφείς
            <div className="checkbox-list">
              {authors.map((author) => (
                <label key={author.id}>
                  <input
                    type="checkbox"
                    checked={form.author_ids.includes(author.id)}
                    onChange={(e) => toggleAuthor(author.id, e.target.checked)}
                  />
                  {author.first_name} {author.last_name}
                </label>
              ))}
            </div>

            {newAuthor === null ? (
              <button
                type="button"
                className="secondary add-trigger"
                onClick={() => setNewAuthor({ first_name: '', last_name: '' })}
              >
                + Νέος συγγραφέας
              </button>
            ) : (
              <div className="inline-add">
                {/* Το Enter εδώ θα υπέβαλλε τη φόρμα του βιβλίου. */}
                <input
                  placeholder="Όνομα"
                  value={newAuthor.first_name}
                  onChange={(e) => setNewAuthor({ ...newAuthor, first_name: e.target.value })}
                  onKeyDown={(e) => e.key === 'Enter' && e.preventDefault()}
                  maxLength={60}
                />
                <input
                  placeholder="Επώνυμο"
                  value={newAuthor.last_name}
                  onChange={(e) => setNewAuthor({ ...newAuthor, last_name: e.target.value })}
                  onKeyDown={(e) => e.key === 'Enter' && e.preventDefault()}
                  maxLength={60}
                />
                <button type="button" className="secondary" onClick={saveAuthor} disabled={adding}>
                  Προσθήκη
                </button>
                <button type="button" className="secondary" onClick={() => setNewAuthor(null)}>
                  Ακύρωση
                </button>
              </div>
            )}
          </span>

          <label className="field">
            {editingId === 0 ? 'Αντίτυπα' : 'Προσθήκη αντιτύπων'}
            <select value={form.copies} onChange={(e) => update('copies', e.target.value)}>
              {(editingId === 0 ? [1, 2, 3, 4, 5] : [0, 1, 2, 3, 4, 5]).map((n) => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </label>

          <div className="loan-actions">
            <button type="submit" className="secondary" disabled={saving}>
              {saving ? 'Αποθήκευση...' : 'Αποθήκευση'}
            </button>
            <button type="button" className="secondary" onClick={() => setEditingId(null)}>
              Ακύρωση
            </button>
          </div>
        </form>
      )}

      {books.length === 0 ? (
        <p className="empty-state">Δεν υπάρχουν βιβλία.</p>
      ) : (
        <ul className="loans">
          {books.map((book) => (
            <li key={book.id}>
              <span className="loan-title">{book.title}</span>
              <span className="loan-code">
                {book.authors.map((a) => `${a.first_name} ${a.last_name}`).join(', ')}
              </span>

              <div className="loan-meta">
                <span className="chip">{book.category.name}</span>
                <span className="chip">{book.isbn}</span>
                <span className={book.total_copies > 0 ? 'badge' : 'badge empty'}>
                  {book.total_copies === 1 ? '1 αντίτυπο' : `${book.total_copies} αντίτυπα`}
                </span>
              </div>

              <div className="loan-actions">
                <button
                  className="secondary"
                  onClick={() => openEdit(book)}
                  disabled={acting === book.id}
                >
                  Επεξεργασία
                </button>
                <button
                  className="secondary"
                  onClick={() => remove(book)}
                  disabled={acting === book.id}
                >
                  Διαγραφή
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
