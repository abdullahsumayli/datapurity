import { useEffect, useState } from 'react'
import apiClient from '../config/apiClient'
import { Export, ExportFormat } from '../types/export'

export function useExports() {
  const [exports, setExports] = useState<Export[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const fetchExports = async () => {
    setIsLoading(true)
    try {
      const response = await apiClient.get('/exports')
      setExports(response.data)
    } catch (error) {
      console.error('Failed to fetch exports:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchExports()
  }, [])

  const createExport = async (format: ExportFormat, datasetId?: number, filters?: any) => {
    const response = await apiClient.post('/exports', {
      format,
      dataset_id: datasetId,
      filters
    })
    
    await fetchExports()
    return response.data
  }

  const getExport = async (id: number) => {
    const response = await apiClient.get(`/exports/${id}`)
    return response.data
  }

  return {
    exports,
    isLoading,
    fetchExports,
    createExport,
    getExport
  }
}
