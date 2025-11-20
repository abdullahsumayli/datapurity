import { Link } from 'react-router-dom'

function NotFoundPage() {
  return (
    <div className="page-container" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
      <h1 style={{ fontSize: '4rem', margin: '0' }}>404</h1>
      <h2>Page Not Found</h2>
      <p className="page-description">
        The page you're looking for doesn't exist.
      </p>
      <Link to="/dashboard" className="btn-primary" style={{ marginTop: '2rem', display: 'inline-block' }}>
        Go to Dashboard
      </Link>
    </div>
  )
}

export default NotFoundPage
