import axios, { AxiosInstance, InternalAxiosRequestConfig } from 'axios'

// استخدام المسار النسبي للـ API
const apiClient: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to attach JWT token
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // عدم تسجيل الخروج التلقائي - فقط إرجاع الخطأ
    // يمكن للمستخدم تسجيل الخروج يدويًا من القائمة
    return Promise.reject(error)
  }
)

export default apiClient
