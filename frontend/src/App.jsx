import { BrowserRouter, Route, Routes } from 'react-router-dom'

import { AuthProvider } from './AuthContext'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import Catalog from './pages/Catalog'
import Login from './pages/Login'
import MyLoans from './pages/MyLoans'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Catalog />} />
            <Route path="/login" element={<Login />} />
            <Route
              path="/loans"
              element={
                <ProtectedRoute>
                  <MyLoans />
                </ProtectedRoute>
              }
            />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
