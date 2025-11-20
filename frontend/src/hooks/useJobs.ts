import { useEffect, useState } from 'react'
import apiClient from '../config/apiClient'
import { Job } from '../types/job'

export function useJobs() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const fetchJobs = async () => {
    setIsLoading(true)
    try {
      const response = await apiClient.get('/jobs')
      setJobs(response.data)
    } catch (error) {
      console.error('Failed to fetch jobs:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchJobs()
  }, [])

  const getJob = async (id: number) => {
    const response = await apiClient.get(`/jobs/${id}`)
    return response.data
  }

  const cancelJob = async (id: number) => {
    const response = await apiClient.post(`/jobs/${id}/cancel`)
    await fetchJobs()
    return response.data
  }

  return {
    jobs,
    isLoading,
    fetchJobs,
    getJob,
    cancelJob
  }
}
