import axios from 'axios'

// Se quiser usar variável de ambiente, coloque em .env: VITE_API_URL=http://127.0.0.1:5000/api
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const searchDestinations = (query = '') => {
  return apiClient.get(`/destinations?q=${encodeURIComponent(query)}`)
}

export const getDestinationDetails = (destinationId) => {
  return apiClient.get(`/destinations/${destinationId}`)
}

export const getDestinationInsights = (destinationId) => {
  return apiClient.get(`/destinations/${destinationId}/insights`)
}
