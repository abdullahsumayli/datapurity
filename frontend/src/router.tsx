import { Navigate, Route, Routes } from 'react-router-dom'
import { useAuth } from './hooks/useAuth'

// Layouts
import AppShell from './layouts/AppShell/AppShell'

// Marketing
import { LandingPage } from './pages/marketing/LandingPage'

// Auth Pages
import GoogleCallbackPage from './pages/auth/GoogleCallbackPage'
import LoginPage from './pages/auth/LoginPage'

// Protected Pages
import BillingPage from './pages/billing/BillingPage'
import CardReviewPage from './pages/cards/CardReviewPage'
import CardUploadPage from './pages/cards/CardUploadPage'
import ContactsPage from './pages/contacts/ContactsPage'
import DashboardPage from './pages/dashboard/DashboardPage'
import DatasetDetailsPage from './pages/datasets/DatasetDetailsPage'
import UploadDatasetPage from './pages/datasets/UploadDatasetPage'
import ExportsPage from './pages/exports/ExportsPage'
import JobDetailsPage from './pages/jobs/JobDetailsPage'
import JobsListPage from './pages/jobs/JobsListPage'
import NotFoundPage from './pages/misc/NotFoundPage'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth()
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}

function AppRouter() {
  return (
    <Routes>
      {/* Landing Page */}
      <Route path="/" element={<LandingPage />} />
      
      {/* Public Routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/auth/callback" element={<GoogleCallbackPage />} />

      {/* Protected Routes */}
      <Route
        path="/app"
        element={
          <ProtectedRoute>
            <AppShell />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/app/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        
        <Route path="datasets">
          <Route path="upload" element={<UploadDatasetPage />} />
          <Route path=":id" element={<DatasetDetailsPage />} />
        </Route>
        
        <Route path="jobs">
          <Route index element={<JobsListPage />} />
          <Route path=":id" element={<JobDetailsPage />} />
        </Route>
        
        <Route path="cards">
          <Route path="upload" element={<CardUploadPage />} />
          <Route path="review" element={<CardReviewPage />} />
        </Route>
        
        <Route path="contacts" element={<ContactsPage />} />
        <Route path="exports" element={<ExportsPage />} />
        <Route path="billing" element={<BillingPage />} />
      </Route>

      {/* 404 */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

export default AppRouter
