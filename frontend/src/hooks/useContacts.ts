import { useEffect, useState } from 'react'
import apiClient from '../config/apiClient'
import { Contact } from '../types/contact'

export function useContacts() {
  const [contacts, setContacts] = useState<Contact[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const fetchContacts = async (datasetId?: number, search?: string) => {
    setIsLoading(true)
    try {
      const params: any = {}
      if (datasetId) params.dataset_id = datasetId
      if (search) params.search = search
      
      const response = await apiClient.get('/contacts', { params })
      setContacts(response.data)
    } catch (error) {
      console.error('Failed to fetch contacts:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchContacts()
  }, [])

  const getContact = async (id: number) => {
    const response = await apiClient.get(`/contacts/${id}`)
    return response.data
  }

  const updateContact = async (id: number, data: Partial<Contact>) => {
    const response = await apiClient.patch(`/contacts/${id}`, data)
    await fetchContacts()
    return response.data
  }

  return {
    contacts,
    isLoading,
    fetchContacts,
    getContact,
    updateContact
  }
}
