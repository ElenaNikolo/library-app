const BASE_URL = 'http://127.0.0.1:8000'

export function getToken() {
  return localStorage.getItem('token')
}

export function setToken(token) {
  localStorage.setItem('token', token)
}

export function clearToken() {
  localStorage.removeItem('token')
}

export async function request(path, options = {}) {
  const token = getToken()
  const headers = { ...options.headers }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(BASE_URL + path, { ...options, headers })

  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    // Στα 422 το detail είναι λίστα σφαλμάτων validation, όχι κείμενο.
    const detail = typeof body.detail === 'string' ? body.detail : ''
    const error = new Error(detail || 'Κάτι πήγε στραβά')
    error.status = response.status
    throw error
  }

  return response.json()
}
