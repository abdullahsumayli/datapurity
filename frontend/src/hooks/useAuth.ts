import { useEffect, useState } from 'react'
import apiClient from '../config/apiClient'
import { LoginRequest, SignupRequest, User } from '../types/auth'

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in on mount
    const token = localStorage.getItem('access_token')
    if (token) {
      // Fetch current user from API
      fetchCurrentUser()
    } else {
      setIsLoading(false)
    }
  }, [])

  const fetchCurrentUser = async () => {
    try {
      const response = await apiClient.get('/auth/me')
      setUser(response.data)
      setIsAuthenticated(true)
    } catch (error) {
      // Token expired or invalid
      localStorage.removeItem('access_token')
      setIsAuthenticated(false)
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (credentials: LoginRequest) => {
    const response = await apiClient.post('/auth/login', credentials)
    const { access_token } = response.data
    
    localStorage.setItem('access_token', access_token)
    setIsAuthenticated(true)
    
    // Fetch user data
    await fetchCurrentUser()
  }

  const signup = async (data: SignupRequest) => {
    await apiClient.post('/auth/signup', data)
    
    // Login after successful signup
    await login({ email: data.email, password: data.password })
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setUser(null)
    setIsAuthenticated(false)
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    login,
    signup,
    logout
  }
}
