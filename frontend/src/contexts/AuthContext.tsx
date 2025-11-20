import { createContext, ReactNode, useContext, useEffect, useState } from 'react'
import apiClient from '../config/apiClient'
import { LoginRequest, SignupRequest, User } from '../types/auth'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (credentials: LoginRequest) => Promise<void>
  signup: (data: SignupRequest) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check if user is logged in on mount
    const token = localStorage.getItem('access_token')
    if (token) {
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
    const response = await apiClient.post('/auth/signup', data)
    const { access_token } = response.data
    
    localStorage.setItem('access_token', access_token)
    setIsAuthenticated(true)
    
    // Fetch user data
    await fetchCurrentUser()
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setUser(null)
    setIsAuthenticated(false)
  }

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, isLoading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
