function CardUploadPage() {
  return (
    <div className="page-container">
      <h1>Upload Business Cards</h1>
      <p className="page-description">
        Upload images of business cards for automatic OCR processing.
      </p>
      
      {/* TODO: Add CardUploadDropzone component */}
      
      <div className="placeholder-content">
        <p>📇 Card upload dropzone will appear here</p>
        <p>Supported formats: JPG, PNG, PDF</p>
        <p>Batch upload multiple cards at once</p>
      </div>
    </div>
  )
}

export default CardUploadPage
