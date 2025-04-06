import React from 'react'
import DestinationCard from './DestinationCard'
import LoadingSpinner from './LoadingSpinner'

function DestinationList({ destinations, isLoading, error }) {
  if (isLoading) {
    return <LoadingSpinner />
  }

  if (error) {
    return <p className="error-message text-red-400">Erro ao carregar destinos: {error}</p>
  }

  if (!destinations || destinations.length === 0) {
    return <p>Nenhum destino encontrado.</p>
  }

  return (
    <div className="destination-list grid grid-cols-1 md:grid-cols-3 gap-4">
      {destinations.map((dest) => (
        <DestinationCard key={dest.id} destination={dest} />
      ))}
    </div>
  )
}

export default DestinationList
