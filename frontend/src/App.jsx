import React from "react"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import HomePage from "./pages/HomePage"
import DestinationDetailPage from "./pages/DestinationDetailPage"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/destination/:destinationId" element={<DestinationDetailPage />} />
      </Routes>
    </Router>
  )
}

export default App
