import React, { useState } from 'react'

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (event) => {
    event.preventDefault()
    onSearch(query)
  }

  return (
    <form onSubmit={handleSubmit} className="search-bar flex gap-2">
      <input
        type="text"
        placeholder="Para onde você quer ir?"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="search-input px-2 py-1 rounded text-black w-64"
      />
      <button
        type="submit"
        className="search-button bg-blue-500 text-white px-4 py-1 rounded"
      >
        Buscar
      </button>
    </form>
  )
}

export default SearchBar
