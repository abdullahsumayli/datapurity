import { useEffect, useState } from 'react'
import apiClient from '../config/apiClient'
import { Card } from '../types/card'

export function useCards() {
  const [cards, setCards] = useState<Card[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const fetchCards = async (reviewed?: boolean) => {
    setIsLoading(true)
    try {
      const params = reviewed !== undefined ? { reviewed } : {}
      const response = await apiClient.get('/cards', { params })
      setCards(response.data)
    } catch (error) {
      console.error('Failed to fetch cards:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchCards()
  }, [])

  const uploadCard = async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await apiClient.post('/cards/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    await fetchCards()
    return response.data
  }

  const updateCard = async (id: number, data: Partial<Card>) => {
    const response = await apiClient.patch(`/cards/${id}`, data)
    await fetchCards()
    return response.data
  }

  return {
    cards,
    isLoading,
    fetchCards,
    uploadCard,
    updateCard
  }
}
