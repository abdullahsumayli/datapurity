import { useEffect, useState } from 'react'
import apiClient from '../config/apiClient'
import { Dataset } from '../types/dataset'

export function useDatasets() {
  const [datasets, setDatasets] = useState<Dataset[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const fetchDatasets = async () => {
    setIsLoading(true)
    try {
      const response = await apiClient.get('/datasets')
      setDatasets(response.data)
    } catch (error) {
      console.error('Failed to fetch datasets:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchDatasets()
  }, [])

  const getDataset = async (id: number) => {
    const response = await apiClient.get(`/datasets/${id}`)
    return response.data
  }

  const uploadDataset = async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await apiClient.post('/datasets/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    await fetchDatasets()
    return response.data
  }

  return {
    datasets,
    isLoading,
    fetchDatasets,
    getDataset,
    uploadDataset
  }
}
