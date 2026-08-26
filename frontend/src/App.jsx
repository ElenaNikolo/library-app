import { BrowserRouter, Route, Routes } from 'react-router-dom'

import { AuthProvider } from './AuthContext'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import BookDetail from './pages/BookDetail'
import Catalog from './pages/Catalog'
import Login from './pages/Login'
import MyLoans from './pages/MyLoans'
import MyRequests from './pages/MyRequests'
import StaffLoans from './pages/StaffLoans'
import StaffRequests from './pages/StaffRequests'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Catalog />} />
            <Route path="/books/:id" element={<BookDetail />} />
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
              path="/requests"
              element={
                <ProtectedRoute roles={['MEMBER']}>
                  <MyRequests />
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
            <Route
              path="/staff/requests"
              element={
                <ProtectedRoute roles={['ADMIN', 'LIBRARIAN']}>
                  <StaffRequests />
                </ProtectedRoute>
              }
            />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
