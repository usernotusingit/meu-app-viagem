import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { getDestinationDetails, getDestinationInsights } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'

function DestinationDetailPage() {
  const { destinationId } = useParams()
  const [destination, setDestination] = useState(null)
  const [insights, setInsights] = useState(null)
  const [isLoadingDetails, setIsLoadingDetails] = useState(true)
  const [isLoadingInsights, setIsLoadingInsights] = useState(true)
  const [errorDetails, setErrorDetails] = useState(null)
  const [errorInsights, setErrorInsights] = useState(null)

  useEffect(() => {
    const fetchDetails = async () => {
      setIsLoadingDetails(true)
      setErrorDetails(null)
      try {
        const response = await getDestinationDetails(destinationId)
        setDestination(response.data)
      } catch (err) {
        console.error("Erro buscando detalhes:", err)
        setErrorDetails(err.message || 'Falha ao buscar detalhes do destino.')
      } finally {
        setIsLoadingDetails(false)
      }
    }

    const fetchInsights = async () => {
      setIsLoadingInsights(true)
      setErrorInsights(null)
      try {
        const response = await getDestinationInsights(destinationId)
        if (response.data.error) {
          setErrorInsights(`Erro da IA: ${response.data.error}`)
          setInsights({ news: 'Indisponível', tips: 'Indisponível', prices: 'Indisponível' })
        } else {
          setInsights(response.data)
        }
      } catch (err) {
        console.error("Erro buscando insights:", err)
        setErrorInsights(err.message || 'Falha ao buscar insights da IA.')
        setInsights({ news: 'Erro de conexão', tips: 'Erro de conexão', prices: 'Erro de conexão' })
      } finally {
        setIsLoadingInsights(false)
      }
    }

    fetchDetails()
    fetchInsights()
  }, [destinationId])

  if (isLoadingDetails) {
    return <LoadingSpinner />
  }

  if (errorDetails) {
    return <p className="error-message text-red-400">Erro: {errorDetails}</p>
  }

  if (!destination) {
    return <p>Destino não encontrado.</p>
  }

  // Função para exibir texto em múltiplas linhas
  const formatMultilineText = (text) => {
    if (!text) return ''
    return text.split('\n').map((line, index) => (
      <React.Fragment key={index}>
        {line}
        <br />
      </React.Fragment>
    ))
  }

  return (
    <div className="destination-detail-page p-4">
      <header
        className="detail-header h-64 bg-center bg-cover flex items-center justify-center mb-4"
        style={{ backgroundImage: `url(${destination.imageUrl || 'https://via.placeholder.com/1200x400?text=Destino'})` }}
      >
        <div className="bg-black bg-opacity-50 p-4 text-center">
          <h1 className="text-3xl font-bold">{destination.name}</h1>
          <p className="text-lg">{destination.country}</p>
        </div>
      </header>

      <div className="detail-content">
        <section className="description-section mb-4">
          <h2 className="text-2xl font-semibold mb-2">Sobre {destination.name}</h2>
          <p>{destination.description}</p>
        </section>

        <section className="insights-section">
          <h2 className="text-2xl font-semibold mb-2">Informações e Dicas (via IA)</h2>
          {isLoadingInsights && <LoadingSpinner />}
          {errorInsights && <p className="error-message text-red-400">{errorInsights}</p>}
          {insights && !errorInsights && (
            <div className="insights-grid grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="insight-card bg-gray-800 p-4 rounded">
                <h3 className="text-xl font-bold mb-2">Novidades Recentes</h3>
                <p>{formatMultilineText(insights.news)}</p>
              </div>
              <div className="insight-card bg-gray-800 p-4 rounded">
                <h3 className="text-xl font-bold mb-2">Dicas Úteis</h3>
                <p>{formatMultilineText(insights.tips)}</p>
              </div>
              <div className="insight-card bg-gray-800 p-4 rounded">
                <h3 className="text-xl font-bold mb-2">Preços Estimados</h3>
                <p>{formatMultilineText(insights.prices)}</p>
              </div>
            </div>
          )}
          {!insights && !isLoadingInsights && !errorInsights && (
            <p>Não foi possível carregar os insights.</p>
          )}
        </section>
      </div>
    </div>
  )
}

export default DestinationDetailPage
