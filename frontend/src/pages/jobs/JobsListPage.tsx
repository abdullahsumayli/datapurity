function JobsListPage() {
  return (
    <div className="page-container">
      <h1>Background Jobs</h1>
      <p className="page-description">
        Monitor the status of your data processing jobs.
      </p>
      
      {/* TODO: Add JobsTable component */}
      {/* TODO: Add polling for job status updates */}
      
      <div className="placeholder-content">
        <p>⚙️ Jobs table will appear here</p>
        <p>Track dataset cleaning, OCR processing, and exports</p>
      </div>
    </div>
  )
}

export default JobsListPage
