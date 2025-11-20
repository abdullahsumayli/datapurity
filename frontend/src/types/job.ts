export enum JobStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

export enum JobType {
  DATASET_CLEANING = 'dataset_cleaning',
  CARD_OCR = 'card_ocr',
  EXPORT_GENERATION = 'export_generation',
  BATCH_VALIDATION = 'batch_validation'
}

export interface Job {
  id: number
  user_id: number
  job_type: JobType
  status: JobStatus
  progress: number
  total_items?: number
  processed_items?: number
  error_message?: string
  created_at: string
  started_at?: string
  completed_at?: string
}
