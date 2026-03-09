import { useState, useEffect } from 'react'
import StatusCard from '../components/StatusCard'
import MemoryTimeline from '../components/MemoryTimeline'
import './TrinityStatus.css'

function TrinityStatus() {
  const [status, setStatus] = useState({
    lastMemoryWrite: '...',
    bootstrapStatus: 'loading',
    gapsDetected: 0,
    gapsAcknowledged: 0,
    activeProjects: 3,
    pendingAlerts: 0,
  })
  const [gaps, setGaps] = useState([])
  const [plannedAbsences, setPlannedAbsences] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Fetch bootstrap data from backend
  useEffect(() => {
    fetch('/api/bootstrap/')
      .then(r => {
        if (!r.ok) throw new Error('Failed to fetch bootstrap data')
        return r.json()
      })
      .then(data => {
        setStatus({
          lastMemoryWrite: data.last_known_state,
          bootstrapStatus: data.status,
          gapsDetected: data.gaps_found,
          gapsAcknowledged: data.gaps_acknowledged,
          activeProjects: 3, // TODO: fetch from projects API
          pendingAlerts: data.gaps_found,
        })
        setGaps(data.gaps || [])
        setPlannedAbsences(data.planned_absences || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to fetch bootstrap:', err)
        setError(err.message)
        setLoading(false)
      })
  }, [])

  const getStatusColor = (status) => {
    switch (status) {
      case 'clean': return 'ok'
      case 'warning': return 'warning'
      case 'critical': return 'error'
      case 'loading': return 'info'
      default: return 'info'
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'clean': return 'All Clear'
      case 'warning': return 'Warning'
      case 'critical': return 'Critical'
      case 'loading': return 'Loading...'
      default: return status
    }
  }

  if (loading) {
    return (
      <div className="trinity-status">
        <header className="page-header">
          <h1>Trinity Status</h1>
          <p className="subtitle">Loading agent health...</p>
        </header>
      </div>
    )
  }

  if (error) {
    return (
      <div className="trinity-status">
        <header className="page-header">
          <h1>Trinity Status</h1>
          <p className="subtitle error">Error: {error}</p>
        </header>
      </div>
    )
  }

  return (
    <div className="trinity-status">
      <header className="page-header">
        <h1>Trinity Status</h1>
        <p className="subtitle">Personal agent health and continuity</p>
      </header>

      {/* Bootstrap Layer 0 Status */}
      <section className="section">
        <h2>🚀 Layer 0: Bootstrap Discovery</h2>
        <div className="grid">
          <StatusCard 
            title="Bootstrap Status" 
            status={getStatusColor(status.bootstrapStatus)}
            statusText={getStatusText(status.bootstrapStatus)}
            description={status.bootstrapStatus === 'clean' 
              ? 'All systems operational' 
              : `${status.gapsDetected} active gap${status.gapsDetected !== 1 ? 's' : ''} detected`}
          />
          <StatusCard 
            title="Active Gaps" 
            value={status.gapsDetected}
            status={status.gapsDetected === 0 ? 'ok' : 'warning'}
            description="Missing time periods requiring attention"
          />
          <StatusCard 
            title="Acknowledged"
            value={status.gapsAcknowledged}
            status="info"
            description="Known/expected gaps (planned or acknowledged)"
          />
        </div>
      </section>

      {/* Gap Details */}
      {gaps.length > 0 && (
        <section className="section">
          <h2>⚠️ Gap Details</h2>
          <div className="gap-list">
            {gaps.map((gap, index) => (
              <div key={index} className={`gap-item ${gap.severity} ${gap.acknowledged ? 'acknowledged' : ''}`}>
                <div className="gap-header">
                  <span className="gap-dates">{gap.period_start} → {gap.period_end}</span>
                  <span className={`gap-badge ${gap.severity}`}>{gap.severity}</span>
                  {gap.acknowledged && <span className="gap-badge acknowledged">✓ acknowledged</span>}
                </div>
                <div className="gap-location">{gap.location}</div>
                {gap.reason && <div className="gap-reason">{gap.reason}</div>}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Planned Absences */}
      {plannedAbsences.length > 0 && (
        <section className="section">
          <h2>📅 Planned Absences</h2>
          <div className="absence-list">
            {plannedAbsences.map((absence, index) => (
              <div key={index} className={`absence-item ${absence.active ? 'active' : 'past'}`}>
                <div className="absence-dates">
                  {absence.start} → {absence.end}
                  {absence.active && <span className="absence-badge active">active</span>}
                </div>
                <div className="absence-reason">{absence.reason}</div>
                <div className="absence-return">Expected return: {absence.expected_return}</div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Memory Continuity */}
      <section className="section">
        <h2>🧠 Memory Continuity</h2>
        <div className="grid">
          <StatusCard 
            title="Last Memory Write" 
            value={status.lastMemoryWrite}
            status="ok"
            description="Most recent daily note in workspace"
          />
          <StatusCard 
            title="Active Projects" 
            value={status.activeProjects}
            status="ok"
            description="Projects with recent activity"
          />
          <StatusCard 
            title="Pending Alerts" 
            value={status.pendingAlerts}
            status={status.pendingAlerts === 0 ? 'ok' : 'warning'}
            description="Items requiring attention"
          />
        </div>
        <MemoryTimeline />
      </section>

      {/* Quick Links */}
      <section className="section">
        <h2>🔗 Quick Access</h2>
        <div className="quick-links">
          <a href="#" className="quick-link">Today's Daily Note</a>
          <a href="#" className="quick-link">Veritas Project</a>
          <a href="#" className="quick-link">HEARTBEAT.md</a>
          <a href="#" className="quick-link">SOUL.md</a>
        </div>
      </section>
    </div>
  )
}

export default TrinityStatus
