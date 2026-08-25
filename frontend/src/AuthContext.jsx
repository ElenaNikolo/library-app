import { createContext, useContext, useEffect, useState } from 'react'

import { clearToken, getToken, request, setToken } from './api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!getToken()) {
      setLoading(false)
      return
    }

    request('/api/auth/me')
      .then(setUser)
      .catch((err) => {
        if (err.status === 401 || err.status === 403) {
          clearToken()
        }
      })
      .finally(() => setLoading(false))
  }, [])

  async function login(username, password) {
    const body = new URLSearchParams({ username, password })
    const data = await request('/api/auth/login', { method: 'POST', body })

    setToken(data.access_token)
    setUser(await request('/api/auth/me'))
  }

  function logout() {
    clearToken()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
