export interface User {
  id: number
  email: string
  full_name?: string
  is_active: boolean
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface SignupRequest {
  email: string
  password: string
  full_name?: string
}

export interface Token {
  access_token: string
  token_type: string
}
