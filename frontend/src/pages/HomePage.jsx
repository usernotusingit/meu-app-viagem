import React, { useState, useEffect, useCallback } from 'react'
import SearchBar from '../components/SearchBar'
import DestinationList from '../components/DestinationList'
import { searchDestinations } from '../services/api'

function HomePage() {
  const [destinations, setDestinations] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  const [currentQuery, setCurrentQuery] = useState('')

  const fetchDestinations = useCallback(async (query) => {
    setIsLoading(true)
    setError(null)
    try {
      const response = await searchDestinations(query)
      setDestinations(response.data)
    } catch (err) {
      console.error("Erro buscando destinos:", err)
      setError(err.message || 'Falha ao buscar dados')
    } finally {
      setIsLoading(false)
    }
  }, [])

  // Busca inicial sem query (destinos populares)
  useEffect(() => {
    fetchDestinations('')
  }, [fetchDestinations])

  const handleSearch = (query) => {
    setCurrentQuery(query)
    fetchDestinations(query)
  }

  return (
    <div className="home-page p-4">
      <header className="home-header mb-4">
        <h1 className="text-2xl font-bold mb-2">Encontre seu próximo destino</h1>
        <SearchBar onSearch={handleSearch} />
      </header>
      <main className="home-content">
        <h2 className="text-xl font-semibold mb-2">
          {currentQuery ? `Resultados para "${currentQuery}"` : "Destinos Populares"}
        </h2>
        <DestinationList
          destinations={destinations}
          isLoading={isLoading}
          error={error}
        />
      </main>
    </div>
  )
}

export default HomePage
