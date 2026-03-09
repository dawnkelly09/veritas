import { useState, useEffect } from 'react'
import StatusCard from '../components/StatusCard'
import MemoryTimeline from '../components/MemoryTimeline'
import './TrinityStatus.css'

function TrinityStatus() {
  const [status, setStatus] = useState({
    lastMemoryWrite: '2026-02-21 12:37',
    bootstrapStatus: 'clean',
    gapsDetected: 0,
    activeProjects: 3,
    pendingAlerts: 0,
  })

  // Fetch status from backend API
  useEffect(() => {
    fetch('/api/status')
      .then(r => r.json())
      .then(data => {
        setStatus({
          lastMemoryWrite: data.last_memory_write,
          bootstrapStatus: data.bootstrap_status,
          gapsDetected: data.gaps_detected,
          activeProjects: data.active_projects,
          pendingAlerts: data.pending_alerts,
        })
      })
      .catch(err => console.error('Failed to fetch status:', err))
  }, [])

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
            status={status.bootstrapStatus}
            statusText={status.bootstrapStatus === 'clean' ? 'All Clear' : 'Gaps Detected'}
            description="Last bootstrap check completed successfully"
          />
          <StatusCard 
            title="Context Gaps" 
            value={status.gapsDetected}
            status={status.gapsDetected === 0 ? 'ok' : 'warning'}
            description="Missing time periods since last session"
          />
          <StatusCard 
            title="Fallback Locations Checked"
            value={3}
            status="ok"
            description="Workspace, Obsidian vault, Desktop backup"
          />
        </div>
      </section>

      {/* Memory Continuity */}
      <section className="section">
        <h2>🧠 Memory Continuity</h2>
        <div className="grid">
          <StatusCard 
            title="Last Memory Write" 
            value={status.lastMemoryWrite}
            status="ok"
            description="Most recent daily note in Obsidian vault"
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
