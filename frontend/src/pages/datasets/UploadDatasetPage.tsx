function UploadDatasetPage() {
  return (
    <div className="page-container">
      <h1>Upload Dataset</h1>
      <p className="page-description">
        Upload a CSV or Excel file containing your contact data for cleaning and validation.
      </p>
      
      {/* TODO: Add DatasetUploadForm component */}
      
      <div className="placeholder-content">
        <p>📤 File upload dropzone will appear here</p>
        <p>Supported formats: CSV, XLSX, XLS</p>
        <p>Maximum file size: 100 MB</p>
      </div>
    </div>
  )
}

export default UploadDatasetPage
