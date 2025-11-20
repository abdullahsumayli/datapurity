export interface Dataset {
  id: number
  user_id: number
  name: string
  original_filename: string
  file_size: number
  row_count?: number
  column_count?: number
  is_processed: boolean
  health_score?: number
  created_at: string
  updated_at?: string
}

export interface DatasetStats {
  total_records: number
  valid_emails: number
  valid_phones: number
  duplicates: number
  average_quality_score: number
}
