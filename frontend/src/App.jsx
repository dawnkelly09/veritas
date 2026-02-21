import { Routes, Route, Link } from 'react-router-dom'
import TrinityStatus from './pages/TrinityStatus'
import VeritasIntegrity from './pages/VeritasIntegrity'
import './App.css'

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-brand">
          <h1>🛡️ Veritas</h1>
          <span className="tagline">Agent Constitution Protocol</span>
        </div>
        <div className="nav-links">
          <Link to="/" className="nav-link">Trinity Status</Link>
          <Link to="/integrity" className="nav-link">Veritas Integrity</Link>
        </div>
      </nav>
      
      <main className="main-content">
        <Routes>
          <Route path="/" element={<TrinityStatus />} />
          <Route path="/integrity" element={<VeritasIntegrity />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
