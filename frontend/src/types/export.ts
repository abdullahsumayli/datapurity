export enum ExportFormat {
  CSV = 'csv',
  EXCEL = 'excel',
  JSON = 'json',
  VCARD = 'vcard'
}

export enum ExportStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export interface Export {
  id: number
  user_id: number
  dataset_id?: number
  format: ExportFormat
  status: ExportStatus
  file_path?: string
  file_size?: number
  record_count?: number
  download_url?: string
  expires_at?: string
  created_at: string
  completed_at?: string
}
