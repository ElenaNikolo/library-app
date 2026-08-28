import { BrowserRouter, Route, Routes } from 'react-router-dom'

import { AuthProvider } from './AuthContext'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import AdminUsers from './pages/AdminUsers'
import BookDetail from './pages/BookDetail'
import Catalog from './pages/Catalog'
import Login from './pages/Login'
import MyLoans from './pages/MyLoans'
import MyRequests from './pages/MyRequests'
import Register from './pages/Register'
import StaffBooks from './pages/StaffBooks'
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
            <Route path="/register" element={<Register />} />
            <Route
              path="/loans"
              element={
                <ProtectedRoute roles={['MEMBER']}>
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
              path="/staff/books"
              element={
                <ProtectedRoute roles={['ADMIN', 'LIBRARIAN']}>
                  <StaffBooks />
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
              path="/admin/users"
              element={
                <ProtectedRoute roles={['ADMIN']}>
                  <AdminUsers />
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
