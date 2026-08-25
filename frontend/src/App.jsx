import { BrowserRouter, Route, Routes } from 'react-router-dom'

import { AuthProvider } from './AuthContext'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import Catalog from './pages/Catalog'
import Login from './pages/Login'
import MyLoans from './pages/MyLoans'
import StaffLoans from './pages/StaffLoans'

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
            <Route
              path="/staff/loans"
              element={
                <ProtectedRoute roles={['ADMIN', 'LIBRARIAN']}>
                  <StaffLoans />
                </ProtectedRoute>
              }
            />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
