import { BrowserRouter, Route, Routes } from 'react-router-dom'

import { AuthProvider } from './AuthContext'
import Layout from './components/Layout'
import Catalog from './pages/Catalog'
import Login from './pages/Login'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Catalog />} />
            <Route path="/login" element={<Login />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
