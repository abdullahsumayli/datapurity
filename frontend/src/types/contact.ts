export interface Contact {
  id: number
  dataset_id: number
  first_name?: string
  last_name?: string
  full_name?: string
  company?: string
  job_title?: string
  email?: string
  phone?: string
  mobile?: string
  address_line1?: string
  address_line2?: string
  city?: string
  state?: string
  postal_code?: string
  country?: string
  email_valid?: boolean
  phone_valid?: boolean
  overall_quality_score?: number
  is_duplicate: boolean
  created_at: string
  updated_at?: string
}
