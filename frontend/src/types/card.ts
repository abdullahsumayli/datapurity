export interface Card {
  id: number
  user_id: number
  original_filename: string
  storage_path: string
  ocr_text?: string
  ocr_confidence?: number
  extracted_name?: string
  extracted_company?: string
  extracted_phone?: string
  extracted_email?: string
  extracted_address?: string
  is_processed: boolean
  is_reviewed: boolean
  created_at: string
  updated_at?: string
}
