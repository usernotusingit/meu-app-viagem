import React from 'react'
import { Link } from 'react-router-dom'

function DestinationCard({ destination }) {
  return (
    <Link
      to={`/destination/${destination.id}`}
      className="destination-card block bg-gray-800 rounded shadow hover:shadow-md transition-shadow p-2 m-2"
    >
      <img
        src={destination.imageUrl || 'https://via.placeholder.com/300x200?text=Destino'}
        alt={destination.name}
        className="card-image w-full h-48 object-cover rounded"
      />
      <div className="card-content mt-2">
        <h3 className="card-title text-lg font-bold">{destination.name}</h3>
        <p className="card-country text-gray-400">{destination.country}</p>
      </div>
    </Link>
  )
}

export default DestinationCard
